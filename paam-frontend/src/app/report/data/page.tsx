"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import axios from "axios";
import saveAs from "file-saver";
import { toast } from "react-toastify";

const ExportData = () => {
  const items = ["Setting", "Data", "PPTX"];

  const handleDownloadClick = async (type: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/report/${type}`, {
        responseType: "blob",
      });
      
      saveAs(response.data, `${type}_data.zip`);
      toast.success("Downloading success")
    } catch (error) {
      toast.error(`Downloading error: ${error}`);
    }
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-10">
        <CanvasNavBar items={items} current="report" />
        <div>
          <button
            className="relative rounded-lg bg-green-300 p-3 font-semibold text-slate-600 hover:bg-green-600 hover:text-white"
            onClick={() => handleDownloadClick('excel')}
          >
            Download Excel
          </button>
        </div>
        <div>
          <button
            className="relative rounded-lg bg-slate-400 text-white p-3 font-semibold hover:bg-slate-600 hover:text-black"
            onClick={() => handleDownloadClick('spss')}
          >
            Download SPSS
          </button>
        </div>
        <div>
          <button
            className="relative rounded-lg bg-yellow-300 p-3 font-semibold text-slate-600 hover:bg-yellow-600 hover:text-white"
            onClick={() => handleDownloadClick('datasets')}
          >
            Download Datasets
          </button>
        </div>
      </Canvas>
    </div>
  );
};

export default ExportData;
