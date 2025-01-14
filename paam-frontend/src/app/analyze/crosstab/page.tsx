"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";

import { ChangeEvent, useState } from "react";
import axios from "axios";

const Crosstab = () => {
  const items = ["Crosstab", "PPTX"];

  const [ctabRequest, setCtabRequest] = useState({
    base: "",
    target: "",
    deepBy: [],
    alpha: "",
    pct: false,
  });

  const [ctabData, setCtabData] = useState("");

  const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;

    const processedValue = type === "checkbox" ? checked : value;

    setCtabRequest((prev) => ({ ...prev, [name]: processedValue }));
  };

  const handleClick = async (e: React.FormEvent) => {
    e.preventDefault();

    const response = await axios.post(
      "http://localhost:8000/analyze/crosstab/",
      ctabRequest,
    );
    const ctabData = response.data.crosstabData;
    setCtabData(ctabData);
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-2">
        <CanvasNavBar items={items} current="analyze" />
        <form className="mb-5 flex flex-row items-center gap-5 font-sans text-sm font-semibold">
          <div className="flex flex-row items-center gap-5">
            <label className="flex flex-row items-center gap-2">
              Base Question:
              <input
                type="text"
                name="base"
                className="h-7 w-10 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
            <label className="flex flex-row items-center gap-2">
              Target Question:
              <input
                type="text"
                name="target"
                className="h-7 w-10 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
          </div>
          <div className="flex flex-row items-center gap-5">
            <label className="flex flex-row items-center gap-2">
              ALPHA:
              <input
                type="text"
                name="alpha"
                placeholder="0.05"
                // defaultValue="0.05"
                className="h-7 w-10 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
            <label className="flex flex-row items-center gap-2">
              PERCENTAGE:
              <input
                type="checkbox"
                name="pct"
                checked={ctabRequest.pct}
                className="h-6 w-6 cursor-pointer"
                onChange={handleOnChange}
              />
            </label>
          </div>

          <button
            className="rounded-3xl bg-slate-400 px-4 py-2 font-bold text-white hover:bg-slate-900"
            onClick={handleClick}
          >
            Submit{" "}
          </button>
        </form>
        <div
          className=""
          dangerouslySetInnerHTML={{ __html: ctabData }}
        />
      </Canvas>
    </div>
  );
};

export default Crosstab;
