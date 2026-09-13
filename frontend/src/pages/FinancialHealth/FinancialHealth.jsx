import {
  ArrowLeft,
  HeartPulse,
  TrendingUp,
  Wallet,
  ShieldCheck,
  Target,
  Sparkles,
} from "lucide-react";

import "./FinancialHealth.css";

function FinancialHealth({ onBack }) {
  const score = 78;

  const metrics = [
    {
      title: "Savings Rate",
      value: "71.6%",
      status: "Excellent",
      icon: Wallet,
      className: "green",
    },
    {
      title: "Debt Health",
      value: "82%",
      status: "Healthy",
      icon: ShieldCheck,
      className: "blue",
    },
    {
      title: "Emergency Fund",
      value: "5.8 Months",
      status: "Good",
      icon: HeartPulse,
      className: "purple",
    },
    {
      title: "Goal Progress",
      value: "64%",
      status: "On Track",
      icon: Target,
      className: "orange",
    },
  ];

  return (
    <div className="health-page">
      <header className="health-header">
        <button className="health-back" onClick={onBack}>
          <ArrowLeft size={20} />
          Back to Dashboard
        </button>

        <div className="health-brand">
          <div className="health-logo">F</div>
          <div>
            <h2>FinGuru</h2>
            <span>Financial Health</span>
          </div>
        </div>
      </header>

      <main className="health-container">
        <section className="health-title">
          <div>
            <span className="health-label">FINANCIAL WELLNESS</span>
            <h1>Your Financial Health</h1>
            <p>
              Understand your financial position and discover opportunities
              to become financially stronger.
            </p>
          </div>

          <div className="health-date">
            Updated just now
          </div>
        </section>

        <section className="health-overview">
          <div className="score-card">
            <div className="score-header">
              <div>
                <span>FINANCIAL HEALTH SCORE</span>
                <h2>Excellent</h2>
              </div>

              <HeartPulse size={30} />
            </div>

            <div className="score-circle">
              <div>
                <strong>{score}</strong>
                <span>/ 100</span>
              </div>
            </div>

            <p>
              Your financial health is stronger than average. Keep building
              savings while maintaining responsible spending.
            </p>
          </div>

          <div className="health-insight">
            <div className="insight-icon">
              <Sparkles size={25} />
            </div>

            <div>
              <span>FIN GURU AI INSIGHT</span>
              <h3>You're doing well! 🚀</h3>
              <p>
                Your current savings rate is excellent. If you continue saving
                at this pace, you can reach your major financial goals faster.
              </p>
            </div>
          </div>
        </section>

        <section className="metrics-grid">
          {metrics.map((metric) => {
            const Icon = metric.icon;

            return (
              <div className={`health-metric ${metric.className}`} key={metric.title}>
                <div className="metric-icon">
                  <Icon size={23} />
                </div>

                <div className="metric-info">
                  <span>{metric.title}</span>
                  <strong>{metric.value}</strong>
                  <small>{metric.status}</small>
                </div>

                <TrendingUp className="metric-trend" size={20} />
              </div>
            );
          })}
        </section>

        <section className="health-breakdown">
          <div className="breakdown-card">
            <div className="section-heading">
              <div>
                <span>HEALTH BREAKDOWN</span>
                <h2>What's driving your score?</h2>
              </div>
            </div>

            <div className="progress-item">
              <div>
                <span>Savings</span>
                <strong>90%</strong>
              </div>
              <div className="progress-track">
                <div className="progress-fill savings-fill" style={{ width: "90%" }} />
              </div>
            </div>

            <div className="progress-item">
              <div>
                <span>Spending Control</span>
                <strong>84%</strong>
              </div>
              <div className="progress-track">
                <div className="progress-fill spending-fill" style={{ width: "84%" }} />
              </div>
            </div>

            <div className="progress-item">
              <div>
                <span>Debt Management</span>
                <strong>82%</strong>
              </div>
              <div className="progress-track">
                <div className="progress-fill debt-fill" style={{ width: "82%" }} />
              </div>
            </div>

            <div className="progress-item">
              <div>
                <span>Goal Planning</span>
                <strong>64%</strong>
              </div>
              <div className="progress-track">
                <div className="progress-fill goal-fill" style={{ width: "64%" }} />
              </div>
            </div>
          </div>

          <div className="action-card">
            <div className="action-icon">
              <Target size={27} />
            </div>

            <span>NEXT BEST ACTION</span>
            <h2>Grow your emergency fund</h2>

            <p>
              Increasing your emergency fund from 5.8 to 6 months of expenses
              will give you an additional layer of financial security.
            </p>

            <button>
              View Recommendation
              <TrendingUp size={18} />
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default FinancialHealth;