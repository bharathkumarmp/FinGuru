import {
  ArrowRight,
  Bell,
  Brain,
  Calculator,
  ChevronDown,
  Languages,
  Lightbulb,
  LockKeyhole,
  Search,
  ShieldCheck,
  Sparkles,
  Target,
  User,
  Wallet,
  ArrowLeftRight,
  Activity,
  CreditCard,
  RefreshCw,
  TrendingUp,
  IndianRupee,
  PiggyBank,
  BarChart3,
} from "lucide-react";

import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import {
  getCustomer,
  getCustomerAccounts,
  getCustomerBalance,
  getCustomerTransactions,
  getFinancialHealth,
  getRecommendations,
} from "../../services/api";

import "./Dashboard.css";


function Dashboard({ onLogout }) {

  const navigate = useNavigate();
  const location = useLocation();

  // ==========================================================
  // BACKEND STATE
  // ==========================================================

  const [customer, setCustomer] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [balance, setBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [financialHealth, setFinancialHealth] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // ==========================================================
  // DEMO CUSTOMER
  // ==========================================================

  const customerId = 1;


  // ==========================================================
  // HELPERS
  // ==========================================================

  const getArray = (data, keys = []) => {

    if (Array.isArray(data)) {
      return data;
    }

    for (const key of keys) {
      if (Array.isArray(data?.[key])) {
        return data[key];
      }
    }

    return [];
  };


  const getBalance = (data) => {

    if (typeof data === "number") {
      return data;
    }

    if (typeof data === "string") {
      return data;
    }

    return (
      data?.balance ??
      data?.total_balance ??
      data?.available_balance ??
      data?.amount ??
      278500
    );
  };


  const getHealthScore = (data) => {

    if (typeof data === "number") {
      return data;
    }

    return (
      data?.score ??
      data?.health_score ??
      data?.financial_health_score ??
      78
    );
  };


  const formatMoney = (value) => {

    if (
      value === null ||
      value === undefined ||
      value === ""
    ) {
      return "₹0";
    }

    if (
      typeof value === "string" &&
      value.includes("₹")
    ) {
      return value;
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return String(value);
    }

    return `₹${number.toLocaleString("en-IN")}`;
  };


  // ==========================================================
  // LOAD BACKEND DATA
  // ==========================================================

  const loadDashboard = async () => {

    setLoading(true);
    setError("");

    try {

      const results = await Promise.allSettled([

        getCustomer(customerId),

        getCustomerAccounts(customerId),

        getCustomerBalance(customerId),

        getCustomerTransactions(customerId),

        getFinancialHealth(customerId),

        getRecommendations(customerId),

      ]);


      const [
        customerResult,
        accountsResult,
        balanceResult,
        transactionsResult,
        healthResult,
        recommendationResult,
      ] = results;


      // CUSTOMER

      if (
        customerResult.status === "fulfilled"
      ) {
        setCustomer(customerResult.value);
      }


      // ACCOUNTS

      if (
        accountsResult.status === "fulfilled"
      ) {

        setAccounts(
          getArray(
            accountsResult.value,
            [
              "accounts",
              "data",
              "items",
            ]
          )
        );

      }


      // BALANCE

      if (
        balanceResult.status === "fulfilled"
      ) {

        setBalance(
          balanceResult.value
        );

      }


      // TRANSACTIONS

      if (
        transactionsResult.status === "fulfilled"
      ) {

        setTransactions(
          getArray(
            transactionsResult.value,
            [
              "transactions",
              "data",
              "items",
            ]
          )
        );

      }


      // HEALTH

      if (
        healthResult.status === "fulfilled"
      ) {

        setFinancialHealth(
          healthResult.value
        );

      }


      // RECOMMENDATIONS

      if (
        recommendationResult.status === "fulfilled"
      ) {

        setRecommendations(
          getArray(
            recommendationResult.value,
            [
              "recommendations",
              "data",
              "items",
            ]
          )
        );

      }


      // PARTIAL FAILURE

      const failed = results.filter(
        (result) =>
          result.status === "rejected"
      );


      if (failed.length > 0) {

        console.warn(
          "Some FinGuru APIs are unavailable:",
          failed
        );

      }

    } catch (err) {

      console.error(
        "Dashboard error:",
        err
      );

      setError(
        err?.message ||
        "Unable to connect to backend"
      );

    } finally {

      setLoading(false);

    }
  };


  // ==========================================================
  // INITIAL LOAD
  // ==========================================================

  useEffect(() => {

    loadDashboard();

  }, []);


  // ==========================================================
  // DISPLAY DATA
  // ==========================================================

  const totalBalance =
    getBalance(balance);

  const healthScore =
    getHealthScore(
      financialHealth
    );


  const userName =
    customer?.name ||
    customer?.full_name ||
    customer?.customer_name ||
    "Bharath";


  const userMobile =
    customer?.mobile ||
    customer?.phone ||
    localStorage.getItem(
      "finguru_mobile"
    ) ||
    "9876543210";


  // ==========================================================
  // FEATURES
  // ==========================================================

  const features = [

    {
      title: "Money",
      description:
        "View accounts, balances, and manage your money",
      icon: Wallet,
      className: "money-card",
      color: "purple",
      path: "/money",
    },

    {
      title: "Financial Health",
      description:
        "Check your financial wellness score and insights",
      icon: Activity,
      className: "health-card",
      color: "green",
      path: "/financial-health",
    },

    {
      title: "Security",
      description:
        "Monitor fraud, alerts, and stay protected",
      icon: ShieldCheck,
      className: "security-card",
      color: "blue",
      path: "/security",
    },

    {
      title: "AI Advice",
      description:
        "Get personalized financial recommendations",
      icon: Lightbulb,
      className: "advice-card",
      color: "yellow",
      path: "/advice",
    },

    {
      title: "Loans",
      description:
        "Explore and simulate loan options",
      icon: CreditCard,
      className: "loans-card",
      color: "pink",
      path: "/loans",
    },

    {
      title: "AI Copilot",
      description:
        "Chat with FinGuru AI for expert guidance",
      icon: Brain,
      className: "copilot-card",
      color: "indigo",
      path: "/copilot",
    },

    {
      title: "Simulator",
      description:
        "Simulate future scenarios and plan better",
      icon: Calculator,
      className: "simulator-card",
      color: "cyan",
      path: "/simulator",
    },

    {
      title: "Transactions",
      description:
        "View and analyze your transactions",
      icon: ArrowLeftRight,
      className: "transactions-card",
      color: "sky",
      path: "/transactions",
    },

    {
      title: "Goals",
      description:
        "Set and track your financial goals",
      icon: Target,
      className: "goals-card",
      color: "orange",
      path: "/goals",
    },

    {
      title: "Language & Voice",
      description:
        "Choose your language and use voice commands",
      icon: Languages,
      className: "language-card",
      color: "violet",
      path: "/language",
    },

    {
      title: "Profile",
      description:
        "Manage your personal information",
      icon: User,
      className: "profile-card",
      color: "rose",
      path: "/profile",
    },

    {
      title: "Privacy",
      description:
        "Control your data and privacy settings",
      icon: LockKeyhole,
      className: "privacy-card",
      color: "teal",
      path: "/privacy",
    },

  ];


  // ==========================================================
  // NAVIGATION
  // ==========================================================

  const handleFeatureClick = (
    feature
  ) => {

    navigate(
      feature.path
    );

  };


  const handleProfile = () => {

    navigate("/profile");

  };


  const handleNotifications = () => {

    navigate("/security");

  };


  // ==========================================================
  // SEARCH → COPILOT
  // ==========================================================

  const handleSearch = (event) => {

    if (event.key !== "Enter") {
      return;
    }

    const query =
      event.target.value.trim();

    if (!query) {
      return;
    }

    navigate(
      "/copilot",
      {
        state: {
          query,
        },
      }
    );

  };


  // ==========================================================
  // LOGOUT
  // ==========================================================

  const handleLogout = () => {

    localStorage.removeItem(
      "finguru_token"
    );

    localStorage.removeItem(
      "finguru_mobile"
    );

    if (onLogout) {
      onLogout();
    }

  };


  // ==========================================================
  // COPILOT QUERY
  // ==========================================================

  const query =
    location.state?.query || "";


  // ==========================================================
  // RENDER
  // ==========================================================

  return (

    <div className="finguru-dashboard">


      {/* ====================================================
          HEADER
      ==================================================== */}

      <header className="dashboard-header">


        {/* LOGO */}

        <div className="brand-area">

          <div className="dashboard-brand-logo">
            F
          </div>

          <div className="brand-text">

            <h2>
              FinGuru
            </h2>

            <span>
              Your AI Banking Companion
            </span>

          </div>

        </div>


        {/* SEARCH */}

        <div className="dashboard-search">

          <Search
            size={19}
          />

          <input
            type="text"
            placeholder="Ask FinGuru anything..."
            onKeyDown={
              handleSearch
            }
            defaultValue={query}
          />

          <span className="search-hint">
            ENTER
          </span>

        </div>


        {/* ACTIONS */}

        <div className="header-actions">


          {/* CONNECTION */}

          <div className="connection-pill">

            <span
              className={`connection-dot ${
                loading
                  ? "loading"
                  : error
                    ? "offline"
                    : "online"
              }`}
            />

            <span>

              {loading
                ? "Connecting"
                : error
                  ? "Offline"
                  : "AI Online"}

            </span>

          </div>


          {/* REFRESH */}

          <button
            className="header-icon-button refresh-button"
            onClick={
              loadDashboard
            }
            disabled={loading}
            title="Refresh"
          >

            <RefreshCw
              size={18}
              className={
                loading
                  ? "spin"
                  : ""
              }
            />

          </button>


          {/* NOTIFICATION */}

          <button
            className="header-icon-button notification-button"
            onClick={
              handleNotifications
            }
            title="Security"
          >

            <Bell
              size={19}
            />

            <span className="notification-dot" />

          </button>


          {/* PROFILE */}

          <button
            className="profile-mini"
            onClick={
              handleProfile
            }
          >

            <div className="profile-avatar">
              BK
            </div>

            <div className="profile-info">

              <strong>
                {userName}
              </strong>

              <span>
                {userMobile}
              </span>

            </div>

            <ChevronDown
              size={17}
            />

          </button>

        </div>

      </header>


      {/* ====================================================
          MAIN
      ==================================================== */}

      <main className="dashboard-container">


        {/* ==================================================
            HERO
        ================================================== */}

        <section className="welcome-banner">


          <div className="hero-decoration hero-decoration-one" />

          <div className="hero-decoration hero-decoration-two" />

          <div className="hero-decoration hero-decoration-three" />


          {/* HERO CONTENT */}

          <div className="welcome-content">

            <div className="welcome-badge">

              <Sparkles
                size={13}
              />

              FINANCIAL WELLNESS

            </div>


            <h1>
              Welcome back,
              <br />
              <span>
                {userName}!
              </span>{" "}
              👋
            </h1>


            <p className="welcome-subtitle">
              Your AI-powered financial wellness
              dashboard is ready.
            </p>


            <p className="welcome-quote">
              “Smarter Banking. Brighter Tomorrow.”
            </p>


            <button
              className="hero-button"
              onClick={() =>
                navigate("/copilot")
              }
            >

              Ask FinGuru

              <ArrowRight
                size={17}
              />

            </button>

          </div>


          {/* AI ROBOT */}

          <div className="ai-character">

            <div className="robot-glow" />

            <div className="robot">

              <div className="robot-antenna">
                <span />
              </div>


              <div className="robot-head">

                <div className="robot-ear left" />
                <div className="robot-ear right" />

                <div className="robot-eye">
                  •
                </div>

                <div className="robot-eye">
                  •
                </div>

                <div className="robot-mouth">
                  ─
                </div>

              </div>


              <div className="robot-neck" />


              <div className="robot-body">

                <Sparkles
                  size={25}
                />

              </div>

            </div>


            <div className="ai-speech">

              <div className="speech-label">

                <span />

                FINGURU AI

              </div>

              <strong>
                I'm FinGuru 🤖
              </strong>

              <p>
                Your AI companion for a
                smarter financial future.
              </p>

            </div>

          </div>


          {/* HERO SIDE */}

          <div className="welcome-side">

            <div>
              <span>01</span>
              SAVE
            </div>

            <div>
              <span>02</span>
              PLAN
            </div>

            <div>
              <span>03</span>
              GROW
            </div>

            <div>
              <span>04</span>
              SECURE
            </div>

            <strong>
              TOGETHER
            </strong>

          </div>

        </section>


        {/* ==================================================
            SUMMARY
        ================================================== */}

        <section className="dashboard-stats">


          {/* BALANCE */}

          <div className="dashboard-stat-card balance-stat">

            <div className="stat-top">

              <div className="stat-icon purple">

                <IndianRupee
                  size={20}
                />

              </div>

              <span className="stat-label">
                TOTAL BALANCE
              </span>

            </div>


            <strong className="stat-value">

              {formatMoney(
                totalBalance
              )}

            </strong>


            <div className="stat-footer">

              <PiggyBank
                size={13}
              />

              <span>
                Across your accounts
              </span>

            </div>

          </div>


          {/* HEALTH */}

          <div className="dashboard-stat-card health-stat">

            <div className="stat-top">

              <div className="stat-icon green">

                <Activity
                  size={20}
                />

              </div>

              <span className="stat-label">
                FINANCIAL HEALTH
              </span>

            </div>


            <div className="score-row">

              <strong className="stat-value">
                {healthScore}
                <small>
                  /100
                </small>
              </strong>

              <span className="excellent-badge">
                {healthScore >= 75
                  ? "Excellent"
                  : "Improve"}
              </span>

            </div>


            <div className="progress-track">

              <div
                className="progress-fill green-fill"
                style={{
                  width: `${Math.min(
                    Number(healthScore) || 0,
                    100
                  )}%`,
                }}
              />

            </div>

          </div>


          {/* TRANSACTIONS */}

          <div className="dashboard-stat-card transaction-stat">

            <div className="stat-top">

              <div className="stat-icon blue">

                <ArrowLeftRight
                  size={20}
                />

              </div>

              <span className="stat-label">
                TRANSACTIONS
              </span>

            </div>


            <strong className="stat-value">
              {transactions.length}
            </strong>


            <div className="stat-footer blue-text">

              <BarChart3
                size={13}
              />

              <span>
                Backend records loaded
              </span>

            </div>

          </div>


          {/* AI */}

          <div className="dashboard-stat-card ai-stat">

            <div className="stat-top">

              <div className="stat-icon pink">

                <Sparkles
                  size={20}
                />

              </div>

              <span className="stat-label">
                AI INSIGHTS
              </span>

            </div>


            <strong className="stat-value">

              {recommendations.length > 0
                ? recommendations.length
                : "Ready"}

            </strong>


            <div className="stat-footer pink-text">

              <Sparkles
                size={13}
              />

              <span>
                Personalized for you
              </span>

            </div>

          </div>

        </section>


        {/* ==================================================
            BACKEND WARNING
        ================================================== */}

        {error && (

          <div className="backend-warning">

            <div className="warning-symbol">
              ⚠️
            </div>

            <div className="warning-text">

              <strong>
                Backend connection issue
              </strong>

              <span>
                {error}
              </span>

            </div>

            <button
              onClick={
                loadDashboard
              }
            >
              Retry
            </button>

          </div>

        )}


        {/* ==================================================
            AI INSIGHT
        ================================================== */}

        <section className="ai-insight-card">

          <div className="ai-insight-icon">

            <Sparkles
              size={25}
            />

          </div>


          <div className="ai-insight-content">

            <span>
              FINGURU AI INSIGHT
            </span>

            <h3>

              {recommendations.length > 0
                ? "Your personalized financial recommendations are ready."
                : "FinGuru is analyzing your financial profile."}

            </h3>

            <p>

              {healthScore >= 75

                ? "Your financial health is looking strong. Keep saving consistently and continue building toward your financial goals."

                : "FinGuru recommends reviewing your spending, savings, and financial goals to improve your financial wellness."}

            </p>

          </div>


          <button
            className="insight-button"
            onClick={() =>
              navigate("/advice")
            }
          >

            View Advice

            <ArrowRight
              size={17}
            />

          </button>

        </section>


        {/* ==================================================
            SECTION TITLE
        ================================================== */}

        <div className="section-heading">

          <div>

            <span>
              YOUR FINANCIAL TOOLKIT
            </span>

            <h2>
              Everything you need
            </h2>

          </div>

          <p>
            AI-powered tools designed around you
          </p>

        </div>


        {/* ==================================================
            FEATURE GRID
        ================================================== */}

        <section className="feature-grid">

          {features.map(
            (feature) => {

              const Icon =
                feature.icon;

              return (

                <button
                  key={feature.title}
                  className={`feature-card ${feature.className}`}
                  onClick={() =>
                    handleFeatureClick(
                      feature
                    )
                  }
                >


                  <div className="feature-number">
                    {String(
                      features.indexOf(
                        feature
                      ) + 1
                    ).padStart(2, "0")}
                  </div>


                  <div className="feature-icon">

                    <Icon
                      size={26}
                    />

                  </div>


                  <div className="feature-content">

                    <h2>
                      {feature.title}
                    </h2>

                    <p>
                      {feature.description}
                    </p>

                  </div>


                  <div className="feature-arrow">

                    <ArrowRight
                      size={19}
                    />

                  </div>

                </button>

              );

            }
          )}

        </section>


        {/* ==================================================
            INTELLIGENCE CARD
        ================================================== */}

        <section className="intelligence-card">

          <div className="intelligence-icon">

            <TrendingUp
              size={24}
            />

          </div>


          <div className="intelligence-content">

            <span>
              FINGURU INTELLIGENCE ENGINE
            </span>

            <strong>
              Your financial data is connected
            </strong>

            <p>
              FinGuru can analyze your accounts,
              transactions, financial health and
              recommendations.
            </p>

          </div>


          <div className="connected-pill">

            <span />

            Connected

          </div>

        </section>


        {/* ==================================================
            BOTTOM BANNER
        ================================================== */}

        <section className="bottom-banner">


          <div className="bottom-brand">

            <div className="bottom-logo">
              F
            </div>

            <div>

              <h3>
                Building a Financially Stronger Bharat 🇮🇳
              </h3>

              <p>
                Powered by AI. Designed for You.
              </p>

            </div>

          </div>


          <div className="bottom-links">

            <span>
              Financial Inclusion
            </span>

            <i />

            <span>
              Financial Wellness
            </span>

            <i />

            <span>
              A Safer Tomorrow
            </span>

          </div>

        </section>


        {/* ==================================================
            FOOTER
        ================================================== */}

        <footer className="dashboard-footer">

          <span>
            © 2026 FinGuru AI
          </span>

          <span>
            Secure • Intelligent • Personalized
          </span>

          <button
            onClick={
              handleLogout
            }
          >
            Logout
          </button>

        </footer>

      </main>

    </div>
  );
}


export default Dashboard;