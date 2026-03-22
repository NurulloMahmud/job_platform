let allJobs = [];
let jobMap  = {};   // id → job object, for quick modal lookup

async function fetchJobs() {
  try {
    const res = await fetch("/jobs/");
    if (!res.ok) throw new Error("Failed to fetch");
    allJobs = await res.json();
    allJobs.forEach(j => { jobMap[j.id] = j; });
    renderJobs(allJobs);
  } catch (e) {
    document.getElementById("loading-state").classList.add("hidden");
    document.getElementById("error-state").classList.remove("hidden");
    document.getElementById("job-count").textContent = "Could not load jobs";
  }
}

function renderJobs(jobs) {
  document.getElementById("loading-state").classList.add("hidden");

  const grid  = document.getElementById("jobs-grid");
  const empty = document.getElementById("empty-state");
  const count = document.getElementById("job-count");

  if (jobs.length === 0) {
    grid.classList.add("hidden");
    empty.classList.remove("hidden");
    count.textContent = "No jobs match your search";
    return;
  }

  empty.classList.add("hidden");
  grid.classList.remove("hidden");
  count.textContent = `${jobs.length} open position${jobs.length !== 1 ? "s" : ""} available`;

  grid.innerHTML = jobs.map(job => `
    <div class="job-card bg-white rounded-2xl shadow-sm p-6 flex flex-col gap-4 border border-gray-100">
      <div>
        <div class="flex items-center gap-2 mb-2">
          <span class="w-9 h-9 rounded-lg bg-indigo-100 text-indigo-700 font-bold text-sm flex items-center justify-center uppercase">
            ${job.company.name.charAt(0)}
          </span>
          <span class="text-sm text-gray-500 font-medium">${escapeHtml(job.company.name)}</span>
        </div>
        <h2 class="text-lg font-bold text-gray-800 leading-snug">${escapeHtml(job.title)}</h2>
        <p class="text-sm text-gray-500 mt-1">${escapeHtml(job.position)}</p>
      </div>
      <div class="flex items-center gap-2 mt-auto">
        <span class="salary-badge text-xs font-semibold px-3 py-1 rounded-full">
          $${formatSalary(job.salary)} / yr
        </span>
      </div>
      <button
        class="block w-full text-center bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold py-2.5 rounded-xl transition"
        onclick="handleApply(event, ${job.id})"
      >Apply Now</button>
    </div>
  `).join("");
}

function filterJobs() {
  const query = document.getElementById("search-input").value.trim().toLowerCase();
  const filtered = query
    ? allJobs.filter(j =>
        j.title.toLowerCase().includes(query) ||
        j.position.toLowerCase().includes(query) ||
        j.company.name.toLowerCase().includes(query))
    : allJobs;
  renderJobs(filtered);
}

// ── Apply flow ────────────────────────────────────────────────────────────────

function handleApply(e, jobId) {
  e.preventDefault();
  const token = getToken();
  if (!token || !isTokenValid(token)) {
    window.location.href = "/login?next=" + encodeURIComponent("/");
    return;
  }
  openApplyModal(jobMap[jobId]);
}

function openApplyModal(job) {
  document.getElementById("modal-job-title").textContent    = job.title;
  document.getElementById("modal-job-company").textContent  = job.company.name;
  document.getElementById("modal-job-position").textContent = job.position;
  document.getElementById("modal-job-salary").textContent   = "$" + formatSalary(job.salary) + " / yr";
  document.getElementById("modal-message").value            = "";
  document.getElementById("modal-error").classList.add("hidden");
  document.getElementById("modal-success").classList.add("hidden");
  document.getElementById("modal-submit-btn").disabled      = false;
  document.getElementById("modal-submit-btn").textContent   = "Submit Application";
  document.getElementById("apply-modal").dataset.jobId      = job.id;
  document.getElementById("apply-modal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closeApplyModal() {
  document.getElementById("apply-modal").classList.add("hidden");
  document.body.style.overflow = "";
}

async function submitApply() {
  const modal   = document.getElementById("apply-modal");
  const jobId   = modal.dataset.jobId;
  const message = document.getElementById("modal-message").value.trim();
  const btn     = document.getElementById("modal-submit-btn");
  const errEl   = document.getElementById("modal-error");
  const okEl    = document.getElementById("modal-success");

  if (!message) {
    errEl.textContent = "Please write a cover letter.";
    errEl.classList.remove("hidden");
    return;
  }

  btn.disabled    = true;
  btn.textContent = "Submitting…";
  errEl.classList.add("hidden");

  try {
    const res = await fetch(`/jobs/${jobId}/apply`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({ message }),
    });

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.detail || "Could not submit application");
    }

    btn.classList.add("hidden");
    okEl.textContent = "Application submitted! Good luck 🎉";
    okEl.classList.remove("hidden");
    setTimeout(closeApplyModal, 2000);

  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove("hidden");
    btn.disabled    = false;
    btn.textContent = "Submit Application";
  }
}

// ── Utils ─────────────────────────────────────────────────────────────────────

function formatSalary(salary) {
  return Number(salary).toLocaleString("en-US");
}

document.addEventListener("DOMContentLoaded", () => {
  fetchJobs();
  document.getElementById("search-input").addEventListener("keyup", filterJobs);
});
