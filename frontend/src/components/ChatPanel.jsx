import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../api";

const SUGGESTIONS = [
  "What are the major expense categories?",
  "Tell me about investment transactions",
  "Summarize the travel expenses",
  "What EMI payments are there?",
  "How much did I spend on food?",
];

export default function ChatPanel({ status }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () =>
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });

  useEffect(scrollToBottom, [messages, loading]);

  const send = async (text) => {
    const trimmed = (text || input).trim();
    if (!trimmed || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendMessage(trimmed);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `⚠️ ${err.message}` },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  const clearChat = () => setMessages([]);

  const isReady = status?.vectorstore_ready && status?.api_key_set;

  return (
    <div className="main-content">
      {/* Header */}
      <header className="chat-header">
        <div className="chat-header-left">
          <h1 className="gradient-text">Financial Assistant</h1>
          <span
            className={`chat-header-badge ${
              isReady ? "badge-ready" : "badge-offline"
            }`}
          >
            <span
              className={`status-dot ${isReady ? "green" : "red"}`}
            />
            {isReady ? "Online" : "Offline"}
          </span>
        </div>
        {messages.length > 0 && (
          <button className="btn btn-ghost btn-sm" onClick={clearChat}>
            🗑️ Clear
          </button>
        )}
      </header>

      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 && !loading ? (
          <div className="chat-empty">
            <div className="chat-empty-icon">💬</div>
            <div className="chat-empty-title">
              Ask anything about your transactions
            </div>
            <div className="chat-empty-subtitle">
              Upload your financial data in the sidebar, then start asking
              questions. The AI will search your documents and provide
              accurate answers.
            </div>
            <div className="suggested-prompts">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  className="suggested-prompt"
                  onClick={() => send(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`message ${msg.role}`}
                style={{ animationDelay: `${Math.min(i * 50, 300)}ms` }}
              >
                <div className="message-avatar">
                  {msg.role === "user" ? "👤" : "🤖"}
                </div>
                <div className="message-body">
                  {msg.content.split("\n").map((line, li) => (
                    <span key={li}>
                      {line}
                      {li < msg.content.split("\n").length - 1 && <br />}
                    </span>
                  ))}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-body">
                  <div className="typing-indicator">
                    <span className="typing-dot" />
                    <span className="typing-dot" />
                    <span className="typing-dot" />
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="chat-input-wrap">
        <div className="chat-input-inner">
          <textarea
            ref={inputRef}
            className="chat-input-field"
            placeholder={
              isReady
                ? "Ask about your transactions…"
                : "Configure API key & upload data to start…"
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={!isReady}
          />
          <button
            className="chat-send-btn"
            onClick={() => send()}
            disabled={!input.trim() || loading || !isReady}
            title="Send message"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}
