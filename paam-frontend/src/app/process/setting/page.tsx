"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import axios, { AxiosResponse } from "axios";
import { ChangeEvent, useState } from "react";
import { toast } from "react-toastify";

const ExportSetting = () => {
  const items = ["Questions", "Setting", "Data"];

  const [exportSettingRequest, setexportSettingRequest] = useState({
    controlVars: [],
    targetVars: [],
    deepVars: [],
  });

  const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    let parseValue;

    try {
      parseValue = value ? JSON.parse(value) : value;
    } catch {
      parseValue = value;
    }

    setexportSettingRequest((prev) => ({ ...prev, [name]: parseValue }));
  };

  const handleOnClick = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response: AxiosResponse = await axios.post(
        "http://localhost:8000/report/settings",
        exportSettingRequest,
      );
      toast.success(`Message: ${response.data.message}`);
    } catch (error) {
      toast.error(`Error when Set export config ${e}`);
    }
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-10">
        <CanvasNavBar items={items} current="process" />
        <form className="flex flex-col gap-5 pl-5">
          <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
            <p className="w-28">Control Variables</p>
            <input
              type="text"
              name="controlVars"
              className="h-7 w-40 rounded-md border-2 border-gray-300"
              onChange={handleOnChange}
            />
          </label>
          <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
            <p className="w-28">Target Variables</p>
            <input
              type="text"
              name="targetVars"
              className="h-7 w-40 rounded-md border-2 border-gray-300"
              onChange={handleOnChange}
            />
          </label>
          <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
            <p className="w-28">Deep Variables</p>
            <input
              type="text"
              name="deepVars"
              className="h-7 w-40 rounded-md border-2 border-gray-300"
              onChange={handleOnChange}
            />
          </label>
          <button
            className="h-10 w-24 rounded-md bg-slate-600 text-sm font-semibold text-white"
            onClick={handleOnClick}
          >
            Set
          </button>
        </form>
      </Canvas>
    </div>
  );
};

export default ExportSetting;
