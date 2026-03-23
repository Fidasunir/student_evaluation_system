// static/js/script.js

document.addEventListener("DOMContentLoaded", function () {

  // -------------------------------
  // Toast/Alert for AI-generated draft
  // -------------------------------
  const aiGenerated = document.getElementById("ai-generated-flag");
  if (aiGenerated && aiGenerated.value === "1") {
    // Show Bootstrap toast or simple alert
    if (typeof bootstrap !== "undefined") {
      const toastEl = document.createElement("div");
      toastEl.className = "toast align-items-center text-bg-success border-0 position-fixed bottom-0 end-0 m-3";
      toastEl.setAttribute("role", "alert");
      toastEl.innerHTML = `
        <div class="d-flex">
          <div class="toast-body">
            ✅ AI-generated questions saved in draft successfully!
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      `;
      document.body.appendChild(toastEl);
      const toast = new bootstrap.Toast(toastEl);
      toast.show();
    } else {
      alert("✅ AI-generated questions saved in draft successfully!");
    }
  }

  // -------------------------------
  // Optional: Auto-open modal if needed
  // -------------------------------
  const autoOpenModalId = document.getElementById("auto-open-modal-id");
  if (autoOpenModalId && autoOpenModalId.value) {
    const modalEl = document.getElementById(autoOpenModalId.value);
    if (modalEl) {
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    }
  }

});
