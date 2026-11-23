from pathlib import Path
import os
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent
load_dotenv(BACKEND_DIR / ".env")

APP_NAME = os.getenv("APP_NAME", "EcoMind AI")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./ecomind_dev.db"
)
MODEL_PATH = Path(os.getenv(
    "MODEL_PATH",
    str(PROJECT_DIR / "models" / "ecomind_mobilenetv2.keras")
))
if not MODEL_PATH.is_absolute():
    MODEL_PATH = (BACKEND_DIR / MODEL_PATH).resolve()

CLASS_NAMES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
IMAGE_SIZE = (224, 224)
