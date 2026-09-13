import {
  ArrowDownLeft,
  ArrowUpRight,
  ArrowLeft,
  CreditCard,
  Wallet,
  PiggyBank,
  TrendingUp,
  IndianRupee,
} from "lucide-react";

import "./Money.css";

function Money({ onBack }) {
  return (
    <div className="money-page">

      {/* HEADER */}

      <header className="money-header">

        <button className="back-button" onClick={onBack}>
          <ArrowLeft size={19} />
          Back to Dashboard
        </button>

        <div className="money-title">
          <div className="money-title-icon">
            <Wallet size={22} />
          </div>

          <div>
            <h1>My Money</h1>
            <p>Your complete financial overview</p>
          </div>
        </div>

      </header>


      <main className="money-container">

        {/* TOTAL BALANCE */}

        <section className="balance-card">

          <div>
            <span>Total Balance</span>

            <h2>₹2,78,500</h2>

            <p>
              <TrendingUp size={15} />
              +8.4% from last month
            </p>
          </div>

          <div className="balance-icon">
            <IndianRupee size={42} />
          </div>

        </section>


        {/* ACCOUNT CARDS */}

        <section>

          <div className="section-heading">
            <div>
              <h2>Your Accounts</h2>
              <p>Accounts connected to FinGuru</p>
            </div>
          </div>


          <div className="account-grid">

            <div className="account-card">

              <div className="account-top">
                <div className="account-icon bank">
                  <Wallet size={21} />
                </div>

                <span className="account-status">
                  Active
                </span>
              </div>

              <h3>Primary Savings Account</h3>

              <p>**** 4521</p>

              <strong>₹1,53,500</strong>

            </div>


            <div className="account-card">

              <div className="account-top">
                <div className="account-icon card">
                  <CreditCard size={21} />
                </div>

                <span className="account-status">
                  Active
                </span>
              </div>

              <h3>Credit Card</h3>

              <p>**** 7824</p>

              <strong>₹25,000</strong>

            </div>


            <div className="account-card">

              <div className="account-top">
                <div className="account-icon investment">
                  <TrendingUp size={21} />
                </div>

                <span className="account-status">
                  Growing
                </span>
              </div>

              <h3>Investments</h3>

              <p>Mutual Funds + SIP</p>

              <strong>₹1,00,000</strong>

            </div>

          </div>

        </section>


        {/* INCOME / EXPENSE */}

        <section className="money-grid">

          <div className="money-panel">

            <div className="panel-icon income-icon">
              <ArrowDownLeft size={21} />
            </div>

            <div>
              <span>Monthly Income</span>
              <h2>₹65,000</h2>
              <p className="green">
                +8.4% this month
              </p>
            </div>

          </div>


          <div className="money-panel">

            <div className="panel-icon expense-icon">
              <ArrowUpRight size={21} />
            </div>

            <div>
              <span>Monthly Expenses</span>
              <h2>₹18,450</h2>
              <p>
                28.4% of income
              </p>
            </div>

          </div>


          <div className="money-panel">

            <div className="panel-icon savings-icon">
              <PiggyBank size={21} />
            </div>

            <div>
              <span>Monthly Savings</span>
              <h2>₹46,550</h2>
              <p className="green">
                71.6% savings rate
              </p>
            </div>

          </div>

        </section>


        {/* AI INSIGHT */}

        <section className="money-insight">

          <div className="insight-icon">
            ✦
          </div>

          <div>
            <span>FINGURU AI INSIGHT</span>

            <h3>
              You're building a strong financial foundation.
            </h3>

            <p>
              Your current savings rate is 71.6%. FinGuru
              recommends maintaining your emergency fund
              while continuing your investment contributions.
            </p>
          </div>

        </section>

      </main>

    </div>
  );
}

export default Money;