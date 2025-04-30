import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [knowledge, setKnowledge] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      if (data.reply) {
        const botMessage = { sender: "bot", text: data.reply };
        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      const errorMessage = { sender: "bot", text: "Error connecting to server." };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const uploadKnowledge = async () => {
    if (!knowledge.trim()) return;
    try {
      await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: new URLSearchParams({ text: knowledge }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      alert("Knowledge uploaded successfully!");
      setKnowledge("");
    } catch (error) {
      alert("Failed to upload knowledge.");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">💬 Chatbot Framework</h1>

      {/* Upload Knowledge Section */}
      <div className="w-full max-w-md bg-white p-4 rounded-lg shadow mb-6">
        <textarea
          className="w-full p-2 border rounded mb-2"
          rows="4"
          placeholder="Paste knowledge base content here..."
          value={knowledge}
          onChange={(e) => setKnowledge(e.target.value)}
        />
        <button
          onClick={uploadKnowledge}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 w-full"
        >
          Upload Knowledge
        </button>
      </div>

      {/* Chat Section */}
      <div className="w-full max-w-md bg-white rounded-lg shadow p-4 mb-4 overflow-y-auto h-96">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 p-2 rounded ${
              msg.sender === "user" ? "bg-blue-100 text-right" : "bg-gray-200 text-left"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="p-2 text-gray-400 italic text-center">Typing...</div>
        )}
      </div>

      <div className="flex w-full max-w-md">
        <input
          type="text"
          className="flex-1 p-2 border rounded-l"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 rounded-r hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  );
}
