const TOKEN_KEY = "cj_token";
const USER_KEY  = "cj_user";

// ── Storage helpers ──────────────────────────────────────────────────────────

function saveToken(token) { localStorage.setItem(TOKEN_KEY, token); }
function getToken()       { return localStorage.getItem(TOKEN_KEY); }

function saveUser(user)   { localStorage.setItem(USER_KEY, JSON.stringify(user)); }
function getUser()        {
  try { return JSON.parse(localStorage.getItem(USER_KEY)); } catch { return null; }
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

// ── Token helpers ────────────────────────────────────────────────────────────

function decodeToken(token) {
  try { return JSON.parse(atob(token.split(".")[1])); } catch { return null; }
}

function isTokenValid(token) {
  const p = decodeToken(token);
  return p && p.exp * 1000 > Date.now();
}

function authHeaders() {
  return { "Authorization": `Bearer ${getToken()}`, "Content-Type": "application/json" };
}

// ── Navbar ───────────────────────────────────────────────────────────────────

function renderNavAuth() {
  const area = document.getElementById("nav-auth");
  if (!area) return;
  const token = getToken();
  const user  = getUser();

  if (token && isTokenValid(token) && user) {
    area.innerHTML = `
      <a href="/my-applications" class="text-sm hover:text-indigo-600 transition font-medium">My Applications</a>
      <a href="/dashboard"       class="text-sm hover:text-indigo-600 transition font-medium">Dashboard</a>
      <span class="text-gray-400">|</span>
      <span class="text-gray-500 text-sm">Hi, <span class="font-semibold text-gray-700">${escapeHtml(user.name.split(" ")[0])}</span></span>
      <button onclick="logout()" class="text-sm text-red-500 hover:text-red-700 transition font-medium">Logout</button>
    `;
  } else {
    area.innerHTML = `
      <a href="/login"    class="text-sm hover:text-indigo-600 transition font-medium">Login</a>
      <a href="/register" class="text-sm bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg transition font-medium">Register</a>
    `;
  }
}

function logout() {
  clearAuth();
  window.location.href = "/";
}

// ── "Post a Job" smart redirect ──────────────────────────────────────────────

async function postJobFlow() {
  const token = getToken();

  if (!token || !isTokenValid(token)) {
    window.location.href = "/login?next=" + encodeURIComponent("/jobs/new");
    return;
  }

  if (!getUser()) {
    const res = await fetch("/auth/me", { headers: authHeaders() });
    if (!res.ok) { clearAuth(); window.location.href = "/login"; return; }
    saveUser(await res.json());
  }

  const userId = getUser().id;
  const res = await fetch("/companies/");
  if (!res.ok) { window.location.href = "/login"; return; }
  const companies = await res.json();
  const mine = companies.filter(c => c.owner_id === userId);

  if (mine.length === 0) {
    window.location.href = "/companies/new?next=" + encodeURIComponent("/jobs/new");
  } else {
    window.location.href = "/jobs/new";
  }
}

// ── Shared util ──────────────────────────────────────────────────────────────

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

document.addEventListener("DOMContentLoaded", renderNavAuth);
