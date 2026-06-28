"use client";
import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") {
      setIsDark(true);
      applyTheme(true);
    }
  }, []);

  const applyTheme = (dark: boolean) => {
    const root = document.documentElement;
    if (dark) {
      root.style.backgroundColor = "#09090b";
      root.style.color = "#fafafa";
      document.body.style.backgroundColor = "#09090b";
      document.body.style.color = "#fafafa";
    } else {
      root.style.backgroundColor = "#ffffff";
      root.style.color = "#0a0a0a";
      document.body.style.backgroundColor = "#ffffff";
      document.body.style.color = "#0a0a0a";
    }
  };

  const toggle = () => {
    const newDark = !isDark;
    setIsDark(newDark);
    localStorage.setItem("theme", newDark ? "dark" : "light");
    applyTheme(newDark);
  };

  return (
    <button
      onClick={toggle}
      style={{
        position: "fixed",
        bottom: "24px",
        right: "24px",
        zIndex: 50,
        width: "56px",
        height: "56px",
        borderRadius: "50%",
        backgroundColor: isDark ? "#1a1a1a" : "#f5f5f5",
        border: isDark ? "1px solid #333" : "1px solid #ddd",
        cursor: "pointer",
        fontSize: "24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      {isDark ? "☀️" : "🌙"}
    </button>
  );
}
