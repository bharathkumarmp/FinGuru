// frontend/src/services/api.js

const API_BASE_URL = "http://127.0.0.1:8000";

/* =========================================================
   GENERIC API REQUEST
========================================================= */

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("finguru_token");

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  // Attach authentication token when available
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  let response;

  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });
  } catch (error) {
    console.error("FinGuru API connection error:", error);

    throw new Error(
      "Unable to connect to FinGuru backend. Make sure FastAPI is running on port 8000."
    );
  }

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      data?.error ||
      `Request failed with status ${response.status}`;

    throw new Error(
      typeof errorMessage === "string"
        ? errorMessage
        : JSON.stringify(errorMessage)
    );
  }

  return data;
}

/* =========================================================
   AUTHENTICATION
========================================================= */

export async function login(mobile, password) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({
      mobile,
      password,
    }),
  });

  if (data?.access_token) {
    localStorage.setItem("finguru_token", data.access_token);
  }

  if (mobile) {
    localStorage.setItem("finguru_mobile", mobile);
  }

  return data;
}

export async function getCurrentUser() {
  return apiRequest("/auth/me");
}

export function logout() {
  localStorage.removeItem("finguru_token");
  localStorage.removeItem("finguru_mobile");
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem("finguru_token"));
}

/* =========================================================
   CUSTOMER
========================================================= */

export async function getCustomer(customerId = 1) {
  return apiRequest(`/customers/${customerId}`);
}

/* =========================================================
   ACCOUNTS
========================================================= */

export async function getCustomerAccounts(customerId = 1) {
  return apiRequest(`/accounts/customer/${customerId}`);
}

export async function getCustomerBalance(customerId = 1) {
  return apiRequest(`/accounts/customer/${customerId}/balance`);
}

export async function getAccount(accountId) {
  return apiRequest(`/accounts/${accountId}`);
}

export async function getAccountBalance(accountId) {
  return apiRequest(`/accounts/${accountId}/balance`);
}

/* =========================================================
   TRANSACTIONS
========================================================= */

export async function getCustomerTransactions(customerId = 1) {
  return apiRequest(`/transactions/customer/${customerId}`);
}

export async function getTransaction(transactionId) {
  return apiRequest(`/transactions/${transactionId}`);
}

export async function createTransaction(transactionData) {
  return apiRequest("/transactions", {
    method: "POST",
    body: JSON.stringify(transactionData),
  });
}

/* =========================================================
   FINANCIAL HEALTH
========================================================= */

export async function getFinancialHealth(customerId = 1) {
  return apiRequest(
    `/customers/${customerId}/financial-health`
  );
}

export async function getLatestFinancialHealth(customerId = 1) {
  return apiRequest(
    `/customers/${customerId}/financial-health/latest`
  );
}

/* =========================================================
   FINANCIAL STRESS
========================================================= */

export async function getFinancialStress(customerId = 1) {
  return apiRequest(
    `/customers/${customerId}/financial-stress`
  );
}

export async function getLatestFinancialStress(customerId = 1) {
  return apiRequest(
    `/customers/${customerId}/financial-stress/latest`
  );
}

/* =========================================================
   RECOMMENDATIONS
========================================================= */

export async function getRecommendations(customerId = 1) {
  return apiRequest(
    `/recommendations/${customerId}`
  );
}

/* =========================================================
   OFFERS
========================================================= */

export async function getOffers(customerId = 1) {
  return apiRequest(
    `/offers/${customerId}`
  );
}

/* =========================================================
   LOAN SIMULATION
========================================================= */

export async function simulateLoan(loanData) {
  return apiRequest("/loan/simulate", {
    method: "POST",
    body: JSON.stringify(loanData),
  });
}

/* =========================================================
   CONSENT / PRIVACY
========================================================= */

export async function getDataConsent(customerId = 1) {
  return apiRequest(
    `/customers/${customerId}/data-consent`
  );
}

export async function updateConsent(
  customerId = 1,
  consentData
) {
  return apiRequest(
    `/customers/${customerId}/consent`,
    {
      method: "POST",
      body: JSON.stringify(consentData),
    }
  );
}

export async function grantFinancialAdviceConsent(
  customerId = 1
) {
  return updateConsent(customerId, {
    purpose: "financial_advice",
    granted: true,
  });
}

export async function revokeFinancialAdviceConsent(
  customerId = 1
) {
  return updateConsent(customerId, {
    purpose: "financial_advice",
    granted: false,
  });
}

export async function grantFinancialAnalysisConsent(
  customerId = 1
) {
  return updateConsent(customerId, {
    purpose: "financial_analysis",
    granted: true,
  });
}

export async function grantLoanRecommendationConsent(
  customerId = 1
) {
  return updateConsent(customerId, {
    purpose: "loan_recommendation",
    granted: true,
  });
}

export async function grantFraudDetectionConsent(
  customerId = 1
) {
  return updateConsent(customerId, {
    purpose: "fraud_detection",
    granted: true,
  });
}

/* =========================================================
   SECURITY / INCIDENTS
========================================================= */

export async function getIncidents() {
  return apiRequest("/incidents");
}

export async function getIncident(incidentId) {
  return apiRequest(`/incidents/${incidentId}`);
}

/* =========================================================
   GENERIC AI
========================================================= */

export async function aiRequest(
  endpoint,
  payload = {}
) {
  return apiRequest(endpoint, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/* =========================================================
   AI COPILOT
========================================================= */

/*
 * Backend:
 * POST /copilot/chat
 *
 * Usage:
 *
 * copilotRequest({
 *   customer_id: 1,
 *   message: "How much did I spend?",
 *   language: "English",
 *   use_customer_context: true
 * });
 */

export async function copilotRequest(payload = {}) {
  return apiRequest("/copilot/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/* =========================================================
   HEALTH CHECK
========================================================= */

export async function healthCheck() {
  return apiRequest("/");
}

export async function checkBackendHealth() {
  return apiRequest("/health");
}

/* =========================================================
   API BASE URL
========================================================= */

export { API_BASE_URL };