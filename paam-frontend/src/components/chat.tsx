import { useState } from "react";
import { toast } from "react-toastify";

interface Message {
  sender: "user" | "bot";
  text: string;
}

interface ChatFrameProps {}

const ChatFrame: React.FC<ChatFrameProps> = () => {
  const [messages, setMessage] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSendMessage = async (message: string): Promise<void> => {
    try {
      const response = await fetch("http://localhost:8000/analyze/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        toast.error("Fail to fetch response");
        return;
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let partialText = "";

      const botMessage: Message = { sender: "bot", text: "" };
      setMessage((prev) => [...prev, botMessage]);

      while (!done) {
        const { value, done: readerDone } = (await reader?.read()) ?? {};
        done = readerDone || false;

        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          partialText += chunk;

          setMessage((prev) =>
            prev.map((msg, index) =>
              index === prev.length - 1 ? { ...msg, text: partialText } : msg,
            ),
          );
        }
      }
    } catch (error) {
      toast.error(`Error when fetching ${error}`);
      setMessage((prev) => [
        ...prev,
        { sender: "bot", text: `ERROR: ${error}` },
      ]);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: "user", text: input };
    setMessage((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      await handleSendMessage(input);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="mx-auto flex h-[450px] w-[95%] flex-col bg-white p-4 font-sans text-[10px]">
      <div className="mb-4 flex flex-1 flex-col overflow-y-scroll border p-2">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 break-words rounded p-2 text-black ${
              message.sender === "user"
                ? "ml-auto max-w-[70%] bg-blue-300 text-right"
                : "mr-auto max-w-[90%] break-words bg-gray-200 text-left"
            }`}
            dangerouslySetInnerHTML={{
              __html: message.text
                .replace(/\n+/g, '\n')
                .replace(/\n/g, "<br>")
            }}
          ></div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          className="flex-1 rounded border p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          disabled={loading}
        />
        <button
          className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default ChatFrame;
