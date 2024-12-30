'use client';
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import React from "react";
import ChatFrame from "@/components/chat";
import { toast } from "react-toastify";

const AIChat = () => {
  const items = ["Chat", "Create"];

  const handleSendMessage = async (message: string): Promise<string> => {
    try {
      const response = await fetch("http://localhost:8000/ai/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        toast.error("Fail to fetch response");
      }

      const data = await response.json();
      return data.message;
    } catch (error) {
      toast.error(`Error when fetching ${error}`);
      return `ERROR ${error}`
    }
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-5 items-start justify-start">
        <CanvasNavBar items={items} current="ai"></CanvasNavBar>
        <ChatFrame onSend={handleSendMessage} title="Chatbot"></ChatFrame>
      </Canvas>
    </div>
  );
};

export default AIChat;
