import React, { useEffect, useState } from "react";

export default function App() {
  const [msg, setMsg] = useState("Chargement...");

  useEffect(() => {
    fetch("/api/hello")
  .then((res) => res.json())
  .then((data) => setMsg(data.message))
  .catch(() => setMsg("Erreur: impossible de joindre le backend"));

  }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>Frontend</h1>
      <p>Message du backend :</p>
      <h2>{msg}</h2>
    </div>
  );
}
