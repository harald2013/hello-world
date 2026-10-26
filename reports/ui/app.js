"use strict";
const form = document.querySelector("#report-form");
const submit = document.querySelector("#submit");
const refresh = document.querySelector("#refresh");
const status = document.querySelector("#status");
const result = document.querySelector("#result");
let reportId = null;
let busy = false;

async function request(path, options = {}) {
  const token = document.querySelector("#token").value.trim();
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(path, {
    ...options, headers, credentials: "omit", cache: "no-store",
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    if (response.status === 401) throw new Error("Bitte einen gültigen API-Schlüssel eingeben.");
    if (response.status === 422) throw new Error("Bitte 1 bis 1000 gültige Zahlen zwischen -1e12 und 1e12 eingeben.");
    throw new Error("Der Dienst ist gerade nicht erreichbar. Bitte später erneut versuchen.");
  }
  return response.json();
}

async function checkReport() {
  const report = await request(`/reports/${encodeURIComponent(reportId)}`);
  if (report.status === "completed") {
    status.textContent = "Dein Report ist fertig.";
    result.textContent = JSON.stringify(report.result, null, 2);
    result.hidden = false;
    refresh.hidden = true;
    return true;
  }
  if (["failed", "timed_out", "terminated", "canceled"].includes(report.status)) {
    status.textContent = "Der Report konnte nicht abgeschlossen werden. Du kannst einen neuen erstellen.";
    refresh.hidden = true;
    return true;
  }
  status.textContent = `Report ${reportId} wird verarbeitet …`;
  return false;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  const input = document.querySelector("#values").value.trim();
  const values = input ? input.split(/[,;\s]+/).filter(Boolean).map(Number) : [];
  if (!values.length || !values.every(Number.isFinite)) {
    status.textContent = "Bitte gültige Zahlen eingeben, zum Beispiel 10, 20, 30.";
    return;
  }
  busy = true;
  submit.disabled = true;
  refresh.disabled = true;
  refresh.hidden = true;
  result.hidden = true;
  result.textContent = "";
  reportId = null;
  status.textContent = "Report wird gestartet …";
  try {
    const job = await request("/reports", {
      method: "POST", body: JSON.stringify({ values, delay_seconds: 2 }),
    });
    reportId = job.id;
    // Only user-created reports are polled, and polling is bounded.
    for (let attempt = 0; attempt < 15; attempt++) {
      if (await checkReport()) return;
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }
    status.textContent = "Dein Report braucht noch etwas Zeit. Prüfe den Status später erneut.";
    refresh.hidden = false;
  } catch (error) {
    status.textContent = error instanceof TypeError || error.name === "TimeoutError"
      ? "Die Verbindung wurde unterbrochen. Ein gestarteter Report kann trotzdem weiterlaufen."
      : error.message;
    refresh.hidden = reportId === null;
  } finally {
    busy = false;
    submit.disabled = false;
    refresh.disabled = false;
  }
});

refresh.addEventListener("click", async () => {
  if (!reportId || busy) return;
  busy = true;
  submit.disabled = true;
  refresh.disabled = true;
  try { await checkReport(); }
  catch (error) { status.textContent = "Status konnte nicht geladen werden. Bitte erneut versuchen."; }
  finally { busy = false; submit.disabled = false; refresh.disabled = false; }
});
