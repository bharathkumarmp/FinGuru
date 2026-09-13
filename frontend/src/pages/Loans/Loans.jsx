import { useMemo, useState } from "react";
import {
  ArrowLeft,
  BadgeCheck,
  Banknote,
  Calculator,
  CheckCircle2,
  Clock3,
  IndianRupee,
  Percent,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import "./Loans.css";

function Loans({ onBack }) {
  const [loanAmount, setLoanAmount] = useState(500000);
  const [interestRate, setInterestRate] = useState(10.5);
  const [tenure, setTenure] = useState(5);

  const emi = useMemo(() => {
    const principal = Number(loanAmount);
    const monthlyRate = Number(interestRate) / 100 / 12;
    const months = Number(tenure) * 12;

    if (!principal || !monthlyRate || !months) {
      return 0;
    }

    const monthlyEmi =
      (principal *
        monthlyRate *
        Math.pow(1 + monthlyRate, months)) /
      (Math.pow(1 + monthlyRate, months) - 1);

    return Math.round(monthlyEmi);
  }, [loanAmount, interestRate, tenure]);

  const totalPayment = emi * tenure * 12;
  const totalInterest = totalPayment - loanAmount;

  const formatCurrency = (value) =>
    `₹${Number(value).toLocaleString("en-IN")}`;

  return (
    <div className="loans-page">
      {/* HEADER */}
      <header className="loans-header">
        <button className="loans-back-btn" onClick={onBack}>
          <ArrowLeft size={19} />
          Back
        </button>

        <div className="loans-brand">
          <div className="loans-logo">F</div>
          <div>
            <h2>FinGuru</h2>
            <span>Smart Loan Intelligence</span>
          </div>
        </div>

        <div className="loan-header-status">
          <ShieldCheck size={18} />
          Secure & AI Powered
        </div>
      </header>

      <main className="loans-container">
        {/* TITLE */}
        <section className="loans-title-section">
          <div>
            <span className="loans-eyebrow">
              <Sparkles size={14} />
              FINANCIAL PLANNING
            </span>

            <h1>Loans made smarter.</h1>

            <p>
              Understand your borrowing capacity, calculate EMI,
              and make a better loan decision with FinGuru AI.
            </p>
          </div>

          <div className="loan-readiness">
            <div className="readiness-icon">
              <BadgeCheck size={28} />
            </div>

            <div>
              <span>LOAN READINESS</span>
              <strong>Excellent</strong>
              <small>82 / 100</small>
            </div>
          </div>
        </section>

        {/* ELIGIBILITY */}
        <section className="eligibility-card">
          <div className="eligibility-left">
            <div className="section-icon blue">
              <CheckCircle2 size={23} />
            </div>

            <div>
              <h2>You're financially ready</h2>
              <p>
                Based on your financial profile, your current
                repayment capacity looks healthy.
              </p>
            </div>
          </div>

          <div className="eligibility-points">
            <span>
              <CheckCircle2 size={15} />
              Stable income
            </span>

            <span>
              <CheckCircle2 size={15} />
              Healthy savings
            </span>

            <span>
              <CheckCircle2 size={15} />
              Good debt health
            </span>
          </div>
        </section>

        <div className="loans-main-grid">
          {/* CALCULATOR */}
          <section className="loan-calculator-card">
            <div className="card-heading">
              <div>
                <span className="card-eyebrow">
                  <Calculator size={14} />
                  EMI CALCULATOR
                </span>
                <h2>Plan your repayment</h2>
              </div>

              <div className="calculator-icon">
                <IndianRupee size={23} />
              </div>
            </div>

            {/* LOAN AMOUNT */}
            <div className="loan-input-group">
              <div className="input-label-row">
                <label>Loan Amount</label>
                <strong>{formatCurrency(loanAmount)}</strong>
              </div>

              <input
                type="range"
                min="50000"
                max="5000000"
                step="50000"
                value={loanAmount}
                onChange={(e) =>
                  setLoanAmount(Number(e.target.value))
                }
              />

              <div className="range-labels">
                <span>₹50K</span>
                <span>₹50L</span>
              </div>
            </div>

            {/* INTEREST */}
            <div className="loan-input-group">
              <div className="input-label-row">
                <label>Interest Rate</label>
                <strong>{interestRate}%</strong>
              </div>

              <input
                type="range"
                min="6"
                max="18"
                step="0.1"
                value={interestRate}
                onChange={(e) =>
                  setInterestRate(Number(e.target.value))
                }
              />

              <div className="range-labels">
                <span>6%</span>
                <span>18%</span>
              </div>
            </div>

            {/* TENURE */}
            <div className="loan-input-group">
              <div className="input-label-row">
                <label>Loan Tenure</label>
                <strong>{tenure} Years</strong>
              </div>

              <input
                type="range"
                min="1"
                max="20"
                step="1"
                value={tenure}
                onChange={(e) =>
                  setTenure(Number(e.target.value))
                }
              />

              <div className="range-labels">
                <span>1 Year</span>
                <span>20 Years</span>
              </div>
            </div>

            <div className="emi-result">
              <div>
                <span>ESTIMATED MONTHLY EMI</span>
                <strong>{formatCurrency(emi)}</strong>
              </div>

              <div className="emi-small">
                <Clock3 size={16} />
                {tenure} year repayment
              </div>
            </div>
          </section>

          {/* SUMMARY */}
          <section className="repayment-card">
            <div className="card-heading">
              <div>
                <span className="card-eyebrow">
                  <Banknote size={14} />
                  REPAYMENT SUMMARY
                </span>
                <h2>Your loan breakdown</h2>
              </div>
            </div>

            <div className="summary-list">
              <div>
                <span>Principal Amount</span>
                <strong>{formatCurrency(loanAmount)}</strong>
              </div>

              <div>
                <span>Total Interest</span>
                <strong>{formatCurrency(totalInterest)}</strong>
              </div>

              <div>
                <span>Total Repayment</span>
                <strong>{formatCurrency(totalPayment)}</strong>
              </div>

              <div>
                <span>Interest Rate</span>
                <strong>{interestRate}% p.a.</strong>
              </div>
            </div>

            <div className="interest-bar">
              <div className="interest-bar-label">
                <span>Principal</span>
                <span>Interest</span>
              </div>

              <div className="interest-track">
                <div
                  className="principal-part"
                  style={{
                    width: `${
                      totalPayment
                        ? (loanAmount / totalPayment) * 100
                        : 0
                    }%`,
                  }}
                />
              </div>
            </div>

            <div className="repayment-note">
              <Percent size={17} />
              Lower interest rates and shorter tenures can
              significantly reduce your total repayment.
            </div>
          </section>
        </div>

        {/* AI RECOMMENDATION */}
        <section className="loan-ai-card">
          <div className="ai-icon">
            <Sparkles size={26} />
          </div>

          <div className="ai-content">
            <span>FINGURU AI RECOMMENDATION</span>

            <h2>
              Keep your EMI below ₹20,000 if possible.
            </h2>

            <p>
              Your current financial profile indicates a healthy
              repayment capacity. Before taking a loan, compare
              interest rates and avoid extending the tenure more
              than necessary.
            </p>
          </div>

          <div className="ai-score">
            <span>RECOMMENDED</span>
            <strong>Healthy</strong>
          </div>
        </section>

        {/* LOAN OPTIONS */}
        <section className="loan-options-section">
          <div className="section-title">
            <div>
              <span>LOAN OPTIONS</span>
              <h2>Choose based on your goal</h2>
            </div>
          </div>

          <div className="loan-options-grid">
            <div className="loan-option">
              <div className="option-icon">
                <Banknote size={21} />
              </div>
              <h3>Personal Loan</h3>
              <p>
                Flexible funding for personal expenses,
                emergencies, or major purchases.
              </p>
              <strong>From 10.5% p.a.</strong>
            </div>

            <div className="loan-option">
              <div className="option-icon">
                <IndianRupee size={21} />
              </div>
              <h3>Home Loan</h3>
              <p>
                Plan long-term financing for your home with
                structured monthly repayments.
              </p>
              <strong>From 8.5% p.a.</strong>
            </div>

            <div className="loan-option">
              <div className="option-icon">
                <Calculator size={21} />
              </div>
              <h3>Education Loan</h3>
              <p>
                Estimate funding requirements for higher
                education and future career goals.
              </p>
              <strong>From 9% p.a.</strong>
            </div>
          </div>
        </section>

        <footer className="loans-footer">
          <span>© 2026 FinGuru AI</span>
          <span>
            Secure • Transparent • AI Powered
          </span>
        </footer>
      </main>
    </div>
  );
}

export default Loans;