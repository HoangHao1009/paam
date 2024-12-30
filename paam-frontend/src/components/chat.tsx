import { useState } from "react";
import { toast } from "react-toastify";

interface Message {
  sender: "user" | "bot";
  text: string;
}

interface ChatFrameProps {
  onSend: (message: string) => Promise<string>; // No 'undefined' allowed
  title?: string;
}

const ChatFrame: React.FC<ChatFrameProps> = ({ onSend, title = "Chat" }) => {
  const [messages, setMessage] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: "user", text: input };
    setMessage((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const botReply = await onSend(input); // Pass a non-empty string
      const botMessage: Message = { sender: "bot", text: botReply };
      setMessage((prev) => [...prev, botMessage]);
    } catch (error) {
      toast.error(`Bot can not reply ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col w-full h-[400px] mx-auto border rounded-lg shadow-lg p-4 bg-white">
      <h2 className="text-lg font-bold mb-2">{title}</h2>
      <div className="flex-1 overflow-y-auto border p-2 mb-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-2 mb-2 rounded ${
              message.sender === 'user' ? 'bg-slate-500 ml-44 text-white w-3/4' : 'bg-gray-200 text-black w-3/4'
            }`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          className="flex-1 border rounded p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={loading}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatFrame;
