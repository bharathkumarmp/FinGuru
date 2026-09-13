import { useState } from "react";
import {
  Bot,
  Send,
  User,
  Sparkles,
  TrendingUp,
  Wallet,
  ShieldCheck,
  Loader2,
  AlertCircle,
} from "lucide-react";

import { copilotRequest } from "../../services/api";
import "./Copilot.css";

const CUSTOMER_ID = 1;

const suggestedQuestions = [
  "How much did I spend and what was my biggest expense?",
  "How healthy are my finances?",
  "How much did I spend on shopping?",
  "Can I afford a ₹20,000 EMI?",
  "Why is my financial recommendation SEEK_HELP?",
];

function formatAnswer(text) {
  if (!text) return "";

  return text
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export default function Copilot() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "assistant",
      text:
        "Hello! I'm FinGuru Copilot. I can answer questions about your spending, financial health, savings, transactions, and personalized financial guidance.",
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(text = message) {
    const question = text.trim();

    if (!question || loading) {
      return;
    }

    setError("");

    const userMessage = {
      id: Date.now(),
      role: "user",
      text: question,
    };

    setMessages((previous) => [...previous, userMessage]);
    setMessage("");
    setLoading(true);

    try {
      const response = await copilotRequest({
        customer_id: CUSTOMER_ID,
        message: question,
        language: "English",
        use_customer_context: true,
      });

      const answer =
        response?.answer ||
        response?.data?.answer ||
        "I couldn't generate an answer right now.";

      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        text: formatAnswer(answer),
        sources: response?.sources || [],
        customerContextUsed:
          response?.customer_context_used ?? true,
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (err) {
      console.error("FinGuru Copilot error:", err);

      setError(
        err?.message ||
          "Unable to connect to FinGuru Copilot. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    sendMessage();
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="copilot-page">
      <div className="copilot-shell">
        {/* Header */}
        <header className="copilot-header">
          <div className="copilot-title-group">
            <div className="copilot-icon">
              <Bot size={28} />
            </div>

            <div>
              <h1>FinGuru Copilot</h1>
              <p>
                Your AI-powered personal finance assistant
              </p>
            </div>
          </div>

          <div className="copilot-status">
            <span className="status-dot" />
            AI Connected
          </div>
        </header>

        {/* Quick capabilities */}
        <div className="copilot-capabilities">
          <div className="capability-card">
            <Wallet size={20} />
            <div>
              <strong>Spending</strong>
              <span>Track your expenses</span>
            </div>
          </div>

          <div className="capability-card">
            <TrendingUp size={20} />
            <div>
              <strong>Financial Health</strong>
              <span>Understand your score</span>
            </div>
          </div>

          <div className="capability-card">
            <Sparkles size={20} />
            <div>
              <strong>AI Guidance</strong>
              <span>Get personalized insights</span>
            </div>
          </div>

          <div className="capability-card">
            <ShieldCheck size={20} />
            <div>
              <strong>Responsible AI</strong>
              <span>Privacy-aware advice</span>
            </div>
          </div>
        </div>

        {/* Chat */}
        <main className="copilot-chat-card">
          <div className="chat-messages">
            {messages.map((item) => (
              <div
                key={item.id}
                className={`message-row ${item.role}`}
              >
                <div className="message-avatar">
                  {item.role === "assistant" ? (
                    <Bot size={19} />
                  ) : (
                    <User size={19} />
                  )}
                </div>

                <div className="message-content">
                  <div className="message-name">
                    {item.role === "assistant"
                      ? "FinGuru Copilot"
                      : "You"}
                  </div>

                  <div className="message-bubble">
                    {item.text.split("\n").map((line, index) => (
                      <span key={index}>
                        {line}
                        {index < item.text.split("\n").length - 1 && (
                          <br />
                        )}
                      </span>
                    ))}
                  </div>

                  {item.role === "assistant" &&
                    item.customerContextUsed && (
                      <div className="context-badge">
                        <ShieldCheck size={13} />
                        Based on your FinGuru financial data
                      </div>
                    )}

                  {item.sources?.length > 0 && (
                    <div className="sources">
                      <span>Knowledge sources:</span>

                      {item.sources.map((source, index) => (
                        <span
                          className="source-pill"
                          key={`${source}-${index}`}
                        >
                          {source}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row assistant">
                <div className="message-avatar">
                  <Bot size={19} />
                </div>

                <div className="message-content">
                  <div className="message-name">
                    FinGuru Copilot
                  </div>

                  <div className="message-bubble loading-bubble">
                    <Loader2
                      size={18}
                      className="loading-spinner"
                    />
                    Analyzing your financial information...
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="copilot-error">
                <AlertCircle size={18} />
                <span>{error}</span>
              </div>
            )}
          </div>

          {/* Suggestions */}
          <div className="suggestions-section">
            <div className="suggestions-title">
              <Sparkles size={15} />
              Try asking
            </div>

            <div className="suggestions">
              {suggestedQuestions.map((question) => (
                <button
                  key={question}
                  type="button"
                  className="suggestion-button"
                  onClick={() => sendMessage(question)}
                  disabled={loading}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          {/* Input */}
          <form
            className="copilot-input-area"
            onSubmit={handleSubmit}
          >
            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask FinGuru anything about your finances..."
              rows={1}
              disabled={loading}
            />

            <button
              type="submit"
              className="send-button"
              disabled={!message.trim() || loading}
              aria-label="Send message"
            >
              {loading ? (
                <Loader2
                  size={20}
                  className="loading-spinner"
                />
              ) : (
                <Send size={20} />
              )}
            </button>
          </form>

          <div className="copilot-disclaimer">
            FinGuru Copilot provides AI-generated financial guidance.
            It does not replace professional financial advice.
          </div>
        </main>
      </div>
    </div>
  );
}