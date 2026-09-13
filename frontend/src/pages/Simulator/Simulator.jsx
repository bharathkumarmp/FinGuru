import { useMemo, useState } from "react";
import {
  ArrowLeft,
  Calculator,
  CheckCircle2,
  IndianRupee,
  PiggyBank,
  Sparkles,
  Target,
  TrendingUp,
} from "lucide-react";

import "./Simulator.css";

function Simulator({ onBack }) {
  const [monthlyInvestment, setMonthlyInvestment] = useState(5000);
  const [investmentYears, setInvestmentYears] = useState(10);
  const [returnRate, setReturnRate] = useState(10);

  const [monthlySaving, setMonthlySaving] = useState(10000);
  const [savingYears, setSavingYears] = useState(5);

  // ============================================================
  // INVESTMENT CALCULATION
  // ============================================================

  const investmentResult = useMemo(() => {
    const monthlyRate = returnRate / 100 / 12;
    const months = investmentYears * 12;

    if (
      monthlyInvestment <= 0 ||
      monthlyRate <= 0 ||
      months <= 0
    ) {
      return {
        invested: 0,
        returns: 0,
        total: 0,
      };
    }

    const total =
      monthlyInvestment *
      ((Math.pow(1 + monthlyRate, months) - 1) /
        monthlyRate) *
      (1 + monthlyRate);

    const invested = monthlyInvestment * months;

    return {
      invested: Math.round(invested),
      returns: Math.round(total - invested),
      total: Math.round(total),
    };
  }, [
    monthlyInvestment,
    investmentYears,
    returnRate,
  ]);

  // ============================================================
  // SAVINGS CALCULATION
  // ============================================================

  const savingsResult = useMemo(() => {
    const months = savingYears * 12;
    const total = monthlySaving * months;

    return {
      months,
      total,
    };
  }, [monthlySaving, savingYears]);

  // ============================================================
  // FORMAT
  // ============================================================

  const formatCurrency = (value) =>
    `₹${Number(value).toLocaleString("en-IN")}`;

  // ============================================================
  // UI
  // ============================================================

  return (
    <div className="simulator-page">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="simulator-header">

        <button
          className="simulator-back-btn"
          onClick={onBack}
        >
          <ArrowLeft size={19} />
          Back
        </button>

        <div className="simulator-brand">

          <div className="simulator-logo">
            F
          </div>

          <div>
            <h2>FinGuru</h2>
            <span>Financial Simulator</span>
          </div>

        </div>

        <div className="simulator-status">
          <Sparkles size={15} />
          AI Powered
        </div>

      </header>

      <main className="simulator-container">

        {/* ====================================================
            HERO
        ==================================================== */}

        <section className="simulator-hero">

          <div className="simulator-hero-icon">
            <Calculator size={29} />
          </div>

          <div>

            <span className="simulator-eyebrow">
              FINANCIAL SCENARIO PLANNER
            </span>

            <h1>
              See your financial future.
            </h1>

            <p>
              Change your savings and investment assumptions
              to understand how today's decisions could affect
              your future.
            </p>

          </div>

        </section>

        {/* ====================================================
            INVESTMENT SIMULATOR
        ==================================================== */}

        <section className="simulator-card">

          <div className="simulator-card-header">

            <div>

              <span className="card-label">
                <TrendingUp size={14} />
                INVESTMENT SIMULATOR
              </span>

              <h2>
                What could your investment become?
              </h2>

              <p>
                Simulate a monthly investment over time.
              </p>

            </div>

            <div className="simulator-card-icon">
              <TrendingUp size={23} />
            </div>

          </div>

          <div className="simulator-grid">

            {/* INPUTS */}

            <div className="simulator-inputs">

              {/* MONTHLY INVESTMENT */}

              <div className="simulator-input-group">

                <div className="simulator-label-row">

                  <label>
                    Monthly Investment
                  </label>

                  <strong>
                    {formatCurrency(monthlyInvestment)}
                  </strong>

                </div>

                <input
                  type="range"
                  min="500"
                  max="100000"
                  step="500"
                  value={monthlyInvestment}
                  onChange={(event) =>
                    setMonthlyInvestment(
                      Number(event.target.value)
                    )
                  }
                />

                <div className="range-values">
                  <span>₹500</span>
                  <span>₹1L</span>
                </div>

              </div>

              {/* YEARS */}

              <div className="simulator-input-group">

                <div className="simulator-label-row">

                  <label>
                    Investment Period
                  </label>

                  <strong>
                    {investmentYears} Years
                  </strong>

                </div>

                <input
                  type="range"
                  min="1"
                  max="30"
                  step="1"
                  value={investmentYears}
                  onChange={(event) =>
                    setInvestmentYears(
                      Number(event.target.value)
                    )
                  }
                />

                <div className="range-values">
                  <span>1 Year</span>
                  <span>30 Years</span>
                </div>

              </div>

              {/* RETURN */}

              <div className="simulator-input-group">

                <div className="simulator-label-row">

                  <label>
                    Expected Annual Return
                  </label>

                  <strong>
                    {returnRate}%
                  </strong>

                </div>

                <input
                  type="range"
                  min="5"
                  max="18"
                  step="0.5"
                  value={returnRate}
                  onChange={(event) =>
                    setReturnRate(
                      Number(event.target.value)
                    )
                  }
                />

                <div className="range-values">
                  <span>5%</span>
                  <span>18%</span>
                </div>

              </div>

            </div>

            {/* RESULT */}

            <div className="investment-result">

              <span>
                ESTIMATED FUTURE VALUE
              </span>

              <strong>
                {formatCurrency(
                  investmentResult.total
                )}
              </strong>

              <div className="result-breakdown">

                <div>
                  <span>
                    Amount Invested
                  </span>

                  <strong>
                    {formatCurrency(
                      investmentResult.invested
                    )}
                  </strong>
                </div>

                <div>
                  <span>
                    Estimated Returns
                  </span>

                  <strong className="returns">
                    {formatCurrency(
                      investmentResult.returns
                    )}
                  </strong>
                </div>

              </div>

              <div className="growth-bar">

                <div
                  className="invested-bar"
                  style={{
                    width: `${
                      investmentResult.total
                        ? (
                            investmentResult.invested /
                            investmentResult.total
                          ) * 100
                        : 0
                    }%`,
                  }}
                />

              </div>

              <small>
                Based on {returnRate}% annual
                assumed return. Actual returns can vary.
              </small>

            </div>

          </div>

        </section>

        {/* ====================================================
            SAVINGS GOAL SIMULATOR
        ==================================================== */}

        <section className="simulator-card savings-simulator">

          <div className="simulator-card-header">

            <div>

              <span className="card-label">
                <PiggyBank size={14} />
                SAVINGS SIMULATOR
              </span>

              <h2>
                Build your savings goal
              </h2>

              <p>
                See how regular monthly savings can add up.
              </p>

            </div>

            <div className="simulator-card-icon green">
              <PiggyBank size={23} />
            </div>

          </div>

          <div className="savings-grid">

            <div className="savings-inputs">

              <div className="simulator-input-group">

                <div className="simulator-label-row">

                  <label>
                    Monthly Savings
                  </label>

                  <strong>
                    {formatCurrency(monthlySaving)}
                  </strong>

                </div>

                <input
                  type="range"
                  min="1000"
                  max="100000"
                  step="1000"
                  value={monthlySaving}
                  onChange={(event) =>
                    setMonthlySaving(
                      Number(event.target.value)
                    )
                  }
                />

                <div className="range-values">
                  <span>₹1K</span>
                  <span>₹1L</span>
                </div>

              </div>

              <div className="simulator-input-group">

                <div className="simulator-label-row">

                  <label>
                    Savings Period
                  </label>

                  <strong>
                    {savingYears} Years
                  </strong>

                </div>

                <input
                  type="range"
                  min="1"
                  max="20"
                  step="1"
                  value={savingYears}
                  onChange={(event) =>
                    setSavingYears(
                      Number(event.target.value)
                    )
                  }
                />

                <div className="range-values">
                  <span>1 Year</span>
                  <span>20 Years</span>
                </div>

              </div>

            </div>

            <div className="savings-result">

              <div className="savings-result-icon">
                <Target size={25} />
              </div>

              <div>

                <span>
                  PROJECTED SAVINGS
                </span>

                <strong>
                  {formatCurrency(
                    savingsResult.total
                  )}
                </strong>

                <p>
                  Saving{" "}
                  {formatCurrency(monthlySaving)}
                  {" "}every month for{" "}
                  {savingYears} years.
                </p>

              </div>

            </div>

          </div>

        </section>

        {/* ====================================================
            AI INSIGHT
        ==================================================== */}

        <section className="simulator-ai">

          <div className="simulator-ai-icon">
            <Sparkles size={25} />
          </div>

          <div className="simulator-ai-content">

            <span>
              FINGURU AI INSIGHT
            </span>

            <h2>
              Consistency can make a big difference.
            </h2>

            <p>
              Increasing your monthly investment by even
              ₹1,000 can significantly change your projected
              long-term value because your contributions have
              more time to compound.
            </p>

          </div>

          <div className="ai-check">

            <CheckCircle2 size={18} />

            <span>
              Scenario Ready
            </span>

          </div>

        </section>

        {/* ====================================================
            SCENARIO SUMMARY
        ==================================================== */}

        <section className="scenario-section">

          <div className="scenario-heading">

            <span>
              YOUR CURRENT SCENARIO
            </span>

            <h2>
              Financial projection
            </h2>

          </div>

          <div className="scenario-grid">

            <div className="scenario-card">

              <div className="scenario-icon">
                <IndianRupee size={20} />
              </div>

              <span>
                MONTHLY INVESTMENT
              </span>

              <strong>
                {formatCurrency(
                  monthlyInvestment
                )}
              </strong>

            </div>

            <div className="scenario-card">

              <div className="scenario-icon">
                <Calculator size={20} />
              </div>

              <span>
                INVESTMENT PERIOD
              </span>

              <strong>
                {investmentYears} Years
              </strong>

            </div>

            <div className="scenario-card">

              <div className="scenario-icon">
                <TrendingUp size={20} />
              </div>

              <span>
                ASSUMED RETURN
              </span>

              <strong>
                {returnRate}%
              </strong>

            </div>

            <div className="scenario-card highlight">

              <div className="scenario-icon">
                <Target size={20} />
              </div>

              <span>
                FUTURE VALUE
              </span>

              <strong>
                {formatCurrency(
                  investmentResult.total
                )}
              </strong>

            </div>

          </div>

        </section>

        {/* ====================================================
            DISCLAIMER
        ==================================================== */}

        <div className="simulator-disclaimer">

          <Sparkles size={13} />

          Simulations are illustrative only and are not
          guaranteed returns or financial advice.

        </div>

        {/* FOOTER */}

        <footer className="simulator-footer">

          <span>
            © 2026 FinGuru AI
          </span>

          <span>
            Plan • Simulate • Grow
          </span>

        </footer>

      </main>

    </div>
  );
}

export default Simulator;