import React, { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import Money from "./pages/Money/Money";
import FinancialHealth from "./pages/FinancialHealth/FinancialHealth";
import Security from "./pages/Security/Security";
import Advice from "./pages/Advice/Advice";
import Loans from "./pages/Loans/Loans";
import Copilot from "./pages/Copilot/Copilot";
import Simulator from "./pages/Simulator/Simulator";
import Transactions from "./pages/Transactions/Transactions";
import Goals from "./pages/Goals/Goals";
import Language from "./pages/Language/Language";
import Profile from "./pages/Profile/Profile";
import Privacy from "./pages/Privacy/Privacy";

// ============================================================
// DEMO USER
// ============================================================

const finguruUser = {
  id: 1,
  name: "Bharath Kumar",
  mobile: "9876543210",
  accountType: "Savings Account",
  role: "customer",
};

// ============================================================
// SHARED FINANCIAL DATA
// ============================================================

const finguruFinancialData = {
  accounts: {
    savings: 153500,
    creditCard: 25000,
    investments: 100000,
    totalBalance: 278500,
  },

  monthly: {
    income: 65000,
    expenses: 18450,
    savings: 46550,
  },

  financialHealth: {
    score: 78,
    savingsRate: 71.6,
    debtHealth: 82,
    emergencyFundMonths: 5.8,
    goalProgress: 64,
  },

  security: {
    score: 92,
    accountProtection: 95,
    loginSecurity: 90,
    deviceSecurity: 92,
    transactionSecurity: 91,
  },

  loans: {
    readinessScore: 82,
    recommendedMaxEmi: 20000,
  },

  goals: [
    {
      id: 1,
      name: "Emergency Fund",
      target: 150000,
      saved: 87000,
      deadline: "December 2026",
      category: "Safety",
    },
    {
      id: 2,
      name: "New Laptop",
      target: 90000,
      saved: 58500,
      deadline: "March 2027",
      category: "Personal",
    },
    {
      id: 3,
      name: "Vacation Fund",
      target: 100000,
      saved: 42000,
      deadline: "June 2027",
      category: "Lifestyle",
    },
    {
      id: 4,
      name: "Investment Corpus",
      target: 500000,
      saved: 180000,
      deadline: "December 2028",
      category: "Investment",
    },
  ],

  transactions: [
    {
      id: 1,
      name: "Salary Credit",
      amount: 65000,
      type: "income",
      category: "Salary",
    },
    {
      id: 2,
      name: "Amazon",
      amount: 2499,
      type: "expense",
      category: "Shopping",
    },
    {
      id: 3,
      name: "Swiggy",
      amount: 620,
      type: "expense",
      category: "Food",
    },
    {
      id: 4,
      name: "Uber",
      amount: 380,
      type: "expense",
      category: "Transport",
    },
    {
      id: 5,
      name: "Rent Payment",
      amount: 12000,
      type: "expense",
      category: "Housing",
    },
    {
      id: 6,
      name: "Jio",
      amount: 799,
      type: "expense",
      category: "Utilities",
    },
    {
      id: 7,
      name: "Flipkart",
      amount: 1899,
      type: "expense",
      category: "Shopping",
    },
    {
      id: 8,
      name: "Restaurant",
      amount: 1250,
      type: "expense",
      category: "Food",
    },
    {
      id: 9,
      name: "Metro Recharge",
      amount: 500,
      type: "expense",
      category: "Transport",
    },
    {
      id: 10,
      name: "Freelance Payment",
      amount: 8500,
      type: "income",
      category: "Freelance",
    },
  ],
};

// ============================================================
// PRIVACY SETTINGS
// ============================================================

const defaultPrivacySettings = {
  personalizedRecommendations: true,
  aiFinancialInsights: true,
  transactionAnalysis: true,
  financialNotifications: true,
};

// ============================================================
// PROTECTED ROUTE
// ============================================================

function ProtectedRoute({ loggedIn, children }) {
  if (!loggedIn) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// ============================================================
// APP
// ============================================================

function App() {
  const [loggedIn, setLoggedIn] = useState(() => {
    return Boolean(localStorage.getItem("finguru_token"));
  });

  const [privacySettings, setPrivacySettings] = useState(() => {
    const savedSettings = localStorage.getItem("finguru_privacy");

    if (savedSettings) {
      try {
        return JSON.parse(savedSettings);
      } catch (error) {
        console.error(
          "Unable to load privacy settings:",
          error
        );
      }
    }

    return defaultPrivacySettings;
  });

  // ==========================================================
  // LOGIN
  // ==========================================================

  const handleLogin = () => {
    setLoggedIn(true);
  };

  // ==========================================================
  // LOGOUT
  // ==========================================================

  const handleLogout = () => {
    localStorage.removeItem("finguru_token");
    localStorage.removeItem("finguru_mobile");

    setLoggedIn(false);
  };

  // ==========================================================
  // BACK
  // ==========================================================

  const handleBack = () => {
    window.history.back();
  };

  // ==========================================================
  // PRIVACY
  // ==========================================================

  const handlePrivacyChange = (newSettings) => {
    setPrivacySettings(newSettings);

    localStorage.setItem(
      "finguru_privacy",
      JSON.stringify(newSettings)
    );
  };

  // ==========================================================
  // ROUTES
  // ==========================================================

  return (
    <BrowserRouter>
      <Routes>

        {/* LOGIN */}

        <Route
          path="/login"
          element={
            loggedIn ? (
              <Navigate to="/" replace />
            ) : (
              <Login onLogin={handleLogin} />
            )
          }
        />

        {/* DASHBOARD */}

        <Route
          path="/"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Dashboard
                onLogout={handleLogout}
                user={finguruUser}
                financialData={finguruFinancialData}
                privacySettings={privacySettings}
              />
            </ProtectedRoute>
          }
        />

        {/* MONEY */}

        <Route
          path="/money"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Money
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* FINANCIAL HEALTH */}

        <Route
          path="/financial-health"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <FinancialHealth
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* SECURITY */}

        <Route
          path="/security"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Security
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* AI ADVICE */}

        <Route
          path="/advice"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Advice
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* LOANS */}

        <Route
          path="/loans"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Loans
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* AI COPILOT */}

        <Route
          path="/copilot"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Copilot
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* SIMULATOR */}

        <Route
          path="/simulator"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Simulator
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* TRANSACTIONS */}

        <Route
          path="/transactions"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Transactions
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* GOALS */}

        <Route
          path="/goals"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Goals
                onBack={handleBack}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* LANGUAGE & VOICE */}

        <Route
          path="/language"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Language
                onBack={handleBack}
                user={finguruUser}
              />
            </ProtectedRoute>
          }
        />

        {/* PROFILE */}

        <Route
          path="/profile"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Profile
                onBack={handleBack}
                onLogout={handleLogout}
                user={finguruUser}
                financialData={finguruFinancialData}
              />
            </ProtectedRoute>
          }
        />

        {/* PRIVACY */}

        <Route
          path="/privacy"
          element={
            <ProtectedRoute loggedIn={loggedIn}>
              <Privacy
                onBack={handleBack}
                user={finguruUser}
                privacySettings={privacySettings}
                onPrivacyChange={handlePrivacyChange}
              />
            </ProtectedRoute>
          }
        />

        {/* UNKNOWN ROUTE */}

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;