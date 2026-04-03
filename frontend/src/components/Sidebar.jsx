import { useState, useEffect, useRef, useCallback } from "react";
import {
  uploadFile,
  listFiles,
  deleteFile,
  updateSettings,
} from "../api";

const MODELS = [
  { value: "llama-3.3-70b-versatile", label: "Llama 3.3 70B" },
  { value: "llama-3.1-70b-versatile", label: "Llama 3.1 70B" },
  { value: "llama-3.1-8b-instant", label: "Llama 3.1 8B Instant" },
  { value: "mixtral-8x7b-32768", label: "Mixtral 8×7B" },
];

export default function Sidebar({ status, onToast, refreshStatus }) {
  /* ---- state ---- */
  const [tab, setTab] = useState("files"); // "files" | "settings"
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  // settings
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("llama-3.3-70b-versatile");
  const [temperature, setTemperature] = useState(0);
  const [topK, setTopK] = useState(3);
  const [saving, setSaving] = useState(false);

  const fileInputRef = useRef(null);

  /* ---- load files ---- */
  const fetchFiles = useCallback(async () => {
    try {
      const data = await listFiles();
      setFiles(data.files || []);
    } catch {
      /* silent */
    }
  }, []);

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  /* ---- handlers ---- */
  const handleUpload = async (file) => {
    if (!file) return;
    if (!file.name.endsWith(".txt")) {
      onToast("Only .txt files are supported", "error");
      return;
    }
    setUploading(true);
    try {
      const data = await uploadFile(file);
      onToast(data.message, "success");
      fetchFiles();
      refreshStatus();
    } catch (err) {
      onToast(err.message, "error");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (name) => {
    try {
      await deleteFile(name);
      onToast(`Deleted ${name}`, "success");
      fetchFiles();
    } catch (err) {
      onToast(err.message, "error");
    }
  };

  const handleSaveSettings = async () => {
    setSaving(true);
    try {
      const payload = {};
      if (apiKey) payload.api_key = apiKey;
      payload.model_name = model;
      payload.temperature = temperature;
      payload.top_k = topK;
      await updateSettings(payload);
      onToast("Settings saved", "success");
      refreshStatus();
    } catch (err) {
      onToast(err.message, "error");
    } finally {
      setSaving(false);
    }
  };

  /* ---- drag & drop ---- */
  const onDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };
  const onDragLeave = () => setDragOver(false);
  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleUpload(file);
  };

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <aside className="sidebar">
      {/* Header */}
      <div className="sidebar-header">
        <div className="sidebar-logo">💰</div>
        <div>
          <div className="sidebar-title">FinanceRAG</div>
          <div className="sidebar-subtitle">AI Transaction Analyst</div>
        </div>
      </div>

      {/* Nav tabs */}
      <div style={{ padding: "12px 16px 0" }}>
        <div className="sidebar-nav">
          <button
            className={`sidebar-nav-btn ${tab === "files" ? "active" : ""}`}
            onClick={() => setTab("files")}
          >
            📁 Documents
          </button>
          <button
            className={`sidebar-nav-btn ${tab === "settings" ? "active" : ""}`}
            onClick={() => setTab("settings")}
          >
            ⚙️ Settings
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="sidebar-body">
        {tab === "files" && (
          <>
            {/* Upload zone */}
            <div
              className={`drop-zone ${dragOver ? "drag-over" : ""}`}
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              onDrop={onDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="drop-zone-icon">
                {uploading ? "⏳" : "📄"}
              </div>
              <div className="drop-zone-text">
                {uploading
                  ? "Processing file…"
                  : "Drop a .txt file or click to upload"}
              </div>
              <div className="drop-zone-hint">
                Transaction data in plain text format
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt"
                onChange={(e) => handleUpload(e.target.files[0])}
              />
            </div>

            {/* File list */}
            <div className="sidebar-section-label">Uploaded Files</div>
            {files.length === 0 ? (
              <div
                style={{
                  textAlign: "center",
                  padding: "20px 0",
                  color: "var(--text-muted)",
                  fontSize: "13px",
                }}
              >
                No files uploaded yet
              </div>
            ) : (
              files.map((f, i) => (
                <div
                  className="file-item"
                  key={f.name}
                  style={{ animationDelay: `${i * 60}ms` }}
                >
                  <span className="file-item-icon">📄</span>
                  <div className="file-item-info">
                    <div className="file-item-name">{f.name}</div>
                    <div className="file-item-size">{formatSize(f.size)}</div>
                  </div>
                  <button
                    className="file-item-delete"
                    onClick={() => handleDelete(f.name)}
                    title="Delete file"
                  >
                    🗑️
                  </button>
                </div>
              ))
            )}

            {/* DB status */}
            <div className="sidebar-section-label">Database Status</div>
            <div className="settings-card">
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span
                  className={`status-dot ${
                    status?.vectorstore_ready ? "green" : "red"
                  }`}
                />
                <span style={{ fontSize: 13 }}>
                  {status?.vectorstore_ready
                    ? "Vector DB ready"
                    : "No vector DB"}
                </span>
              </div>
            </div>
          </>
        )}

        {tab === "settings" && (
          <>
            {/* API Key */}
            <div className="sidebar-section-label">API Configuration</div>
            <div className="settings-card">
              <div className="form-group">
                <label className="form-label">Groq API Key</label>
                <input
                  className="form-input"
                  type="password"
                  placeholder="gsk_..."
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                />
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  fontSize: 12,
                  color: "var(--text-muted)",
                }}
              >
                <span
                  className={`status-dot ${
                    status?.api_key_set ? "green" : "red"
                  }`}
                />
                {status?.api_key_set
                  ? "API key configured"
                  : "No API key set"}
              </div>
            </div>

            {/* Model */}
            <div className="sidebar-section-label">Model Settings</div>
            <div className="settings-card">
              <div className="form-group">
                <label className="form-label">LLM Model</label>
                <select
                  className="form-select"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                >
                  {MODELS.map((m) => (
                    <option key={m.value} value={m.value}>
                      {m.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Temperature</label>
                <div className="form-range-wrap">
                  <input
                    type="range"
                    className="form-range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={temperature}
                    onChange={(e) =>
                      setTemperature(parseFloat(e.target.value))
                    }
                  />
                  <span className="form-range-value">
                    {temperature.toFixed(1)}
                  </span>
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Top-K Results</label>
                <div className="form-range-wrap">
                  <input
                    type="range"
                    className="form-range"
                    min="1"
                    max="10"
                    step="1"
                    value={topK}
                    onChange={(e) => setTopK(parseInt(e.target.value))}
                  />
                  <span className="form-range-value">{topK}</span>
                </div>
              </div>
            </div>

            {/* Save button */}
            <button
              className="btn btn-primary btn-block"
              onClick={handleSaveSettings}
              disabled={saving}
            >
              {saving ? "Saving…" : "💾 Save Settings"}
            </button>
          </>
        )}
      </div>

      {/* Footer */}
      <div className="sidebar-footer">
        Built with ❤️ using FastAPI &amp; React
      </div>
    </aside>
  );
}
