'use client';
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import React from "react";
import ChatFrame from "@/components/chat";
import { toast } from "react-toastify";

const AIChat = () => {
  const items = ["Crosstab", "Chat"];

  return (
    <div>
      <Canvas className="flex flex-col gap-5 items-start justify-start">
        <CanvasNavBar items={items} current="analyze"></CanvasNavBar>
        <ChatFrame ></ChatFrame>
      </Canvas>
    </div>
  );
};

export default AIChat;
