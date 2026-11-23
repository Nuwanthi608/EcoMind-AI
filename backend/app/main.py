from io import BytesIO
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from PIL import Image, UnidentifiedImageError

from .config import APP_NAME, CLASS_NAMES
from .database import Base, engine, get_db
from .models import Prediction
from .schemas import PredictionResponse
from .impact import get_recommendation
from .predictor import predict_image
from .pdf_report import create_prediction_pdf

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": APP_NAME}

@app.get("/api/classes")
def classes():
    return {"classes": CLASS_NAMES}

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image must be smaller than 10 MB.")
    try:
        image = Image.open(BytesIO(content))
        image.verify()
        image = Image.open(BytesIO(content))
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image.")

    try:
        category, confidence = predict_image(image)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

    advice, impact = get_recommendation(category)
    record = Prediction(
        filename=Path(file.filename or "upload").name,
        category=category,
        confidence=confidence,
        disposal_advice=advice,
        impact_estimate=impact
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/api/history", response_model=list[PredictionResponse])
def history(limit: int = 20, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    return db.query(Prediction).order_by(Prediction.id.desc()).limit(limit).all()

@app.get("/api/report/{prediction_id}")
def report(prediction_id: int, db: Session = Depends(get_db)):
    record = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prediction not found.")
    pdf = create_prediction_pdf(record)
    return StreamingResponse(
        BytesIO(pdf),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=ecomind-report-{prediction_id}.pdf"}
    )
