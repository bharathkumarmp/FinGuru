import {
  createContext,
  useContext,
  useMemo,
  useState,
} from "react";

import translations from "./translations";

const LanguageContext = createContext(null);

const LANGUAGE_KEY = "finguru_language";

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem(LANGUAGE_KEY) || "en";
  });

  const setLanguage = (newLanguage) => {
    setLanguageState(newLanguage);
    localStorage.setItem(LANGUAGE_KEY, newLanguage);
  };

  const t = (key) => {
    const keys = key.split(".");

    let value = translations[language];

    for (const part of keys) {
      value = value?.[part];
    }

    if (value !== undefined) {
      return value;
    }

    // Fallback to English
    value = translations.en;

    for (const part of keys) {
      value = value?.[part];
    }

    return value || key;
  };

  const value = useMemo(
    () => ({
      language,
      setLanguage,
      t,
    }),
    [language]
  );

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);

  if (!context) {
    throw new Error(
      "useLanguage must be used inside LanguageProvider"
    );
  }

  return context;
}