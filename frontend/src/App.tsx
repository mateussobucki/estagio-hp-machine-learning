import { useEffect, useRef, useState } from "react";
import "./App.css";

type Msg = { role: "user" | "bot"; text: string };

const sessionId = crypto.randomUUID();

export default function App() {
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, loading]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setMsgs((m) => [...m, { role: "user", text }]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message: text }),
      });
      const data = await res.json();
      const reply = data.reply;
        data.response ?? data.reply ?? data.answer ?? data.message ?? JSON.stringify(data);
      setMsgs((m) => [...m, { role: "bot", text: reply }]);
    } catch {
      setMsgs((m) => [...m, { role: "bot", text: "Erro ao conectar com a API." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <h2>GPU Assistant</h2>
      <div className="chat">
        {msgs.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.text}
          </div>
        ))}
        {loading && (
          <div className="msg bot typing">
            <span />
            <span />
            <span />
          </div>
        )}
        <div ref={endRef} />
      </div>
      <div className="input-row">
        <input
          value={input}
          placeholder="Pergunte sobre GPUs..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button onClick={send} disabled={loading}>
          Enviar
        </button>
      </div>
    </div>
  );
}