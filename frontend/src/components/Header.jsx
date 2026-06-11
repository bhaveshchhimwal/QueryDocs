import { Moon, Sun } from "lucide-react";
import Logo from "./Logo";

export default function Header({ dark, setDark }) {
  return (
    <header
      style={{
        height: 56,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 20px",
        borderBottom: "1px solid rgba(255,255,255,0.07)",
        flexShrink: 0,
      }}
    >
      <Logo />
      <button
        onClick={() => setDark(!dark)}
        style={{
          width: 32,
          height: 32,
          borderRadius: "50%",
          border: "1px solid rgba(255,255,255,0.1)",
          background: "transparent",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          color: "#9ca3af",
        }}
        aria-label="Toggle theme"
      >
        {dark ? <Sun size={16} /> : <Moon size={16} />}
      </button>
    </header>
  );
}