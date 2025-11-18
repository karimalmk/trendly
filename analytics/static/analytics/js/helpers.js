// ============================================================
// FORMATTING HELPERS
// ============================================================

// -------------------- FORMAT USD --------------------
export function formatUSD(value) {
  if (value == null || isNaN(value)) return "";
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  });
}

// -------------------- FORMAT COMMA --------------------
export function formatComma(value, decimals = 2) {
  if (value == null || isNaN(value)) return "";
  return Number(value).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

// -------------------- FORMAT INTEGER WITH COMMAS --------------------
export function formatIntegerComma(value) {
  if (value == null || isNaN(value)) return "";
  return Math.round(value).toLocaleString("en-US");
}

// -------------------- FORMAT PERCENT --------------------
export function formatPercent(value, decimals = 2) {
  if (value == null || isNaN(value)) return "";
  return (value * 100).toFixed(decimals) + "%";
}