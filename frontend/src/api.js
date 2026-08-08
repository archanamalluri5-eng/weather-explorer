// Thin fetch wrapper around the Weather Explorer backend.
// The base URL comes from VITE_API_BASE_URL (set at build/deploy time) and
// defaults to the dev-server proxy so no CORS setup is needed locally.

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/$/, "");

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const body = await res.json().catch(() => null);

  if (!res.ok) {
    const message =
      (body && (body.message || body.detail)) ||
      `Request failed with status ${res.status}`;
    const error = new Error(message);
    error.status = res.status;
    throw error;
  }
  return body;
}

export function storeWeatherData(payload) {
  return request("/store-weather-data", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function listWeatherFiles() {
  return request("/list-weather-files");
}

export function getWeatherFileContent(file) {
  return request(`/weather-file-content/${encodeURIComponent(file)}`);
}
