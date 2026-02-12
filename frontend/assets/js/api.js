/////////////// BASE FETCH WRAPPER, AUTH HEADER ////////////////

const API_BASE = ''; // relative to FastAPI

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });
    if (!response.ok) {
        let error;
        try {
            error = await response.json();
        } catch {
            error = { detail: response.statusText };
        }
        throw new Error(error.detail || `HTTP ${response.status}`);
    }
    return response.json();
}