"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import { ChangeEvent } from "react";
import { useState } from "react";
import axios from "axios";
import { AxiosResponse } from "axios";

import { toast } from "react-toastify";

const Provider = () => {
  const items = ['Provider', 'Questions']

  const [surveyRequest, setSurveyRequest] = useState({
    surveyId: "",
    apiKey: "",
    srcPlatform: "questionpro",
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSurveyRequest((prev) => ({ ...prev, [name]: value }));
  };

  const handleOnClick = async (e: React.FormEvent) => {
    e.preventDefault();

    setIsLoading(true);
    try {
      const response: AxiosResponse = await axios.post(
        "http://localhost:8000/survey",
        surveyRequest,
      );
      toast.success("Create survey success");
    } catch (error) {
      toast.error("Create survey failed");
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div>
      <Canvas className="flex flex-col gap-10 pl-10">
        <CanvasNavBar items={items} current="survey" className="font-sans font-semibold text-lg"/>
        <form className="flex flex-col gap-5 pl-5">
          <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
            <p className="w-16">Survey ID</p>
            <input
              type="text"
              name="surveyId"
              className="h-7 w-40 rounded-md border-2 border-gray-300"
              onChange={handleOnChange}
            />
          </label>
          <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
            <p className="w-16">API Key</p>
            <input
              type="text"
              name="apiKey"
              className="h-7 w-40 rounded-md border-2 border-gray-300"
              onChange={handleOnChange}
            />
          </label>
          <button
            className="h-10 w-24 rounded-md bg-slate-600 text-sm font-semibold text-white"
            onClick={handleOnClick}
          >
            {isLoading ? "Loading..." : "Get Survey"}
          </button>
        </form>
      </Canvas>
    </div>
  );
};

export default Provider;
