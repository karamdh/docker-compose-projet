import React, { useEffect, useState } from "react";

export default function App() {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState("Chargement...");

  async function load() {
    try {
      setStatus("Chargement...");
      const res = await fetch("/api/users?results=12");
      const data = await res.json();
      setUsers(data.users || []);
      setStatus("OK");
    } catch (e) {
      setStatus("Erreur: impossible de récupérer les utilisateurs");
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>Exo3 — RandomUser via Tor</h1>
      <p>Status: <b>{status}</b></p>
      <button onClick={load} style={{ marginBottom: 16 }}>Rafraîchir</button>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16 }}>
        {users.map((u, i) => (
          <div key={i} style={{ border: "1px solid #ddd", borderRadius: 10, padding: 12 }}>
            <img src={u.photo} alt={u.name} style={{ width: "100%", borderRadius: 10 }} />
            <h3 style={{ marginTop: 10 }}>{u.name}</h3>
          </div>
        ))}
      </div>
    </div>
  );
}
