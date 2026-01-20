import React, { useEffect, useState } from "react";

async function api(path, options) {
  const res = await fetch(path, options);
  const txt = await res.text();
  let data = {};
  try { data = txt ? JSON.parse(txt) : {}; } catch { data = { raw: txt }; }
  if (!res.ok) throw new Error(data?.error || `HTTP ${res.status}`);
  return data;
}

export default function App() {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState("");

  const [cUser, setCUser] = useState("");
  const [cPass, setCPass] = useState("");

  const [uId, setUId] = useState("");
  const [uPass, setUPass] = useState("");

  const [dId, setDId] = useState("");

  async function refresh() {
    try {
      const data = await api("/api/users");
      setUsers(data.users || []);
      setStatus("OK");
    } catch (e) {
      setStatus(`Erreur: ${e.message}`);
    }
  }

  useEffect(() => { refresh(); }, []);

  async function createUser(e) {
    e.preventDefault();
    try {
      await api("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: cUser, password: cPass })
      });
      setCUser(""); setCPass("");
      await refresh();
    } catch (e2) { setStatus(`Create: ${e2.message}`); }
  }

  async function updateUser(e) {
    e.preventDefault();
    try {
      await api(`/api/users/${encodeURIComponent(uId)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: uPass })
      });
      setUId(""); setUPass("");
      await refresh();
    } catch (e2) { setStatus(`Update: ${e2.message}`); }
  }

  async function deleteUser(e) {
    e.preventDefault();
    try {
      await api(`/api/users/${encodeURIComponent(dId)}`, { method: "DELETE" });
      setDId("");
      await refresh();
    } catch (e2) { setStatus(`Delete: ${e2.message}`); }
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24, maxWidth: 900 }}>
      <h1>Exo4 — PostgreSQL Stack</h1>
      <p>Status: <b>{status}</b></p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
        <form onSubmit={createUser} style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
          <h2>Create</h2>
          <input placeholder="username" value={cUser} onChange={(e)=>setCUser(e.target.value)} style={{ width:"100%", marginBottom: 8 }} />
          <input placeholder="password" value={cPass} onChange={(e)=>setCPass(e.target.value)} style={{ width:"100%", marginBottom: 8 }} />
          <button type="submit">Create</button>
        </form>

        <form onSubmit={updateUser} style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
          <h2>Update (by id)</h2>
          <input placeholder="id" value={uId} onChange={(e)=>setUId(e.target.value)} style={{ width:"100%", marginBottom: 8 }} />
          <input placeholder="new password" value={uPass} onChange={(e)=>setUPass(e.target.value)} style={{ width:"100%", marginBottom: 8 }} />
          <button type="submit">Update</button>
        </form>

        <form onSubmit={deleteUser} style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
          <h2>Delete (by id)</h2>
          <input placeholder="id" value={dId} onChange={(e)=>setDId(e.target.value)} style={{ width:"100%", marginBottom: 8 }} />
          <button type="submit">Delete</button>
        </form>
      </div>

      <div style={{ marginTop: 20, border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
        <h2>Users (Read)</h2>
        <button onClick={refresh} style={{ marginBottom: 12 }}>Refresh</button>
        <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ textAlign: "left" }}>
              <th style={{ borderBottom: "1px solid #ddd" }}>id</th>
              <th style={{ borderBottom: "1px solid #ddd" }}>username</th>
              <th style={{ borderBottom: "1px solid #ddd" }}>password</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td style={{ borderBottom: "1px solid #eee" }}>{u.id}</td>
                <td style={{ borderBottom: "1px solid #eee" }}>{u.username}</td>
                <td style={{ borderBottom: "1px solid #eee" }}>{u.password}</td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr><td colSpan="3">Aucun utilisateur</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
