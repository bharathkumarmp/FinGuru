import {
  ArrowLeft,
  Lightbulb,
  TrendingUp,
  PiggyBank,
  ShieldCheck,
  Target,
  Sparkles,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

import "./Advice.css";

function Advice({ onBack, onNavigate }) {
  const recommendations = [
    {
      title: "Increase Monthly Savings",
      description:
        "You currently have a strong savings rate. Increasing your monthly savings by ₹5,000 can accelerate your financial goals.",
      impact: "High Impact",
      icon: PiggyBank,
      className: "green",
      question:
        "How can I increase my monthly savings by ₹5,000 based on my current financial situation?",
    },
    {
      title: "Build Emergency Fund",
      description:
        "Your emergency fund is healthy. Reaching a 6-month reserve would provide an additional layer of financial security.",
      impact: "Recommended",
      icon: ShieldCheck,
      className: "blue",
      question:
        "How should I build my emergency fund based on my current income, spending, and financial health?",
    },
    {
      title: "Invest Consistently",
      description:
        "Consider maintaining a regular investment contribution to build long-term wealth.",
      impact: "Long Term",
      icon: TrendingUp,
      className: "purple",
      question:
        "How much should I consider investing regularly based on my current financial situation?",
    },
    {
      title: "Stay on Goal",
      description:
        "Your financial goals are progressing well. Maintaining your current saving discipline can keep you on track.",
      impact: "On Track",
      icon: Target,
      className: "orange",
      question:
        "What should I do to stay on track with my financial goals based on my current finances?",
    },
  ];

  /*
   * Open FinGuru Copilot with a recommendation-specific question.
   *
   * App.jsx should provide:
   *
   * onNavigate("/copilot", {
   *   state: {
   *     initialQuestion: "..."
   *   }
   * })
   */
  const handleExploreRecommendation = (question) => {
    if (onNavigate) {
      onNavigate("/copilot", {
        state: {
          initialQuestion: question,
        },
      });

      return;
    }

    /*
     * Fallback if onNavigate is not supplied.
     * This keeps the button functional without
     * disturbing the existing application.
     */
    window.location.href = "/copilot";
  };

  return (
    <div className="advice-page">

      {/* ================= HEADER ================= */}

      <header className="advice-header">

        <button
          className="advice-back"
          onClick={onBack}
        >
          <ArrowLeft size={20} />
          Back to Dashboard
        </button>

        <div className="advice-brand">

          <div className="advice-logo">
            F
          </div>

          <div>
            <h2>FinGuru</h2>
            <span>AI Financial Advice</span>
          </div>

        </div>

      </header>


      {/* ================= MAIN ================= */}

      <main className="advice-container">

        {/* ================= TITLE ================= */}

        <section className="advice-title">

          <div>

            <span className="advice-label">
              PERSONALIZED AI GUIDANCE
            </span>

            <h1>
              Smart Advice for Your Money
            </h1>

            <p>
              FinGuru AI analyzes your financial behavior and
              provides personalized actions to help you save,
              grow, and protect your money.
            </p>

          </div>

          <div className="ai-status">
            <span className="ai-status-dot"></span>
            AI Analysis Complete
          </div>

        </section>


        {/* ================= AI HERO ================= */}

        <section className="advice-hero">

          <div className="hero-icon">
            <Sparkles size={30} />
          </div>

          <div className="hero-content">

            <span>
              FIN GURU AI
            </span>

            <h2>
              Here's what I recommend for you 🚀
            </h2>

            <p>
              Based on your current financial profile,
              your strongest opportunity is to increase
              savings while continuing your long-term
              investment strategy.
            </p>

          </div>

          <div className="hero-score">

            <span>
              FINANCIAL
            </span>

            <strong>
              78
            </strong>

            <small>
              Health Score
            </small>

          </div>

        </section>


        {/* ================= RECOMMENDATIONS ================= */}

        <section className="recommendation-section">

          <div className="section-header">

            <div>

              <span>
                PERSONALIZED RECOMMENDATIONS
              </span>

              <h2>
                Your Next Best Actions
              </h2>

            </div>

            <Lightbulb size={22} />

          </div>


          <div className="recommendation-grid">

            {recommendations.map((recommendation) => {

              const Icon = recommendation.icon;

              return (
                <div
                  className={`recommendation-card ${recommendation.className}`}
                  key={recommendation.title}
                >

                  <div className="recommendation-top">

                    <div className="recommendation-icon">
                      <Icon size={23} />
                    </div>

                    <span className="impact">
                      {recommendation.impact}
                    </span>

                  </div>

                  <h3>
                    {recommendation.title}
                  </h3>

                  <p>
                    {recommendation.description}
                  </p>

                  <button
                    className="recommendation-button"
                    onClick={() =>
                      handleExploreRecommendation(
                        recommendation.question
                      )
                    }
                  >
                    Explore Recommendation
                    <ArrowRight size={16} />
                  </button>

                </div>
              );

            })}

          </div>

        </section>


        {/* ================= MONTHLY PLAN ================= */}

        <section className="advice-lower">

          <div className="monthly-plan">

            <div className="plan-heading">

              <div>
                <span>
                  FIN GURU ACTION PLAN
                </span>

                <h2>
                  Your Monthly Financial Plan
                </h2>
              </div>

              <CheckCircle2 size={22} />

            </div>


            <div className="plan-list">

              <div className="plan-item">

                <div className="plan-number">
                  1
                </div>

                <div>
                  <strong>
                    Save ₹46,550
                  </strong>

                  <span>
                    Maintain your current monthly savings.
                  </span>
                </div>

                <CheckCircle2 size={18} />

              </div>


              <div className="plan-item">

                <div className="plan-number">
                  2
                </div>

                <div>
                  <strong>
                    Invest ₹10,000
                  </strong>

                  <span>
                    Continue consistent long-term investing.
                  </span>
                </div>

                <CheckCircle2 size={18} />

              </div>


              <div className="plan-item">

                <div className="plan-number">
                  3
                </div>

                <div>
                  <strong>
                    Keep expenses below ₹20,000
                  </strong>

                  <span>
                    Maintain your current spending discipline.
                  </span>
                </div>

                <CheckCircle2 size={18} />

              </div>

            </div>

          </div>


          {/* ================= SMART TIP ================= */}

          <div className="smart-tip">

            <div className="tip-icon">
              <Lightbulb size={26} />
            </div>

            <span>
              SMART MONEY TIP
            </span>

            <h2>
              Small improvements compound over time.
            </h2>

            <p>
              Saving an additional ₹5,000 every month could
              significantly improve your long-term financial
              position.
            </p>

            <div className="tip-highlight">

              <TrendingUp size={18} />

              <span>
                Build habits, not just balances.
              </span>

            </div>

          </div>

        </section>


        {/* ================= FOOTER ================= */}

        <footer className="advice-footer">

          <div>
            <Sparkles size={17} />
            <span>
              FinGuru AI Recommendation Engine
            </span>
          </div>

          <span>
            Personalized • Intelligent • Actionable
          </span>

        </footer>

      </main>

    </div>
  );
}

export default Advice;