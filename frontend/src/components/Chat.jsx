import { useState, useEffect, useRef } from "react";
import api from "../api";
import ChatInput from "./ChatInput";
import ReactMarkdown from "react-markdown";

const DocIcon = ({ size = 14 }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="#7F77DD"
    strokeWidth="2"
    width={size}
    height={size}
  >
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <path d="M14 2v6h6" />
    <path d="M9 13h6" />
    <path d="M9 17h6" />
  </svg>
);

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const upload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setMessages((p) => [
      ...p,
      { role: "user", type: "file", fileName: file.name },
    ]);

    const data = new FormData();
    data.append("file", file);
    setUploading(true);

    try {
      const res = await api.post("/pdf/upload", data);

      if (res.data.error) {
        setMessages((p) => [
          ...p,
          { role: "ai", type: "text", text: `⚠️ ${res.data.error}` },
        ]);
        return;
      }

      setMessages((p) => [
        ...p,
        {
          role: "ai",
          type: "text",
          text: "Your PDF has been processed and is ready. Ask me anything about it!",
        },
      ]);
    } catch (err) {
      const errMsg =
        err?.response?.data?.error ||
        "Failed to upload PDF. Please try again.";
      setMessages((p) => [
        ...p,
        { role: "ai", type: "text", text: `⚠️ ${errMsg}` },
      ]);
    } finally {
      setUploading(false);
    }
  };

  const send = async () => {
    if (!question.trim() || loading) return;
    const q = question;
    setQuestion("");
    setMessages((p) => [...p, { role: "user", type: "text", text: q }]);
    setLoading(true);

    try {
      const res = await api.post("/chat", { question: q });
      setMessages((p) => [
        ...p,
        { role: "ai", type: "text", text: res.data.answer },
      ]);
    } catch {
      setMessages((p) => [
        ...p,
        { role: "ai", type: "text", text: "Something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0 }}>
      <div style={{ flex: 1, overflowY: "auto", padding: "24px 16px 16px" }}>
        {messages.length === 0 && (
          <div
            style={{
              height: "100%",
              minHeight: "300px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              gap: "12px",
            }}
          >
            <div
              style={{
                width: 56,
                height: 56,
                borderRadius: 16,
                background: "rgba(127,119,221,0.12)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: 4,
              }}
            >
              <DocIcon size={28} />
            </div>
            <h1 style={{ fontSize: 36, fontWeight: 600, letterSpacing: "-0.5px", margin: 0 }}>
              QueryDocs
            </h1>
            <p style={{ fontSize: 15, color: "#9ca3af", margin: 0 }}>
              Upload a PDF and ask anything about it
            </p>
          </div>
        )}

        <div style={{ maxWidth: 640, margin: "0 auto", display: "flex", flexDirection: "column", gap: 12 }}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                display: "flex",
                justifyContent: m.role === "user" ? "flex-end" : "flex-start",
                alignItems: "flex-start",
              }}
            >
              {m.role === "ai" && (
                <div
                  style={{
                    width: 28,
                    height: 28,
                    borderRadius: "50%",
                    background: "rgba(127,119,221,0.15)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginRight: 8,
                    marginTop: 4,
                    flexShrink: 0,
                  }}
                >
                  <DocIcon size={14} />
                </div>
              )}

              <div
                style={{
                  maxWidth: "75%",
                  fontSize: 14,
                  lineHeight: 1.65,
                  padding: "10px 14px",
                  borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                  background: m.role === "user" ? "rgba(127,119,221,0.12)" : "rgba(255,255,255,0.05)",
                  border: m.role === "ai" ? "1px solid rgba(255,255,255,0.08)" : "none",
                }}
              >
                {m.type === "file" ? (
                  <div>
                    <div
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: 6,
                        background: "rgba(127,119,221,0.15)",
                        color: "#a89fe8",
                        fontSize: 12,
                        fontWeight: 500,
                        padding: "4px 10px",
                        borderRadius: 20,
                        marginBottom: 6,
                      }}
                    >
                      <DocIcon size={11} />
                      {m.fileName}
                    </div>
                    <p style={{ fontSize: 12, color: "#6b7280", margin: 0 }}>PDF uploaded</p>
                  </div>
                ) : (
                  <ReactMarkdown>{m.text}</ReactMarkdown>
                )}
              </div>
            </div>
          ))}

          {(loading || uploading) && (
            <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start" }}>
              <div
                style={{
                  width: 28,
                  height: 28,
                  borderRadius: "50%",
                  background: "rgba(127,119,221,0.15)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginRight: 8,
                  marginTop: 4,
                  flexShrink: 0,
                }}
              >
                <DocIcon size={14} />
              </div>
              <div
                style={{
                  padding: "12px 16px",
                  borderRadius: "18px 18px 18px 4px",
                  background: "rgba(255,255,255,0.05)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  display: "flex",
                  gap: 4,
                  alignItems: "center",
                }}
              >
                {[0, 150, 300].map((delay) => (
                  <span
                    key={delay}
                    style={{
                      width: 6,
                      height: 6,
                      borderRadius: "50%",
                      background: "#6b7280",
                      display: "inline-block",
                      animation: `bounce 1.2s ${delay}ms infinite`,
                    }}
                  />
                ))}
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      <ChatInput
        question={question}
        setQuestion={setQuestion}
        send={send}
        upload={upload}
        loading={loading || uploading}
      />

      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-5px); }
        }
        .prose { color: inherit; }
        .prose p { margin: 0 0 8px 0; }
        .prose p:last-child { margin: 0; }
        .prose ul, .prose ol { margin: 4px 0 8px 16px; padding: 0; }
        .prose li { margin-bottom: 2px; }
        .prose code { background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-size: 13px; }
        .prose pre { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; overflow-x: auto; }
        .prose strong { color: inherit; }
      `}</style>
    </div>
  );
}