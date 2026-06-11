import { useState, useEffect } from "react";
import Header from "./components/Header";
import Chat from "./components/Chat";

export default function App() {
  const [dark, setDark] = useState(true);

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

  const theme = {
    bg: dark ? "#0f0f0f" : "#f9fafb",
    surface: dark ? "#1a1a1a" : "#ffffff",
    surfaceHover: dark ? "#222222" : "#f3f4f6",
    border: dark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.1)",
    text: dark ? "#f3f4f6" : "#111827",
    textMuted: dark ? "#9ca3af" : "#6b7280",
    textFaint: dark ? "#4b5563" : "#9ca3af",
    inputBg: dark ? "rgba(255,255,255,0.04)" : "rgba(0,0,0,0.03)",
    userBubble: dark ? "rgba(127,119,221,0.15)" : "rgba(127,119,221,0.1)",
    aiBubble: dark ? "rgba(255,255,255,0.04)" : "#ffffff",
    aiBubbleBorder: dark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)",
    iconBg: dark ? "rgba(127,119,221,0.15)" : "rgba(127,119,221,0.1)",
    sendActive: "#7F77DD",
    sendInactive: dark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.08)",
    sendInactiveText: dark ? "#6b7280" : "#9ca3af",
  };

  return (
    <div
      style={{
        height: "100dvh",
        display: "flex",
        flexDirection: "column",
        background: theme.bg,
        color: theme.text,
        transition: "background 0.2s, color 0.2s",
      }}
    >
      <Header dark={dark} setDark={setDark} theme={theme} />
      <Chat theme={theme} />
    </div>
  );
}