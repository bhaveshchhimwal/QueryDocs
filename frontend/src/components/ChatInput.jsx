import { Plus, ArrowUp } from "lucide-react";

export default function ChatInput({ question, setQuestion, send, upload, loading }) {
  return (
    <div
      style={{
        padding: "12px 16px 16px",
        borderTop: "1px solid rgba(255,255,255,0.07)",
        background: "inherit",
        flexShrink: 0,
      }}
    >
      <div style={{ maxWidth: 640, margin: "0 auto" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            borderRadius: 20,
            border: "1px solid rgba(255,255,255,0.12)",
            padding: "8px 8px 8px 12px",
            background: "rgba(255,255,255,0.04)",
            transition: "border-color 0.15s",
          }}
          onFocus={(e) => e.currentTarget.style.borderColor = "rgba(127,119,221,0.6)"}
          onBlur={(e) => e.currentTarget.style.borderColor = "rgba(255,255,255,0.12)"}
        >
          <label
            style={{
              width: 32,
              height: 32,
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              flexShrink: 0,
              color: "#9ca3af",
              transition: "background 0.15s",
            }}
            title="Upload PDF"
            onMouseEnter={(e) => e.currentTarget.style.background = "rgba(255,255,255,0.08)"}
            onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
          >
            <Plus size={18} />
            <input hidden type="file" accept="application/pdf" onChange={upload} />
          </label>

          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
            placeholder="Ask anything about your PDF…"
            disabled={loading}
            style={{
              flex: 1,
              minWidth: 0,
              background: "transparent",
              border: "none",
              outline: "none",
              fontSize: 14,
              color: "inherit",
              fontFamily: "inherit",
            }}
          />

          <button
            onClick={send}
            disabled={!question.trim() || loading}
            style={{
              width: 32,
              height: 32,
              borderRadius: "50%",
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: question.trim() && !loading ? "pointer" : "not-allowed",
              background: question.trim() && !loading ? "#7F77DD" : "rgba(255,255,255,0.1)",
              color: question.trim() && !loading ? "#fff" : "#6b7280",
              flexShrink: 0,
              transition: "background 0.15s",
            }}
            aria-label="Send"
          >
            <ArrowUp size={16} />
          </button>
        </div>

        <p
          style={{
            textAlign: "center",
            fontSize: 11,
            color: "#4b5563",
            marginTop: 8,
          }}
        >
          © 2026 QueryDocs · All rights reserved
        </p>
      </div>
    </div>
  );
}