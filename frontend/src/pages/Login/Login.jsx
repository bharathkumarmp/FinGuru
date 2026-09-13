import { useState } from "react";
import { Eye, EyeOff, LockKeyhole, Phone, ShieldCheck } from "lucide-react";
import { login } from "../../services/api";
import "./Login.css";

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

    if (cleanMobile.length !== 10) {
      setError("Please enter a valid 10-digit mobile number.");
      return;
    }

    try {
      setLoading(true);

      const data = await login(cleanMobile, password);

      localStorage.setItem("finguru_token", data.access_token);
      localStorage.setItem("finguru_mobile", cleanMobile);

      onLogin();
    } catch (err) {
      setError(err.message || "Invalid mobile number or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      {/* LEFT BRANDING SECTION */}

      <section className="login-brand">

        <div className="brand-content">

          <div className="brand-logo-large">
            F
          </div>

          <h1>FinGuru</h1>

          <p className="brand-tagline">
            Your AI-powered financial intelligence copilot.
          </p>

          <div className="brand-features">

            <div className="brand-feature">
              <span>✓</span>
              <p>Understand your financial health</p>
            </div>

            <div className="brand-feature">
              <span>✓</span>
              <p>Get personalized financial recommendations</p>
            </div>

            <div className="brand-feature">
              <span>✓</span>
              <p>Detect suspicious financial activity</p>
            </div>

            <div className="brand-feature">
              <span>✓</span>
              <p>Make smarter financial decisions with AI</p>
            </div>

          </div>

        </div>

        <div className="brand-footer">
          <ShieldCheck size={16} />
          <span>Your financial data is protected</span>
        </div>

      </section>


      {/* LOGIN SECTION */}

      <section className="login-section">

        <div className="login-card">

          <div className="login-header">

            <h2>Welcome back</h2>

            <p>
              Sign in to continue to your FinGuru account.
            </p>

          </div>


          <form
            onSubmit={handleSubmit}
            className="login-form"
          >

            {/* MOBILE NUMBER */}

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
                  type="tel"
                  inputMode="numeric"
                  maxLength={10}
                  placeholder="9876543210"
                  value={mobile}
                  onChange={(e) => {
                    const value = e.target.value
                      .replace(/\D/g, "")
                      .slice(0, 10);

                    setMobile(value);
                  }}
                  required
                />

              </div>

            </div>


            {/* PASSWORD */}

            <div className="form-group">

              <div className="password-label">

                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-password"
                  onClick={() =>
                    console.log("Forgot password")
                  }
                >
                  Forgot password?
                </button>

              </div>


              <div className="input-wrapper">

                <LockKeyhole size={18} />

                <input
                  id="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
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


            {/* REMEMBER ME */}

            <div className="login-options">

              <label className="remember-me">

                <input
                  type="checkbox"
                />

                <span>
                  Remember me
                </span>

              </label>

            </div>


            {/* ERROR */}

            {error && (
              <div className="login-error">
                {error}
              </div>
            )}


            {/* SUBMIT */}

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


          {/* SECURITY */}

          <div className="login-divider">
            <span>
              Secure access
            </span>
          </div>


          <div className="security-note">

            <ShieldCheck size={18} />

            <p>
              FinGuru uses secure authentication
              to protect your financial information.
            </p>

          </div>


          {/* CREATE ACCOUNT */}

          <p className="login-footer">

            Don't have an account?{" "}

            <button
              type="button"
              onClick={() =>
                console.log("Create account")
              }
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