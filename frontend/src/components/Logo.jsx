export default function Logo() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div
        style={{
          width: 28,
          height: 28,
          borderRadius: 8,
          background: "rgba(127,119,221,0.15)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#7F77DD"
          strokeWidth="2"
          width="16"
          height="16"
        >
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <path d="M14 2v6h6" />
          <path d="M9 13h6" />
          <path d="M9 17h6" />
        </svg>
      </div>
      <span style={{ fontSize: 15, fontWeight: 600, letterSpacing: "-0.2px" }}>
        QueryDocs
      </span>
    </div>
  );
}