/**
 * API helper – all calls to the FastAPI backend.
 */

const BASE = "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, options);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

/* ---- Chat ---- */
export async function sendMessage(message) {
  return request("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
}

/* ---- Files ---- */
export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  return request("/api/upload", { method: "POST", body: form });
}

export async function listFiles() {
  return request("/api/files");
}

export async function deleteFile(filename) {
  return request(`/api/files/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });
}

/* ---- Settings ---- */
export async function updateSettings(payload) {
  return request("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

/* ---- Status ---- */
export async function getStatus() {
  return request("/api/status");
}
