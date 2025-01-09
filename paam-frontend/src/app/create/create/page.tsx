"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import { ChangeEvent } from "react";
import { useState } from "react";
import { toast } from "react-toastify";
import axios from "axios";
import { AxiosResponse } from "axios";
import UploadFile from "@/components/uploadFile";

const AICreate = () => {
  const items = ["Provider", "Create"];

  const [createRequest, setCreateRequest] = useState({
    surveyId: "",
  });

  const handleCreate = async () => {
    try {
      const response: AxiosResponse = await axios.post(
        "http://localhost:8000/create/create",
        createRequest,
        {
          headers: {
            "Content-Type": "application/json", // Chỉ định Content-Type là application/json
          },
        },
      );

      toast.success(`Create Survey successfully: ${createRequest.surveyId}`);
    } catch (error) {
      toast.error(
        `Failed to create Survey ${createRequest.surveyId}: ${error}`,
      );
    }
  };

  const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCreateRequest((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-10 font-sans">
        <CanvasNavBar items={items} current="create"></CanvasNavBar>
        <div className="flex w-40 flex-col gap-5">
          <UploadFile apiEndpoint="http://localhost:8000/create/upload/"/>
          <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
            <p className="w-16">Survey ID</p>
            <input
              type="text"
              name="survey_id"
              className="h-7 w-40 rounded-md border-2 border-gray-300"
              onChange={handleOnChange}
            />
          </label>
          <button
            onClick={handleCreate}
            className="rounded-2xl bg-red-400 p-2 font-semibold text-white hover:bg-slate-700"
          >
            Create
          </button>
        </div>
      </Canvas>
    </div>
  );
};

export default AICreate;
