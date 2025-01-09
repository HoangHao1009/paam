"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import saveAs from "file-saver";
import { toast } from "react-toastify";
import axios from "axios";
import UploadFile from "@/components/uploadFile";

const ExportPPTX = () => {
  const items = ["Setting", "Data", "PPTX"];

  const handleDownloadClick = async (type: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/report/${type}`, {
        responseType: "blob",
      });

      saveAs(response.data, `${type}_data.zip`);
      toast.success("Downloading success");
    } catch (error) {
      toast.error(`Downloading error: ${error}`);
    }
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-10">
        <CanvasNavBar items={items} current="report" />
        <UploadFile apiEndpoint="http://localhost:8000/report/pptx_template"></UploadFile>
        <div>
          <button
            className="relative rounded-lg bg-orange-400 p-3 font-semibold text-white hover:bg-orange-600"
            onClick={() => handleDownloadClick("pptx")}
          >
            Download PPTX
          </button>
        </div>
      </Canvas>
    </div>
  );
};

export default ExportPPTX;
