// frontend/src/i18n/translations.js

const translations = {
  en: {
    // ================= COMMON =================
    common: {
      back: "Back",
      backToDashboard: "Back to Dashboard",
      save: "Save",
      cancel: "Cancel",
      confirm: "Confirm",
      close: "Close",
      loading: "Loading...",
      selected: "Selected",
      active: "Active",
      enabled: "Enabled",
      disabled: "Disabled",
      yes: "Yes",
      no: "No",
      viewAll: "View All",
      learnMore: "Learn More",
      continue: "Continue",
      submit: "Submit",
      success: "Success",
      error: "Error",
    },

    // ================= BRAND =================
    brand: {
      name: "FinGuru",
      tagline: "AI-powered personal finance",
    },

    // ================= NAVIGATION =================
    nav: {
      dashboard: "Dashboard",
      money: "Money",
      financialHealth: "Financial Health",
      advice: "AI Advice",
      copilot: "AI Copilot",
      loans: "Loans",
      simulator: "Simulator",
      transactions: "Transactions",
      goals: "Goals",
      security: "Security",
      language: "Language",
      profile: "Profile",
      privacy: "Privacy",
      settings: "Settings",
      logout: "Logout",
    },

    // ================= DASHBOARD =================
    dashboard: {
      title: "Financial Dashboard",
      welcome: "Welcome back",
      overview: "Here's your financial overview",
      totalBalance: "Total Balance",
      monthlyIncome: "Monthly Income",
      monthlySpending: "Monthly Spending",
      monthlySavings: "Monthly Savings",
      savingsRate: "Savings Rate",
      financialHealth: "Financial Health",
      financialStress: "Financial Stress",
      recentTransactions: "Recent Transactions",
      quickActions: "Quick Actions",
      aiAdvice: "AI Advice",
      askCopilot: "Ask AI Copilot",
      viewTransactions: "View Transactions",
      manageMoney: "Manage Money",
    },

    // ================= MONEY =================
    money: {
      title: "Money",
      overview: "Manage and understand your money",
      balance: "Balance",
      income: "Income",
      spending: "Spending",
      savings: "Savings",
      expenses: "Expenses",
      categories: "Spending Categories",
      biggestExpense: "Biggest Expense",
      monthlyOverview: "Monthly Overview",
      cashFlow: "Cash Flow",
    },

    // ================= FINANCIAL HEALTH =================
    health: {
      title: "Financial Health",
      score: "Health Score",
      excellent: "Excellent",
      good: "Good",
      moderate: "Moderate",
      needsAttention: "Needs Attention",
      incomeScore: "Income Score",
      spendingScore: "Spending Score",
      savingsScore: "Savings Score",
      debtScore: "Debt Score",
      stabilityScore: "Stability Score",
      strengths: "Strengths",
      weaknesses: "Areas to Improve",
      recommendations: "Recommendations",
      savingsRate: "Savings Rate",
      monthlyIncome: "Monthly Income",
      monthlySpending: "Monthly Spending",
      monthlySurplus: "Monthly Surplus",
    },

    // ================= ADVICE =================
    advice: {
      title: "Smart Advice for Your Money",
      subtitle:
        "FinGuru AI analyzes your financial behavior and provides personalized actions to help you save, grow, and protect your money.",
      personalizedGuidance: "PERSONALIZED AI GUIDANCE",
      aiAnalysisComplete: "AI Analysis Complete",
      finGuruAI: "FIN GURU AI",
      recommendationHeading:
        "Here's what I recommend for you",
      personalizedRecommendations:
        "PERSONALIZED RECOMMENDATIONS",
      nextBestActions: "Your Next Best Actions",
      exploreRecommendation: "Explore Recommendation",

      increaseSavings: "Increase Monthly Savings",
      increaseSavingsDescription:
        "You currently have a strong savings rate. Increasing your monthly savings can accelerate your financial goals.",

      emergencyFund: "Build Emergency Fund",
      emergencyFundDescription:
        "Building a 6-month reserve can provide an additional layer of financial security.",

      investConsistently: "Invest Consistently",
      investConsistentlyDescription:
        "Consider maintaining a regular investment contribution to build long-term wealth.",

      stayOnGoal: "Stay on Goal",
      stayOnGoalDescription:
        "Maintaining your current saving discipline can keep you on track.",

      highImpact: "High Impact",
      recommended: "Recommended",
      longTerm: "Long Term",
      onTrack: "On Track",

      actionPlan: "FIN GURU ACTION PLAN",
      monthlyPlan: "Your Monthly Financial Plan",
      smartTip: "SMART MONEY TIP",
      smallImprovements:
        "Small improvements compound over time.",
      buildHabits:
        "Build habits, not just balances.",
    },

    // ================= COPILOT =================
    copilot: {
      title: "FinGuru Copilot",
      subtitle: "Your AI-powered personal finance assistant",
      aiConnected: "AI Connected",
      spending: "Spending",
      spendingDescription: "Track your expenses",
      financialHealth: "Financial Health",
      healthDescription: "Understand your score",
      aiGuidance: "AI Guidance",
      guidanceDescription: "Get personalized insights",
      responsibleAI: "Responsible AI",
      responsibleDescription: "Privacy-aware advice",
      tryAsking: "Try asking",
      placeholder:
        "Ask FinGuru anything about your finances...",
      analyzing:
        "Analyzing your financial information...",
      basedOnData:
        "Based on your FinGuru financial data",
      disclaimer:
        "FinGuru Copilot provides AI-generated financial guidance. It does not replace professional financial advice.",
    },

    // ================= LOANS =================
    loans: {
      title: "Loans",
      loanAmount: "Loan Amount",
      interestRate: "Interest Rate",
      tenure: "Loan Tenure",
      monthlyEMI: "Monthly EMI",
      totalInterest: "Total Interest",
      totalPayment: "Total Payment",
      calculate: "Calculate EMI",
      eligibility: "Loan Eligibility",
      recommendation: "Loan Recommendation",
    },

    // ================= TRANSACTIONS =================
    transactions: {
      title: "Transactions",
      recent: "Recent Transactions",
      all: "All Transactions",
      income: "Income",
      expense: "Expense",
      merchant: "Merchant",
      category: "Category",
      amount: "Amount",
      date: "Date",
      description: "Description",
      noTransactions: "No transactions found",
    },

    // ================= GOALS =================
    goals: {
      title: "Financial Goals",
      savingsGoal: "Savings Goal",
      target: "Target",
      progress: "Progress",
      remaining: "Remaining",
      createGoal: "Create Goal",
      emergencyFund: "Emergency Fund",
      investment: "Investment",
      vacation: "Vacation",
      education: "Education",
    },

    // ================= SECURITY =================
    security: {
      title: "Security",
      secureAccount: "Keep Your Account Secure",
      fraudDetection: "Fraud Detection",
      incidents: "Security Incidents",
      protected: "Your account is protected",
      suspiciousActivity: "Suspicious Activity",
    },

    // ================= LANGUAGE =================
    language: {
      title: "Choose Your Language",
      subtitle:
        "Select your preferred language for the entire FinGuru experience.",
      personalize: "PERSONALIZE YOUR EXPERIENCE",
      currentLanguage: "CURRENT LANGUAGE",
      availableLanguages: "AVAILABLE LANGUAGES",
      selectPreferred:
        "Select your preferred language",
      languageSaved:
        "Your language preference is saved automatically.",
      copilotNote:
        "Your selected language will also be used by FinGuru AI Copilot.",
      english: "English",
      hindi: "Hindi",
      kannada: "Kannada",
      telugu: "Telugu",
      tamil: "Tamil",
      malayalam: "Malayalam",
      marathi: "Marathi",
      bengali: "Bengali",
    },

    // ================= PROFILE =================
    profile: {
      title: "Profile",
      personalInformation: "Personal Information",
      name: "Name",
      mobile: "Mobile Number",
      email: "Email",
      city: "City",
      occupation: "Occupation",
      account: "Account",
    },

    // ================= PRIVACY =================
    privacy: {
      title: "Privacy & Consent",
      subtitle:
        "Control how FinGuru uses your financial information.",
      financialAnalysis: "Financial Analysis",
      financialAdvice: "Financial Advice",
      loanRecommendation: "Loan Recommendations",
      fraudDetection: "Fraud Detection",
      responsibleAI: "Responsible AI",
      consentRequired:
        "Your consent is required before personalized financial advice can be provided.",
      personalizedAdvice:
        "Personalized Advice",
    },
  },

  // =========================================================
  // HINDI
  // =========================================================

  hi: {
    common: {
      back: "वापस",
      backToDashboard: "डैशबोर्ड पर वापस जाएँ",
      save: "सहेजें",
      cancel: "रद्द करें",
      confirm: "पुष्टि करें",
      close: "बंद करें",
      loading: "लोड हो रहा है...",
      selected: "चयनित",
      active: "सक्रिय",
      enabled: "सक्षम",
      disabled: "अक्षम",
      yes: "हाँ",
      no: "नहीं",
      viewAll: "सभी देखें",
      learnMore: "और जानें",
      continue: "जारी रखें",
      submit: "जमा करें",
      success: "सफल",
      error: "त्रुटि",
    },

    brand: {
      name: "FinGuru",
      tagline: "AI-संचालित व्यक्तिगत वित्त",
    },

    nav: {
      dashboard: "डैशबोर्ड",
      money: "पैसे",
      financialHealth: "वित्तीय स्वास्थ्य",
      advice: "AI सलाह",
      copilot: "AI सहायक",
      loans: "ऋण",
      simulator: "सिम्युलेटर",
      transactions: "लेन-देन",
      goals: "लक्ष्य",
      security: "सुरक्षा",
      language: "भाषा",
      profile: "प्रोफ़ाइल",
      privacy: "गोपनीयता",
      settings: "सेटिंग्स",
      logout: "लॉग आउट",
    },

    dashboard: {
      title: "वित्तीय डैशबोर्ड",
      welcome: "वापसी पर स्वागत है",
      overview: "यहाँ आपका वित्तीय विवरण है",
      totalBalance: "कुल बैलेंस",
      monthlyIncome: "मासिक आय",
      monthlySpending: "मासिक खर्च",
      monthlySavings: "मासिक बचत",
      savingsRate: "बचत दर",
      financialHealth: "वित्तीय स्वास्थ्य",
      financialStress: "वित्तीय तनाव",
      recentTransactions: "हाल के लेन-देन",
      quickActions: "त्वरित कार्य",
      aiAdvice: "AI सलाह",
      askCopilot: "AI सहायक से पूछें",
      viewTransactions: "लेन-देन देखें",
      manageMoney: "पैसे प्रबंधित करें",
    },

    money: {
      title: "पैसे",
      overview: "अपने पैसे को समझें और प्रबंधित करें",
      balance: "बैलेंस",
      income: "आय",
      spending: "खर्च",
      savings: "बचत",
      expenses: "व्यय",
      categories: "खर्च की श्रेणियाँ",
      biggestExpense: "सबसे बड़ा खर्च",
      monthlyOverview: "मासिक विवरण",
      cashFlow: "नकदी प्रवाह",
    },

    health: {
      title: "वित्तीय स्वास्थ्य",
      score: "स्वास्थ्य स्कोर",
      excellent: "उत्कृष्ट",
      good: "अच्छा",
      moderate: "मध्यम",
      needsAttention: "ध्यान देने की आवश्यकता",
      incomeScore: "आय स्कोर",
      spendingScore: "खर्च स्कोर",
      savingsScore: "बचत स्कोर",
      debtScore: "ऋण स्कोर",
      stabilityScore: "स्थिरता स्कोर",
      strengths: "आपकी खूबियाँ",
      weaknesses: "सुधार के क्षेत्र",
      recommendations: "सुझाव",
      savingsRate: "बचत दर",
      monthlyIncome: "मासिक आय",
      monthlySpending: "मासिक खर्च",
      monthlySurplus: "मासिक अतिरिक्त राशि",
    },

    advice: {
      title: "आपके पैसे के लिए स्मार्ट सलाह",
      subtitle:
        "FinGuru AI आपके वित्तीय व्यवहार का विश्लेषण करता है और बचत, वृद्धि और सुरक्षा के लिए व्यक्तिगत सुझाव देता है।",
      personalizedGuidance: "व्यक्तिगत AI मार्गदर्शन",
      aiAnalysisComplete: "AI विश्लेषण पूरा हुआ",
      finGuruAI: "FINGURU AI",
      recommendationHeading:
        "आपके लिए मेरी सलाह",
      personalizedRecommendations:
        "व्यक्तिगत सुझाव",
      nextBestActions: "आपके अगले सर्वोत्तम कदम",
      exploreRecommendation: "सुझाव देखें",

      increaseSavings: "मासिक बचत बढ़ाएँ",
      increaseSavingsDescription:
        "आपकी वर्तमान बचत दर अच्छी है। मासिक बचत बढ़ाने से आपके वित्तीय लक्ष्यों को जल्दी पूरा करने में मदद मिल सकती है।",

      emergencyFund: "आपातकालीन निधि बनाएँ",
      emergencyFundDescription:
        "6 महीने की बचत का रिज़र्व आपकी वित्तीय सुरक्षा को और मजबूत कर सकता है।",

      investConsistently: "नियमित निवेश करें",
      investConsistentlyDescription:
        "दीर्घकालिक संपत्ति बनाने के लिए नियमित निवेश जारी रखने पर विचार करें।",

      stayOnGoal: "लक्ष्य पर बने रहें",
      stayOnGoalDescription:
        "अपनी वर्तमान बचत की आदत बनाए रखने से आप अपने लक्ष्यों पर बने रह सकते हैं।",

      highImpact: "उच्च प्रभाव",
      recommended: "अनुशंसित",
      longTerm: "दीर्घकालिक",
      onTrack: "सही दिशा में",

      actionPlan: "FINGURU कार्य योजना",
      monthlyPlan: "आपकी मासिक वित्तीय योजना",
      smartTip: "स्मार्ट मनी टिप",
      smallImprovements:
        "छोटे सुधार समय के साथ बड़ा प्रभाव डालते हैं।",
      buildHabits:
        "सिर्फ बैलेंस नहीं, अच्छी आदतें बनाएँ।",
    },

    copilot: {
      title: "FinGuru AI सहायक",
      subtitle: "आपका AI-संचालित व्यक्तिगत वित्त सहायक",
      aiConnected: "AI कनेक्टेड",
      spending: "खर्च",
      spendingDescription: "अपने खर्चों को ट्रैक करें",
      financialHealth: "वित्तीय स्वास्थ्य",
      healthDescription: "अपना स्कोर समझें",
      aiGuidance: "AI मार्गदर्शन",
      guidanceDescription: "व्यक्तिगत जानकारी प्राप्त करें",
      responsibleAI: "जिम्मेदार AI",
      responsibleDescription: "गोपनीयता-सचेत सलाह",
      tryAsking: "यह पूछकर देखें",
      placeholder:
        "अपने वित्त के बारे में FinGuru से कुछ भी पूछें...",
      analyzing:
        "आपकी वित्तीय जानकारी का विश्लेषण किया जा रहा है...",
      basedOnData:
        "आपके FinGuru वित्तीय डेटा पर आधारित",
      disclaimer:
        "FinGuru Copilot AI द्वारा तैयार वित्तीय मार्गदर्शन प्रदान करता है। यह पेशेवर वित्तीय सलाह का विकल्प नहीं है।",
    },

    loans: {
      title: "ऋण",
      loanAmount: "ऋण राशि",
      interestRate: "ब्याज दर",
      tenure: "ऋण अवधि",
      monthlyEMI: "मासिक EMI",
      totalInterest: "कुल ब्याज",
      totalPayment: "कुल भुगतान",
      calculate: "EMI की गणना करें",
      eligibility: "ऋण पात्रता",
      recommendation: "ऋण सुझाव",
    },

    transactions: {
      title: "लेन-देन",
      recent: "हाल के लेन-देन",
      all: "सभी लेन-देन",
      income: "आय",
      expense: "खर्च",
      merchant: "व्यापारी",
      category: "श्रेणी",
      amount: "राशि",
      date: "तारीख",
      description: "विवरण",
      noTransactions: "कोई लेन-देन नहीं मिला",
    },

    goals: {
      title: "वित्तीय लक्ष्य",
      savingsGoal: "बचत लक्ष्य",
      target: "लक्ष्य",
      progress: "प्रगति",
      remaining: "शेष",
      createGoal: "लक्ष्य बनाएँ",
      emergencyFund: "आपातकालीन निधि",
      investment: "निवेश",
      vacation: "छुट्टी",
      education: "शिक्षा",
    },

    security: {
      title: "सुरक्षा",
      secureAccount: "अपने खाते को सुरक्षित रखें",
      fraudDetection: "धोखाधड़ी का पता लगाना",
      incidents: "सुरक्षा घटनाएँ",
      protected: "आपका खाता सुरक्षित है",
      suspiciousActivity: "संदिग्ध गतिविधि",
    },

    language: {
      title: "अपनी भाषा चुनें",
      subtitle:
        "पूरे FinGuru अनुभव के लिए अपनी पसंदीदा भाषा चुनें।",
      personalize: "अपने अनुभव को व्यक्तिगत बनाएँ",
      currentLanguage: "वर्तमान भाषा",
      availableLanguages: "उपलब्ध भाषाएँ",
      selectPreferred: "अपनी पसंदीदा भाषा चुनें",
      languageSaved:
        "आपकी भाषा की पसंद अपने आप सहेजी जाती है।",
      copilotNote:
        "आपकी चुनी हुई भाषा का उपयोग FinGuru AI Copilot में भी किया जाएगा।",
      english: "अंग्रेज़ी",
      hindi: "हिंदी",
      kannada: "कन्नड़",
      telugu: "तेलुगु",
      tamil: "तमिल",
      malayalam: "मलयालम",
      marathi: "मराठी",
      bengali: "बंगाली",
    },

    profile: {
      title: "प्रोफ़ाइल",
      personalInformation: "व्यक्तिगत जानकारी",
      name: "नाम",
      mobile: "मोबाइल नंबर",
      email: "ईमेल",
      city: "शहर",
      occupation: "पेशा",
      account: "खाता",
    },

    privacy: {
      title: "गोपनीयता और सहमति",
      subtitle:
        "नियंत्रित करें कि FinGuru आपकी वित्तीय जानकारी का उपयोग कैसे करता है।",
      financialAnalysis: "वित्तीय विश्लेषण",
      financialAdvice: "वित्तीय सलाह",
      loanRecommendation: "ऋण सुझाव",
      fraudDetection: "धोखाधड़ी का पता लगाना",
      responsibleAI: "जिम्मेदार AI",
      consentRequired:
        "व्यक्तिगत वित्तीय सलाह देने से पहले आपकी सहमति आवश्यक है।",
      personalizedAdvice: "व्यक्तिगत सलाह",
    },
  },
};

export default translations;