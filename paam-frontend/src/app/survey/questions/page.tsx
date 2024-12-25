"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import axios from "axios";
import { AxiosResponse } from "axios";
import { useState, useEffect } from "react";
import Question from "@/components/question";

const Questions = () => {
  const items = ["Provider", "Questions"];
  const [questions, setQuestions] = useState<any[]>([]);

  useEffect(() => {
    const fetchQuestions = async () => {
      const response: AxiosResponse = await axios.get(
        "http://localhost:8000/survey/questions",
      );
      setQuestions(response.data.questionData);
    };
    fetchQuestions();
  }, []);

  return (
    <div>
      <Canvas className="flex flex-col gap-10">
        <CanvasNavBar items={items} current="survey" />
        <div className="flex h-[350px] flex-col gap-5 overflow-y-auto pl-5">
          {questions.map((questions, index) => (
            <div key={index}>
              <Question {...questions} />
            </div>
          ))}
        </div>
      </Canvas>
    </div>
  );
};

export default Questions;
