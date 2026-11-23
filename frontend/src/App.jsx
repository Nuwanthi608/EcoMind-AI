import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadHistory() {
    try {
      const response = await fetch(`${API}/api/history`);
      if (response.ok) setHistory(await response.json());
    } catch {
      // API may not have started yet.
    }
  }

  useEffect(() => { loadHistory(); }, []);

  function chooseFile(event) {
    const selected = event.target.files?.[0];
    setFile(selected || null);
    setResult(null);
    setError("");
    if (selected) setPreview(URL.createObjectURL(selected));
    else setPreview("");
  }

  async function analyze(event) {
    event.preventDefault();
    if (!file) {
      setError("Please choose a waste image first.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    const body = new FormData();
    body.append("file", file);
    try {
      const response = await fetch(`${API}/api/predict`, {
        method: "POST",
        body
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Prediction failed.");
      setResult(data);
      await loadHistory();
    } catch (err) {
      setError(err.message || "Could not connect to the API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="#"><span className="brand-mark">E</span> EcoMind <b>AI</b></a>
        <span className="status"><i /> Waste intelligence</span>
      </header>

      <section className="hero">
        <p className="eyebrow">AI-POWERED WASTE IDENTIFICATION</p>
        <h1>Make every waste decision<br /><em>count.</em></h1>
        <p className="intro">Upload an image to identify its waste category and get practical disposal guidance.</p>
      </section>

      <section className="workspace">
        <div className="panel upload-panel">
          <div className="panel-heading">
            <div><p className="eyebrow">01 / IMAGE INPUT</p><h2>Analyze waste</h2></div>
            <span className="step">01</span>
          </div>
          <form onSubmit={analyze}>
            <label className="dropzone">
              {preview ? <img src={preview} alt="Selected waste preview" /> :
                <span className="upload-icon">↑</span>}
              <strong>{file ? file.name : "Choose a waste image"}</strong>
              <small>JPG, PNG or WEBP · Maximum 10 MB</small>
              <input type="file" accept="image/*" onChange={chooseFile} />
            </label>
            <button className="primary" disabled={loading}>
              {loading ? "Analyzing image..." : "Identify waste"}
              <span>↗</span>
            </button>
          </form>
          {error && <p className="error">{error}</p>}
        </div>

        <div className="panel result-panel">
          <div className="panel-heading">
            <div><p className="eyebrow">02 / AI ANALYSIS</p><h2>Detection result</h2></div>
            <span className="step">02</span>
          </div>
          {!result ? <div className="empty">
            <div className="empty-orbit">✳</div>
            <strong>Your result will appear here</strong>
            <p>Upload an image and run the AI analysis to see the detected category.</p>
          </div> : <div className="result">
            <span className="result-label">DETECTED CATEGORY</span>
            <h3>{result.category}</h3>
            <div className="confidence">
              <div><span>Model confidence</span><b>{(result.confidence * 100).toFixed(1)}%</b></div>
              <div className="bar"><i style={{ width: `${result.confidence * 100}%` }} /></div>
            </div>
            <div className="advice"><b>Disposal recommendation</b><p>{result.disposal_advice}</p></div>
            <div className="advice"><b>Environmental impact</b><p>{result.impact_estimate}</p></div>
            <a className="report-link" href={`${API}/api/report/${result.id}`}>Download PDF report ↗</a>
          </div>}
        </div>
      </section>

      <section className="panel history-panel">
        <div className="panel-heading">
          <div><p className="eyebrow">03 / RECENT ACTIVITY</p><h2>Prediction history</h2></div>
          <button className="refresh" onClick={loadHistory}>Refresh ↻</button>
        </div>
        {history.length === 0 ? <p className="muted">No predictions yet. Your completed analyses will appear here.</p> :
          <div className="history-list">{history.map(item => (
            <div className="history-row" key={item.id}>
              <span className="history-dot" />
              <div><b>{item.category}</b><small>{item.filename}</small></div>
              <strong>{(item.confidence * 100).toFixed(1)}%</strong>
              <a href={`${API}/api/report/${item.id}`}>PDF ↗</a>
            </div>
          ))}</div>}
      </section>
      <footer>EcoMind AI <span>·</span> Classify thoughtfully. Dispose responsibly.</footer>
    </main>
  );
}
