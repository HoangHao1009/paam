"use client";
import { toast } from "react-toastify";
import { useState } from "react";
import { ChangeEvent } from "react";

interface UploadFileProps {
    apiEndpoint: string;
}

const UploadFile: React.FC<UploadFileProps> = ({apiEndpoint}) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null; // Lấy file đầu tiên (nếu có)
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      toast.warning("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        body: formData,
      });

      const responseData = await response.json();

      if (response.ok) {
        toast.success("File uploaded successfully!");
      } else {
        toast.error(`Failed to upload file. ${responseData.message}`);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="flex w-40 flex-col gap-5">
      <input
        type="file"
        onChange={handleFileChange}
        className="rounded-sm border border-black"
      ></input>
      <button
        onClick={handleUpload}
        className="rounded-2xl bg-blue-400 p-2 font-semibold text-white hover:bg-slate-700"
      >
        Upload
      </button>
    </div>
  );
};

export default UploadFile;
