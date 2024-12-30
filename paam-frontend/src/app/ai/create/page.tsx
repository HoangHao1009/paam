import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import { ChangeEvent } from "react";
import { useState } from "react";
const AICreate = () => {
  const items = ["Chat", "Create"];

  const [file, setFile] = useState<File | null>(null);

  const [response, setReponse] = useState<string>("");

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null; // Lấy file đầu tiên (nếu có)
    setFile(selectedFile);
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-10 font-sans">
        <CanvasNavBar items={items} current="ai"></CanvasNavBar>
        <div className="flex w-40 flex-col gap-5">
          <input type="file" onChange={handleFileChange} className="rounded-sm border border-black"></input>
          <button className="rounded-2xl bg-blue-400 p-2 font-semibold text-white hover:bg-slate-700">
            Extract Information
          </button>
        </div>
      </Canvas>
    </div>
  );
};

export default AICreate;
