import { useState } from "react";
import {
  ArrowLeft,
  Bell,
  Check,
  ChevronRight,
  Edit3,
  IndianRupee,
  Lock,
  LogOut,
  Mail,
  Phone,
  Save,
  ShieldCheck,
  User,
  Wallet,
} from "lucide-react";

import "./Profile.css";

function Profile({ onBack, onLogout }) {
  const [editing, setEditing] = useState(false);

  const [profile, setProfile] = useState({
    name: "Bharath Kumar",
    mobile: "9876543210",
    email: "bharath@example.com",
    occupation: "Software Developer",
    monthlyIncome: "65000",
    monthlySavings: "46550",
    riskProfile: "Moderate",
  });

  const [notifications, setNotifications] = useState({
    transactions: true,
    security: true,
    advice: true,
    goals: true,
  });

  const handleChange = (event) => {
    const { name, value } = event.target;

    setProfile((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const toggleNotification = (key) => {
    setNotifications((previous) => ({
      ...previous,
      [key]: !previous[key],
    }));
  };

  const handleSave = () => {
    setEditing(false);
  };

  return (
    <div className="profile-page">
      <header className="profile-header">
        <div className="profile-header-left">
          <button
            className="profile-back-button"
            onClick={onBack}
            aria-label="Go back"
          >
            <ArrowLeft size={20} />
          </button>

          <div>
            <div className="profile-brand">
              <div className="profile-brand-logo">F</div>
              <span>FinGuru</span>
            </div>

            <p>Profile & Preferences</p>
          </div>
        </div>

        <div className="profile-header-status">
          <ShieldCheck size={16} />
          Account Protected
        </div>
      </header>

      <main className="profile-container">
        <section className="profile-hero">
          <div className="profile-avatar-large">
            BK
          </div>

          <div className="profile-hero-info">
            <span>FINGURU CUSTOMER</span>
            <h1>{profile.name}</h1>
            <p>
              <Phone size={14} />
              +91 {profile.mobile}
            </p>

            <div className="profile-badges">
              <span>
                <ShieldCheck size={13} />
                Verified Account
              </span>

              <span>
                <Wallet size={13} />
                Financial Score 78
              </span>
            </div>
          </div>

          <button
            className="edit-profile-button"
            onClick={() => {
              if (editing) {
                handleSave();
              } else {
                setEditing(true);
              }
            }}
          >
            {editing ? <Save size={17} /> : <Edit3 size={17} />}
            {editing ? "Save Changes" : "Edit Profile"}
          </button>
        </section>

        <div className="profile-layout">
          <section className="profile-main">
            <div className="profile-card">
              <div className="profile-card-heading">
                <div>
                  <span>PERSONAL INFORMATION</span>
                  <h2>Your profile</h2>
                </div>

                <User size={20} />
              </div>

              <div className="profile-form-grid">
                <div className="profile-field">
                  <label>Full Name</label>

                  <div className="field-wrapper">
                    <User size={17} />

                    <input
                      type="text"
                      name="name"
                      value={profile.name}
                      onChange={handleChange}
                      disabled={!editing}
                    />
                  </div>
                </div>

                <div className="profile-field">
                  <label>Mobile Number</label>

                  <div className="field-wrapper">
                    <Phone size={17} />

                    <input
                      type="text"
                      name="mobile"
                      value={profile.mobile}
                      disabled
                    />

                    <span className="verified-small">
                      <Check size={12} />
                    </span>
                  </div>
                </div>

                <div className="profile-field">
                  <label>Email Address</label>

                  <div className="field-wrapper">
                    <Mail size={17} />

                    <input
                      type="email"
                      name="email"
                      value={profile.email}
                      onChange={handleChange}
                      disabled={!editing}
                    />
                  </div>
                </div>

                <div className="profile-field">
                  <label>Occupation</label>

                  <div className="field-wrapper">
                    <Wallet size={17} />

                    <input
                      type="text"
                      name="occupation"
                      value={profile.occupation}
                      onChange={handleChange}
                      disabled={!editing}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="profile-card">
              <div className="profile-card-heading">
                <div>
                  <span>FINANCIAL PROFILE</span>
                  <h2>Financial preferences</h2>
                </div>

                <IndianRupee size={20} />
              </div>

              <div className="profile-form-grid">
                <div className="profile-field">
                  <label>Monthly Income</label>

                  <div className="field-wrapper">
                    <IndianRupee size={17} />

                    <input
                      type="number"
                      name="monthlyIncome"
                      value={profile.monthlyIncome}
                      onChange={handleChange}
                      disabled={!editing}
                    />
                  </div>
                </div>

                <div className="profile-field">
                  <label>Monthly Savings</label>

                  <div className="field-wrapper">
                    <IndianRupee size={17} />

                    <input
                      type="number"
                      name="monthlySavings"
                      value={profile.monthlySavings}
                      onChange={handleChange}
                      disabled={!editing}
                    />
                  </div>
                </div>

                <div className="profile-field">
                  <label>Risk Preference</label>

                  <div className="field-wrapper">
                    <ShieldCheck size={17} />

                    <select
                      name="riskProfile"
                      value={profile.riskProfile}
                      onChange={handleChange}
                      disabled={!editing}
                    >
                      <option>Conservative</option>
                      <option>Moderate</option>
                      <option>Aggressive</option>
                    </select>
                  </div>
                </div>

                <div className="profile-field">
                  <label>Financial Wellness</label>

                  <div className="wellness-value">
                    <strong>78</strong>
                    <span>Excellent</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="profile-card">
              <div className="profile-card-heading">
                <div>
                  <span>NOTIFICATIONS</span>
                  <h2>Stay informed</h2>
                </div>

                <Bell size={20} />
              </div>

              <div className="notification-list">
                <NotificationRow
                  title="Transaction Alerts"
                  description="Get notified when money moves in or out."
                  enabled={notifications.transactions}
                  onClick={() =>
                    toggleNotification("transactions")
                  }
                />

                <NotificationRow
                  title="Security Alerts"
                  description="Receive important account protection alerts."
                  enabled={notifications.security}
                  onClick={() =>
                    toggleNotification("security")
                  }
                />

                <NotificationRow
                  title="AI Advice"
                  description="Receive personalized financial recommendations."
                  enabled={notifications.advice}
                  onClick={() =>
                    toggleNotification("advice")
                  }
                />

                <NotificationRow
                  title="Goal Reminders"
                  description="Get reminders to stay on track with your goals."
                  enabled={notifications.goals}
                  onClick={() => toggleNotification("goals")}
                />
              </div>
            </div>
          </section>

          <aside className="profile-sidebar">
            <div className="security-card-profile">
              <div className="security-profile-icon">
                <ShieldCheck size={24} />
              </div>

              <span>SECURITY STATUS</span>

              <h2>Excellent</h2>

              <p>
                Your FinGuru account currently has strong
                security protection.
              </p>

              <div className="security-score">
                <div>
                  <span>Security Score</span>
                  <strong>92/100</strong>
                </div>

                <div className="security-progress">
                  <div />
                </div>
              </div>
            </div>

            <div className="quick-actions-card">
              <span>ACCOUNT</span>

              <h2>Quick actions</h2>

              <button>
                <div>
                  <Lock size={17} />
                  <span>Security Settings</span>
                </div>

                <ChevronRight size={17} />
              </button>

              <button>
                <div>
                  <Bell size={17} />
                  <span>Notification Settings</span>
                </div>

                <ChevronRight size={17} />
              </button>

              <button>
                <div>
                  <ShieldCheck size={17} />
                  <span>Privacy Controls</span>
                </div>

                <ChevronRight size={17} />
              </button>
            </div>

            <button
              className="logout-profile-button"
              onClick={onLogout}
            >
              <LogOut size={17} />
              Logout from FinGuru
            </button>
          </aside>
        </div>

        <section className="profile-footer-note">
          <ShieldCheck size={17} />

          <div>
            <strong>Your information stays protected.</strong>

            <p>
              FinGuru uses your preferences to personalize your
              financial experience. Sensitive actions should
              always require appropriate authentication.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

function NotificationRow({
  title,
  description,
  enabled,
  onClick,
}) {
  return (
    <div className="notification-row">
      <div className="notification-row-icon">
        <Bell size={17} />
      </div>

      <div className="notification-row-content">
        <strong>{title}</strong>
        <span>{description}</span>
      </div>

      <button
        className={`notification-toggle ${
          enabled ? "enabled" : ""
        }`}
        onClick={onClick}
        aria-label={`Toggle ${title}`}
      >
        <span />
      </button>
    </div>
  );
}

export default Profile;