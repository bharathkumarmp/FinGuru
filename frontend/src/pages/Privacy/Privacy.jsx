import { useEffect, useState } from "react";
import {
  ShieldCheck,
  Lock,
  CheckCircle2,
  XCircle,
  RefreshCw,
  AlertCircle,
  Eye,
  Brain,
  Landmark,
  ShieldAlert,
} from "lucide-react";

import {
  getDataConsent,
  updateConsent,
} from "../../services/api";

import "./Privacy.css";

const CUSTOMER_ID = 1;

const CONSENT_OPTIONS = [
  {
    purpose: "financial_analysis",
    title: "Financial Analysis",
    description:
      "Allow FinGuru to analyze your income, spending, savings, and transaction patterns.",
    icon: Brain,
  },
  {
    purpose: "financial_advice",
    title: "Personalized Financial Advice",
    description:
      "Allow FinGuru to generate personalized financial insights and recommendations.",
    icon: Landmark,
  },
  {
    purpose: "loan_recommendation",
    title: "Loan Recommendations",
    description:
      "Allow FinGuru to evaluate loan suitability and provide responsible borrowing guidance.",
    icon: Landmark,
  },
  {
    purpose: "fraud_detection",
    title: "Fraud Detection",
    description:
      "Allow FinGuru to analyze transaction activity for suspicious or potentially fraudulent behavior.",
    icon: ShieldAlert,
  },
];

function normalizeConsentResponse(data) {
  if (!data) return [];

  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data.consents)) {
    return data.consents;
  }

  if (data.consent) {
    return [data.consent];
  }

  return [];
}

function isConsentGranted(records, purpose) {
  const record = records.find(
    (item) =>
      String(item?.purpose || "").toLowerCase() ===
      purpose.toLowerCase()
  );

  if (!record) return false;

  return (
    record.granted === true ||
    record.is_granted === true ||
    record.status === "granted"
  );
}

export default function Privacy() {
  const [consents, setConsents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [savingPurpose, setSavingPurpose] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function loadConsent() {
    try {
      setLoading(true);
      setError("");

      const data = await getDataConsent(CUSTOMER_ID);

      setConsents(normalizeConsentResponse(data));
    } catch (err) {
      console.error("Consent loading error:", err);
      setError(
        err.message ||
          "Unable to load your privacy preferences."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadConsent();
  }, []);

  async function handleToggle(purpose) {
    const currentlyGranted = isConsentGranted(
      consents,
      purpose
    );

    const newValue = !currentlyGranted;

    try {
      setSavingPurpose(purpose);
      setError("");
      setSuccess("");

      const result = await updateConsent(CUSTOMER_ID, {
        purpose,
        granted: newValue,
      });

      const returnedConsent = result?.consent;

      setConsents((previous) => {
        const filtered = previous.filter(
          (item) =>
            String(item?.purpose || "").toLowerCase() !==
            purpose.toLowerCase()
        );

        return returnedConsent
          ? [...filtered, returnedConsent]
          : [
              ...filtered,
              {
                purpose,
                granted: newValue,
              },
            ];
      });

      setSuccess(
        newValue
          ? "Consent granted successfully."
          : "Consent revoked successfully."
      );

      setTimeout(() => {
        setSuccess("");
      }, 3000);
    } catch (err) {
      console.error("Consent update error:", err);

      setError(
        err.message ||
          "Unable to update your consent preference."
      );
    } finally {
      setSavingPurpose(null);
    }
  }

  const grantedCount = CONSENT_OPTIONS.filter(
    (option) =>
      isConsentGranted(consents, option.purpose)
  ).length;

  const adviceEnabled = isConsentGranted(
    consents,
    "financial_advice"
  );

  return (
    <div className="privacy-page">
      {/* =====================================================
          HEADER
      ===================================================== */}

      <section className="privacy-header">
        <div className="privacy-header-content">
          <div className="privacy-title-row">
            <div className="privacy-icon">
              <ShieldCheck size={30} />
            </div>

            <div>
              <p className="privacy-eyebrow">
                FIN GURU SECURITY
              </p>

              <h1>
                Privacy &amp; Consent
              </h1>

              <p className="privacy-subtitle">
                You control how FinGuru uses your financial
                information.
              </p>
            </div>
          </div>

          <button
            className="refresh-button"
            onClick={loadConsent}
            disabled={loading}
          >
            <RefreshCw
              size={17}
              className={loading ? "spin" : ""}
            />

            Refresh
          </button>
        </div>
      </section>

      {/* =====================================================
          STATUS BANNER
      ===================================================== */}

      <section className="privacy-status-card">
        <div className="status-icon">
          <Lock size={25} />
        </div>

        <div className="status-content">
          <h2>
            Your data, your control
          </h2>

          <p>
            FinGuru only uses data for the purposes you
            explicitly authorize. You can change these
            permissions at any time.
          </p>
        </div>

        <div className="consent-counter">
          <strong>
            {grantedCount}/{CONSENT_OPTIONS.length}
          </strong>

          <span>
            permissions enabled
          </span>
        </div>
      </section>

      {/* =====================================================
          ALERTS
      ===================================================== */}

      {error && (
        <div className="privacy-alert error">
          <AlertCircle size={20} />

          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="privacy-alert success">
          <CheckCircle2 size={20} />

          <span>{success}</span>
        </div>
      )}

      {/* =====================================================
          CONSENT CARDS
      ===================================================== */}

      <section className="consent-section">
        <div className="section-heading">
          <div>
            <p className="section-eyebrow">
              PERMISSIONS
            </p>

            <h2>
              Choose what FinGuru can do
            </h2>

            <p>
              These controls determine which financial
              intelligence features are allowed to use your
              data.
            </p>
          </div>
        </div>

        <div className="consent-grid">
          {CONSENT_OPTIONS.map((option) => {
            const Icon = option.icon;

            const granted = isConsentGranted(
              consents,
              option.purpose
            );

            const saving =
              savingPurpose === option.purpose;

            return (
              <article
                className={`consent-card ${
                  granted ? "granted" : "disabled"
                }`}
                key={option.purpose}
              >
                <div className="consent-card-top">
                  <div className="consent-card-icon">
                    <Icon size={23} />
                  </div>

                  <div
                    className={`consent-status ${
                      granted
                        ? "active"
                        : "inactive"
                    }`}
                  >
                    {granted ? (
                      <>
                        <CheckCircle2 size={15} />
                        Enabled
                      </>
                    ) : (
                      <>
                        <XCircle size={15} />
                        Disabled
                      </>
                    )}
                  </div>
                </div>

                <h3>{option.title}</h3>

                <p>
                  {option.description}
                </p>

                <div className="consent-card-footer">
                  <span>
                    {granted
                      ? "Permission granted"
                      : "Permission required"}
                  </span>

                  <button
                    className={`toggle ${
                      granted ? "on" : ""
                    }`}
                    onClick={() =>
                      handleToggle(option.purpose)
                    }
                    disabled={saving || loading}
                    aria-label={`${
                      granted ? "Revoke" : "Grant"
                    } ${option.title}`}
                  >
                    <span className="toggle-knob">
                      {saving && (
                        <RefreshCw
                          size={11}
                          className="spin"
                        />
                      )}
                    </span>
                  </button>
                </div>
              </article>
            );
          })}
        </div>
      </section>

      {/* =====================================================
          AI RESPONSIBILITY
      ===================================================== */}

      <section className="privacy-principles">
        <div className="principles-header">
          <div className="principles-icon">
            <Eye size={24} />
          </div>

          <div>
            <h2>
              Responsible AI by design
            </h2>

            <p>
              FinGuru separates intelligence from
              decision enforcement.
            </p>
          </div>
        </div>

        <div className="principles-grid">
          <div>
            <strong>
              ML decides numbers
            </strong>

            <span>
              Financial health and affordability scores
              are calculated from structured financial data.
            </span>
          </div>

          <div>
            <strong>
              Agents reason
            </strong>

            <span>
              AI agents interpret financial signals and
              help explain possible actions.
            </span>
          </div>

          <div>
            <strong>
              Policy enforces
            </strong>

            <span>
              Consent, affordability, confidence, bias,
              and compliance checks can block unsafe actions.
            </span>
          </div>

          <div>
            <strong>
              LLM communicates
            </strong>

            <span>
              The final financial guidance is presented in
              clear, human-friendly language.
            </span>
          </div>
        </div>
      </section>

      {/* =====================================================
          ADVICE STATUS
      ===================================================== */}

      <section
        className={`advice-access ${
          adviceEnabled ? "enabled" : "blocked"
        }`}
      >
        {adviceEnabled ? (
          <>
            <CheckCircle2 size={23} />

            <div>
              <strong>
                Personalized financial advice is enabled
              </strong>

              <span>
                FinGuru can now use your authorized
                financial information for advice.
              </span>
            </div>
          </>
        ) : (
          <>
            <Lock size={23} />

            <div>
              <strong>
                Personalized financial advice is disabled
              </strong>

              <span>
                Grant Financial Advice permission above
                to unlock personalized recommendations.
              </span>
            </div>
          </>
        )}
      </section>
    </div>
  );
}