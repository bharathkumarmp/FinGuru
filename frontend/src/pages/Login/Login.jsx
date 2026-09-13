import { useState } from "react";
import {
  Phone,
  LockKeyhole,
  Eye,
  EyeOff,
  ShieldCheck,
} from "lucide-react";

import "./Login.css";
import { login } from "../../services/api";

function Login({ onLogin }) {
  const [showPassword, setShowPassword] = useState(false);
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    const cleanMobile = mobile.replace(/\D/g, "");

    // Validate mobile number
    if (cleanMobile.length !== 10) {
      setError(
        "Please enter a valid 10-digit mobile number."
      );
      return;
    }

    // Validate password
    if (!password.trim()) {
      setError("Please enter your password.");
      return;
    }

    try {
      setLoading(true);

      console.log("FinGuru login request:", {
        mobile: cleanMobile,
        backend: "http://127.0.0.1:8000",
      });

      // Call backend login API
      const data = await login(
        cleanMobile,
        password
      );

      console.log(
        "FinGuru login response:",
        data
      );

      // Make sure token exists
      if (!data?.access_token) {
        throw new Error(
          "Login succeeded but no access token was returned."
        );
      }

      // Store authentication information
      localStorage.setItem(
        "finguru_token",
        data.access_token
      );

      localStorage.setItem(
        "finguru_mobile",
        cleanMobile
      );

      console.log(
        "FinGuru authentication successful."
      );

      // Tell App.jsx that login succeeded
      if (typeof onLogin === "function") {
        onLogin();
      }
    } catch (err) {
      console.error(
        "FinGuru login error:",
        err
      );

      const message =
        err?.message || "";

      const lowerMessage =
        message.toLowerCase();

      // Backend connection error
      if (
        lowerMessage.includes(
          "unable to connect"
        ) ||
        lowerMessage.includes(
          "failed to fetch"
        ) ||
        lowerMessage.includes(
          "networkerror"
        )
      ) {
        setError(
          "Unable to connect to FinGuru backend. Make sure FastAPI is running on port 8000."
        );
      }

      // Authentication error
      else if (
        lowerMessage.includes(
          "invalid mobile"
        ) ||
        lowerMessage.includes(
          "invalid mobile number or password"
        ) ||
        lowerMessage.includes(
          "password"
        )
      ) {
        setError(
          "Invalid mobile number or password."
        );
      }

      // Other API errors
      else {
        setError(
          message ||
            "Login failed. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      {/* =========================================
          LEFT BRANDING SECTION
      ========================================== */}

      <section className="login-brand">

        <div className="brand-content">

          {/* LOGO */}
          <div className="brand-logo-large">
            F
          </div>

          {/* BRAND NAME */}
          <h1>FinGuru</h1>

          {/* TAGLINE */}
          <p className="brand-tagline">
            Your AI-powered financial
            intelligence copilot.
          </p>

          {/* FEATURES */}
          <div className="brand-features">

            <div className="brand-feature">
              <span>✓</span>

              <p>
                Understand your financial
                health
              </p>
            </div>

            <div className="brand-feature">
              <span>✓</span>

              <p>
                Get personalized financial
                recommendations
              </p>
            </div>

            <div className="brand-feature">
              <span>✓</span>

              <p>
                Detect suspicious financial
                activity
              </p>
            </div>

            <div className="brand-feature">
              <span>✓</span>

              <p>
                Make smarter financial
                decisions with AI
              </p>
            </div>

          </div>
        </div>

        {/* BRAND FOOTER */}
        <div className="brand-footer">

          <ShieldCheck size={16} />

          <span>
            Your financial data is protected
          </span>

        </div>

      </section>


      {/* =========================================
          LOGIN SECTION
      ========================================== */}

      <section className="login-section">

        <div className="login-card">

          {/* HEADER */}
          <div className="login-header">

            <h2>
              Welcome back
            </h2>

            <p>
              Sign in to continue to your
              FinGuru account.
            </p>

          </div>


          {/* =====================================
              LOGIN FORM
          ====================================== */}

          <form
            onSubmit={handleSubmit}
            className="login-form"
          >

            {/* ===================================
                MOBILE NUMBER
            ==================================== */}

            <div className="form-group">

              <label htmlFor="mobile">
                Mobile number
              </label>

              <div className="input-wrapper">

                <Phone size={18} />

                <span className="country-code">
                  +91
                </span>

                <input
                  id="mobile"
                  name="mobile"
                  type="tel"
                  inputMode="numeric"
                  autoComplete="tel"
                  maxLength={10}
                  placeholder="Enter mobile number"
                  value={mobile}
                  onChange={(e) => {

                    const value =
                      e.target.value
                        .replace(/\D/g, "")
                        .slice(0, 10);

                    setMobile(value);

                    // Clear error while typing
                    if (error) {
                      setError("");
                    }
                  }}
                  required
                />

              </div>

            </div>


            {/* ===================================
                PASSWORD
            ==================================== */}

            <div className="form-group">

              <div className="password-label">

                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-password"
                  onClick={() => {
                    console.log(
                      "Forgot password clicked"
                    );
                  }}
                >
                  Forgot password?
                </button>

              </div>


              <div className="input-wrapper">

                <LockKeyhole size={18} />

                <input
                  id="password"
                  name="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => {

                    setPassword(
                      e.target.value
                    );

                    // Clear error while typing
                    if (error) {
                      setError("");
                    }
                  }}
                  required
                />


                {/* PASSWORD VISIBILITY */}
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(
                      (previous) =>
                        !previous
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >

                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}

                </button>

              </div>

            </div>


            {/* ===================================
                REMEMBER ME
            ==================================== */}

            <div className="login-options">

              <label className="remember-me">

                <input
                  type="checkbox"
                  name="remember"
                />

                <span>
                  Remember me
                </span>

              </label>

            </div>


            {/* ===================================
                ERROR MESSAGE
            ==================================== */}

            {error && (
              <div
                className="login-error"
                role="alert"
              >
                {error}
              </div>
            )}


            {/* ===================================
                SIGN IN BUTTON
            ==================================== */}

            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >

              {loading
                ? "Signing in..."
                : "Sign in"}

            </button>

          </form>


          {/* =====================================
              SECURITY DIVIDER
          ====================================== */}

          <div className="login-divider">

            <span>
              Secure access
            </span>

          </div>


          {/* =====================================
              SECURITY MESSAGE
          ====================================== */}

          <div className="security-note">

            <ShieldCheck size={18} />

            <p>
              FinGuru uses secure authentication
              to protect your financial
              information.
            </p>

          </div>


          {/* =====================================
              CREATE ACCOUNT
          ====================================== */}

          <p className="login-footer">

            Don't have an account?{" "}

            <button
              type="button"
              onClick={() => {
                console.log(
                  "Create account clicked"
                );
              }}
            >
              Create account
            </button>

          </p>

        </div>

      </section>

    </div>
  );
}

export default Login;