const API_BASE = "http://127.0.0.1:5000/api/v1";

function saveToken(token) {
    localStorage.setItem("accessToken", token);
}

function getToken() {
    return localStorage.getItem("accessToken") || "";
}

function clearToken() {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("currentRunId");
}

function saveCurrentRunId(runId) {
    localStorage.setItem("currentRunId", String(runId));
}

function getCurrentRunId() {
    return localStorage.getItem("currentRunId");
}

function clearCurrentRunId() {
    localStorage.removeItem("currentRunId");
}

async function apiRequest(path, method = "GET", body = null, withAuth = false) {
    const headers = {
        "Content-Type": "application/json"
    };

    if (withAuth) {
        const token = getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
    }

    const options = {
        method,
        headers
    };

    if (body !== null) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(API_BASE + path, options);

    let data;
    try {
        data = await response.json();
    } catch (e) {
        data = { ok: false, error: { message: "Invalid JSON response" } };
    }

    return {
        status: response.status,
        data
    };
}

function renderResponse(elementId, title, result) {
    const el = document.getElementById(elementId);
    if (!el) return;

    el.textContent =
        `${title}\n\nHTTP Status: ${result.status}\n\n` +
        `${JSON.stringify(result.data, null, 2)}`;
}

function renderToken(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;

    const token = getToken();
    el.textContent = token ? token : "Токен не сохранён";
}

function goTo(page) {
    window.location.href = page;
}

function logout() {
    clearToken();
    goTo("index.html");
}