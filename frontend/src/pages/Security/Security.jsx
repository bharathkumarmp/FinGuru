import {
  ArrowLeft,
  ShieldCheck,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  LockKeyhole,
  Smartphone,
  CreditCard,
  Activity,
  Eye,
  Clock3,
} from "lucide-react";

import "./Security.css";

function Security({ onBack }) {
  const securityScore = 92;

  const securityItems = [
    {
      title: "Account Protection",
      description: "Your account security settings are strong.",
      status: "Protected",
      icon: ShieldCheck,
      className: "protected",
    },
    {
      title: "Login Security",
      description: "No unusual login activity detected.",
      status: "Secure",
      icon: LockKeyhole,
      className: "secure",
    },
    {
      title: "Device Security",
      description: "Your registered devices are verified.",
      status: "Verified",
      icon: Smartphone,
      className: "verified",
    },
    {
      title: "Transaction Security",
      description: "Recent transactions appear normal.",
      status: "Monitoring",
      icon: CreditCard,
      className: "monitoring",
    },
  ];

  const transactions = [
    {
      merchant: "Amazon India",
      amount: "₹2,499",
      time: "Today, 10:42 AM",
      status: "Verified",
    },
    {
      merchant: "Swiggy",
      amount: "₹648",
      time: "Yesterday, 8:15 PM",
      status: "Verified",
    },
    {
      merchant: "Flipkart",
      amount: "₹3,299",
      time: "Yesterday, 2:31 PM",
      status: "Verified",
    },
  ];

  return (
    <div className="security-page">

      {/* ================= HEADER ================= */}

      <header className="security-header">
        <button
          className="security-back"
          onClick={onBack}
        >
          <ArrowLeft size={20} />
          Back to Dashboard
        </button>

        <div className="security-brand">
          <div className="security-logo">
            F
          </div>

          <div>
            <h2>FinGuru</h2>
            <span>Security Center</span>
          </div>
        </div>
      </header>


      {/* ================= MAIN ================= */}

      <main className="security-container">

        {/* ================= TITLE ================= */}

        <section className="security-title">
          <div>
            <span className="security-label">
              AI SECURITY CENTER
            </span>

            <h1>
              Your Money is Protected
            </h1>

            <p>
              FinGuru continuously analyzes your financial activity
              to help detect suspicious behavior and protect your money.
            </p>
          </div>

          <div className="security-status">
            <CheckCircle2 size={17} />
            System Secure
          </div>
        </section>


        {/* ================= SECURITY OVERVIEW ================= */}

        <section className="security-overview">

          <div className="security-score-card">

            <div className="security-score-top">
              <div>
                <span>
                  SECURITY SCORE
                </span>

                <h2>
                  Excellent
                </h2>
              </div>

              <ShieldCheck size={31} />
            </div>

            <div className="security-score">

              <div className="security-score-circle">

                <div>
                  <strong>
                    {securityScore}
                  </strong>

                  <span>
                    / 100
                  </span>
                </div>

              </div>

            </div>

            <div className="security-score-message">
              <CheckCircle2 size={18} />

              <span>
                No critical security threats detected.
              </span>
            </div>

          </div>


          {/* ================= AI MONITORING ================= */}

          <div className="ai-monitoring-card">

            <div className="monitoring-icon">
              <Activity size={27} />
            </div>

            <div className="monitoring-content">

              <span>
                FIN GURU AI MONITORING
              </span>

              <h2>
                Everything looks normal
              </h2>

              <p>
                Our AI security engine analyzed your recent
                account activity and found no significant
                signs of fraud or suspicious behavior.
              </p>

              <div className="monitoring-live">
                <span className="live-dot"></span>
                AI monitoring active
              </div>

            </div>

          </div>

        </section>


        {/* ================= SECURITY CARDS ================= */}

        <section className="security-grid">

          {securityItems.map((item) => {

            const Icon = item.icon;

            return (
              <div
                className={`security-item ${item.className}`}
                key={item.title}
              >

                <div className="security-item-icon">
                  <Icon size={24} />
                </div>

                <div className="security-item-content">

                  <h3>
                    {item.title}
                  </h3>

                  <p>
                    {item.description}
                  </p>

                  <span>
                    <CheckCircle2 size={14} />
                    {item.status}
                  </span>

                </div>

              </div>
            );

          })}

        </section>


        {/* ================= LOWER SECTION ================= */}

        <section className="security-lower">

          {/* Recent Transactions */}

          <div className="activity-card">

            <div className="activity-heading">

              <div>
                <span>
                  TRANSACTION MONITORING
                </span>

                <h2>
                  Recent Activity
                </h2>
              </div>

              <Eye size={21} />

            </div>


            <div className="transaction-list">

              {transactions.map((transaction) => (

                <div
                  className="transaction-row"
                  key={transaction.merchant}
                >

                  <div className="transaction-icon">
                    <CreditCard size={18} />
                  </div>

                  <div className="transaction-info">

                    <strong>
                      {transaction.merchant}
                    </strong>

                    <span>
                      <Clock3 size={12} />
                      {transaction.time}
                    </span>

                  </div>

                  <div className="transaction-right">

                    <strong>
                      {transaction.amount}
                    </strong>

                    <span>
                      <CheckCircle2 size={13} />
                      {transaction.status}
                    </span>

                  </div>

                </div>

              ))}

            </div>

          </div>


          {/* Security Alert */}

          <div className="security-alert-card">

            <div className="alert-icon">
              <ShieldAlert size={26} />
            </div>

            <span>
              STAY PROTECTED
            </span>

            <h2>
              Never share your OTP
            </h2>

            <p>
              FinGuru will never ask you to share your OTP,
              PIN, CVV, password, or complete card details.
            </p>

            <div className="security-warning">

              <AlertTriangle size={17} />

              <span>
                Report suspicious activity immediately.
              </span>

            </div>

          </div>

        </section>


        {/* ================= FOOTER ================= */}

        <footer className="security-footer">

          <div>
            <ShieldCheck size={18} />

            <span>
              FinGuru AI Security Engine
            </span>
          </div>

          <span>
            Secure • Intelligent • Always Monitoring
          </span>

        </footer>

      </main>

    </div>
  );
}

export default Security;