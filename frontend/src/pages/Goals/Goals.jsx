import { useMemo, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  CalendarDays,
  CheckCircle2,
  CircleDollarSign,
  Plus,
  Sparkles,
  Target,
  TrendingUp,
  Wallet,
  X,
} from "lucide-react";

import "./Goals.css";

const initialGoals = [
  {
    id: 1,
    name: "Emergency Fund",
    description: "Build a safety cushion for unexpected expenses",
    target: 150000,
    saved: 87000,
    deadline: "Dec 2026",
    category: "Safety",
    icon: Wallet,
    accent: "green",
  },
  {
    id: 2,
    name: "New Laptop",
    description: "Save for a high-performance laptop",
    target: 90000,
    saved: 58500,
    deadline: "Mar 2027",
    category: "Personal",
    icon: Target,
    accent: "blue",
  },
  {
    id: 3,
    name: "Vacation Fund",
    description: "Plan a memorable vacation without taking debt",
    target: 100000,
    saved: 42000,
    deadline: "Jun 2027",
    category: "Lifestyle",
    icon: CalendarDays,
    accent: "purple",
  },
  {
    id: 4,
    name: "Investment Corpus",
    description: "Create a long-term wealth-building fund",
    target: 500000,
    saved: 180000,
    deadline: "Dec 2028",
    category: "Investment",
    icon: TrendingUp,
    accent: "orange",
  },
];

const formatCurrency = (value) =>
  `₹${Number(value).toLocaleString("en-IN")}`;

function calculateMonthlyContribution(target, saved, months) {
  const remaining = Math.max(Number(target) - Number(saved), 0);

  if (months <= 0) {
    return remaining;
  }

  return Math.ceil(remaining / months);
}

function Goals({ onBack }) {
  const [goals, setGoals] = useState(initialGoals);
  const [showForm, setShowForm] = useState(false);

  const [form, setForm] = useState({
    name: "",
    description: "",
    target: "",
    saved: "",
    months: "12",
    category: "Personal",
  });

  const totals = useMemo(() => {
    const target = goals.reduce((sum, goal) => sum + goal.target, 0);
    const saved = goals.reduce((sum, goal) => sum + goal.saved, 0);

    return {
      target,
      saved,
      remaining: Math.max(target - saved, 0),
      progress: target ? Math.round((saved / target) * 100) : 0,
    };
  }, [goals]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const addGoal = (event) => {
    event.preventDefault();

    if (!form.name || !form.target) {
      return;
    }

    const target = Number(form.target);
    const saved = Number(form.saved || 0);
    const months = Number(form.months || 12);

    const newGoal = {
      id: Date.now(),
      name: form.name,
      description:
        form.description || "Personal financial goal created with FinGuru",
      target,
      saved: Math.min(saved, target),
      deadline: `${months} months`,
      category: form.category,
      icon: Target,
      accent: "blue",
    };

    setGoals((previous) => [newGoal, ...previous]);

    setForm({
      name: "",
      description: "",
      target: "",
      saved: "",
      months: "12",
      category: "Personal",
    });

    setShowForm(false);
  };

  return (
    <div className="goals-page">
      <header className="goals-header">
        <div className="goals-header-left">
          <button
            className="goals-back-button"
            onClick={onBack}
            aria-label="Go back"
          >
            <ArrowLeft size={20} />
          </button>

          <div>
            <div className="goals-brand">
              <div className="goals-brand-logo">F</div>
              <span>FinGuru</span>
            </div>

            <p>Financial Goals</p>
          </div>
        </div>

        <button
          className="add-goal-button"
          onClick={() => setShowForm(true)}
        >
          <Plus size={19} />
          Add Goal
        </button>
      </header>

      <main className="goals-container">
        <section className="goals-hero">
          <div className="goals-hero-content">
            <span className="goals-eyebrow">
              <Target size={15} />
              GOAL PLANNER
            </span>

            <h1>Turn your plans into progress.</h1>

            <p>
              Set meaningful financial goals, track your progress, and let
              FinGuru help you stay on course.
            </p>

            <button
              className="hero-goal-button"
              onClick={() => setShowForm(true)}
            >
              Create a new goal
              <ArrowRight size={18} />
            </button>
          </div>

          <div className="hero-target">
            <div className="hero-target-icon">
              <Target size={30} />
            </div>

            <span>Total Goal Progress</span>

            <strong>{totals.progress}%</strong>

            <div className="hero-progress">
              <div
                style={{
                  width: `${Math.min(totals.progress, 100)}%`,
                }}
              />
            </div>

            <small>
              {formatCurrency(totals.saved)} saved of{" "}
              {formatCurrency(totals.target)}
            </small>
          </div>
        </section>

        <section className="goal-summary">
          <div className="summary-card">
            <div className="summary-icon target-icon">
              <Target size={21} />
            </div>

            <div>
              <span>Total Target</span>
              <strong>{formatCurrency(totals.target)}</strong>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon saved-icon">
              <CheckCircle2 size={21} />
            </div>

            <div>
              <span>Total Saved</span>
              <strong>{formatCurrency(totals.saved)}</strong>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon remaining-icon">
              <CircleDollarSign size={21} />
            </div>

            <div>
              <span>Remaining</span>
              <strong>{formatCurrency(totals.remaining)}</strong>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon goal-count-icon">
              <TrendingUp size={21} />
            </div>

            <div>
              <span>Active Goals</span>
              <strong>{goals.length}</strong>
            </div>
          </div>
        </section>

        <section className="goals-section">
          <div className="section-heading">
            <div>
              <span>YOUR GOALS</span>
              <h2>Goals you're working towards</h2>
            </div>

            <button
              className="section-add-button"
              onClick={() => setShowForm(true)}
            >
              <Plus size={17} />
              New Goal
            </button>
          </div>

          <div className="goals-grid">
            {goals.map((goal) => {
              const Icon = goal.icon;

              const progress =
                goal.target > 0
                  ? Math.min(
                      Math.round((goal.saved / goal.target) * 100),
                      100
                    )
                  : 0;

              const remaining = Math.max(goal.target - goal.saved, 0);

              const monthlyContribution =
                calculateMonthlyContribution(
                  goal.target,
                  goal.saved,
                  goal.deadline.includes("months")
                    ? Number.parseInt(goal.deadline)
                    : 12
                );

              return (
                <article
                  className={`goal-card goal-${goal.accent}`}
                  key={goal.id}
                >
                  <div className="goal-card-top">
                    <div className="goal-icon">
                      <Icon size={23} />
                    </div>

                    <span className="goal-category">
                      {goal.category}
                    </span>
                  </div>

                  <div className="goal-title">
                    <h3>{goal.name}</h3>
                    <p>{goal.description}</p>
                  </div>

                  <div className="goal-money-row">
                    <div>
                      <span>Saved</span>
                      <strong>{formatCurrency(goal.saved)}</strong>
                    </div>

                    <div className="goal-target-money">
                      <span>Target</span>
                      <strong>{formatCurrency(goal.target)}</strong>
                    </div>
                  </div>

                  <div className="goal-progress-area">
                    <div className="goal-progress-label">
                      <span>Progress</span>
                      <strong>{progress}%</strong>
                    </div>

                    <div className="goal-progress">
                      <div
                        style={{
                          width: `${progress}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div className="goal-details">
                    <div>
                      <CalendarDays size={16} />
                      <span>Deadline</span>
                      <strong>{goal.deadline}</strong>
                    </div>

                    <div>
                      <CircleDollarSign size={16} />
                      <span>Remaining</span>
                      <strong>{formatCurrency(remaining)}</strong>
                    </div>
                  </div>

                  <div className="goal-monthly">
                    <div className="monthly-icon">
                      <Wallet size={18} />
                    </div>

                    <div>
                      <span>Suggested monthly contribution</span>
                      <strong>
                        {formatCurrency(monthlyContribution)}
                      </strong>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <section className="goal-ai-card">
          <div className="goal-ai-icon">
            <Sparkles size={26} />
          </div>

          <div className="goal-ai-content">
            <span>FIN GURU AI RECOMMENDATION</span>

            <h2>Your goals are moving in the right direction.</h2>

            <p>
              You have already saved{" "}
              <strong>{formatCurrency(totals.saved)}</strong> toward your
              active goals. Based on your current monthly savings of
              approximately ₹46,550, consider prioritizing your emergency
              fund first and then increasing your long-term investment
              contribution.
            </p>
          </div>

          <div className="ai-action">
            <TrendingUp size={20} />
            <span>Stay consistent</span>
          </div>
        </section>
      </main>

      {showForm && (
        <div
          className="goal-modal-overlay"
          onClick={() => setShowForm(false)}
        >
          <div
            className="goal-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="modal-header">
              <div>
                <span>Create Goal</span>
                <h2>What are you saving for?</h2>
              </div>

              <button
                className="modal-close"
                onClick={() => setShowForm(false)}
                aria-label="Close"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={addGoal}>
              <div className="form-group">
                <label>Goal Name</label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleInputChange}
                  placeholder="e.g. New Car"
                  required
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <input
                  type="text"
                  name="description"
                  value={form.description}
                  onChange={handleInputChange}
                  placeholder="What is this goal for?"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Target Amount</label>

                  <div className="input-with-prefix">
                    <span>₹</span>

                    <input
                      type="number"
                      name="target"
                      value={form.target}
                      onChange={handleInputChange}
                      placeholder="100000"
                      min="1"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Already Saved</label>

                  <div className="input-with-prefix">
                    <span>₹</span>

                    <input
                      type="number"
                      name="saved"
                      value={form.saved}
                      onChange={handleInputChange}
                      placeholder="0"
                      min="0"
                    />
                  </div>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Target Timeline</label>

                  <select
                    name="months"
                    value={form.months}
                    onChange={handleInputChange}
                  >
                    <option value="3">3 months</option>
                    <option value="6">6 months</option>
                    <option value="12">12 months</option>
                    <option value="18">18 months</option>
                    <option value="24">24 months</option>
                    <option value="36">36 months</option>
                    <option value="60">60 months</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Category</label>

                  <select
                    name="category"
                    value={form.category}
                    onChange={handleInputChange}
                  >
                    <option value="Safety">Safety</option>
                    <option value="Personal">Personal</option>
                    <option value="Lifestyle">Lifestyle</option>
                    <option value="Investment">Investment</option>
                    <option value="Education">Education</option>
                    <option value="Travel">Travel</option>
                  </select>
                </div>
              </div>

              {form.target && (
                <div className="form-preview">
                  <Sparkles size={18} />

                  <span>
                    FinGuru estimates you'll need approximately{" "}
                    <strong>
                      {formatCurrency(
                        calculateMonthlyContribution(
                          Number(form.target),
                          Number(form.saved || 0),
                          Number(form.months || 12)
                        )
                      )}
                    </strong>{" "}
                    per month.
                  </span>
                </div>
              )}

              <button className="create-goal-button" type="submit">
                <Target size={18} />
                Create Financial Goal
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Goals;