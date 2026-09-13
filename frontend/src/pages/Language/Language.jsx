import {
  ArrowLeft,
  Languages,
  Check,
  Sparkles,
  Globe2,
} from "lucide-react";

import { useLanguage } from "../../i18n/LanguageContext";

import "./Language.css";

function Language({ onBack }) {
  const {
    language,
    setLanguage,
    t,
  } = useLanguage();

  const languages = [
    {
      id: "en",
      name: "English",
      nativeName: "English",
    },
    {
      id: "hi",
      name: "Hindi",
      nativeName: "हिन्दी",
    },
    {
      id: "kn",
      name: "Kannada",
      nativeName: "ಕನ್ನಡ",
    },
    {
      id: "te",
      name: "Telugu",
      nativeName: "తెలుగు",
    },
    {
      id: "ta",
      name: "Tamil",
      nativeName: "தமிழ்",
    },
    {
      id: "ml",
      name: "Malayalam",
      nativeName: "മലയാളം",
    },
    {
      id: "mr",
      name: "Marathi",
      nativeName: "मराठी",
    },
    {
      id: "bn",
      name: "Bengali",
      nativeName: "বাংলা",
    },
  ];

  function handleLanguageChange(languageId) {
    setLanguage(languageId);
  }

  return (
    <div className="language-page">

      <header className="language-header">

        <button
          className="language-back"
          onClick={onBack}
        >
          <ArrowLeft size={20} />
          {t("common.back")}
        </button>

        <div className="language-brand">

          <div className="language-logo">
            F
          </div>

          <div>
            <h2>{t("brand.name")}</h2>
            <span>
              {t("language.title")}
            </span>
          </div>

        </div>

      </header>

      <main className="language-container">

        <section className="language-hero">

          <div className="language-hero-icon">
            <Languages size={32} />
          </div>

          <div>

            <span className="language-label">
              {t("language.personalize")}
            </span>

            <h1>
              {t("language.title")}
            </h1>

            <p>
              {t("language.subtitle")}
            </p>

          </div>

        </section>

        <section className="current-language">

          <div className="current-language-icon">
            <Globe2 size={22} />
          </div>

          <div>
            <span>
              {t("language.currentLanguage")}
            </span>

            <strong>
              {
                languages.find(
                  (item) => item.id === language
                )?.nativeName
              }
            </strong>
          </div>

          <div className="selected-indicator">
            <Check size={17} />
            {t("common.selected")}
          </div>

        </section>

        <section className="language-section">

          <div className="language-section-heading">

            <div>
              <span>
                {t("language.availableLanguages")}
              </span>

              <h2>
                {t("language.selectPreferred")}
              </h2>
            </div>

            <Sparkles size={22} />

          </div>

          <div className="language-grid">

            {languages.map((item) => {

              const isSelected =
                language === item.id;

              return (
                <button
                  key={item.id}
                  type="button"
                  className={`language-card ${
                    isSelected ? "selected" : ""
                  }`}
                  onClick={() =>
                    handleLanguageChange(item.id)
                  }
                >

                  <div className="language-card-top">

                    <div className="language-symbol">
                      {item.name.charAt(0)}
                    </div>

                    {isSelected && (
                      <div className="language-check">
                        <Check size={16} />
                      </div>
                    )}

                  </div>

                  <div className="language-card-content">

                    <strong>
                      {item.name}
                    </strong>

                    <h3>
                      {item.nativeName}
                    </h3>

                  </div>

                </button>
              );
            })}

          </div>

        </section>

        <section className="language-ai-note">

          <div className="language-ai-icon">
            <Sparkles size={22} />
          </div>

          <div>

            <strong>
              FinGuru AI Copilot
            </strong>

            <p>
              {t("language.copilotNote")}
            </p>

          </div>

        </section>

        <footer className="language-footer">

          <span>
            {t("brand.name")}
          </span>

          <span>
            {t("brand.tagline")}
          </span>

        </footer>

      </main>

    </div>
  );
}

export default Language;