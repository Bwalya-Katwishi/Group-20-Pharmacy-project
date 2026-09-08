(function () {
  const scanInput = document.getElementById("code");
  const scanForm = document.getElementById("scan-form");
  const amountInput = document.getElementById("amount-tendered");
  const changeEl = document.getElementById("change-due");
  const methodSelect = document.getElementById("pay-method");
  const total = Number(window.POS_TOTAL || 0);
  const currency = window.POS_CURRENCY || "";

  if (scanInput) {
    scanInput.focus();
    scanInput.select();
  }

  if (scanForm && scanInput) {
    scanForm.addEventListener("submit", function () {
      if (!scanInput.value.trim()) {
        scanInput.focus();
      }
    });
  }

  function updateChange() {
    if (!amountInput || !changeEl) return;
    const method = methodSelect ? methodSelect.value : "CASH";
    const tendered = parseFloat(amountInput.value) || 0;
    if (method !== "CASH") {
      changeEl.textContent = currency + " 0.00";
      return;
    }
    const change = Math.max(0, tendered - total);
    changeEl.textContent = currency + " " + change.toFixed(2);
    changeEl.style.color = tendered < total ? "#b42318" : "";
  }

  if (amountInput) {
    amountInput.addEventListener("input", updateChange);
    if (methodSelect) methodSelect.addEventListener("change", updateChange);
    updateChange();
  }
})();
