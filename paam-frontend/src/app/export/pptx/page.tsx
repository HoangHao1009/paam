"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";


const ExportPPTX = () => {
  const items = ["Setting", "Data", "PPTX"];

  return (
    <div>
      <Canvas className="flex flex-col gap-10">
        <CanvasNavBar items={items} current="export" />
      </Canvas>
    </div>
  );
};

export default ExportPPTX;
