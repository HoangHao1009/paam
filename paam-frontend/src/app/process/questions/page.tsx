"use client";
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import axios from "axios";
import { AxiosResponse } from "axios";
import { useState, useEffect } from "react";
import Question from "@/components/question";

const Questions = () => {
  const items = ["Questions"];
  const [questions, setQuestions] = useState<any[]>([]);

  useEffect(() => {
    const fetchQuestions = async () => {
      const response: AxiosResponse = await axios.get(
        "http://localhost:8000/process/questions",
      );
      setQuestions(response.data.questionData);
    };
    fetchQuestions();
  }, []);

  const handleDeleteQuestion = (deletedQuestionCode: string) => {
    setQuestions((prevQuestion) =>
      prevQuestion.filter(
        (question) => question.questionCode != deletedQuestionCode,
      ),
    );
  };

  const handleUpdateQuestion = async () => {
    // Gọi lại API để lấy danh sách mới
    const response: AxiosResponse = await axios.get(
      "http://localhost:8000/process/questions"
    );
    setQuestions(response.data.questionData);
  };

  return (
    <div>
      <Canvas className="flex flex-col gap-10">
        <CanvasNavBar items={items} current="process" />
        <div className="flex h-[400px] flex-col gap-5 overflow-y-auto pl-5">
          {questions.map((questions, index) => (
            <div key={index}>
              <Question {...questions} onDelete={handleDeleteQuestion} onUpdate={handleUpdateQuestion}/>
            </div>
          ))}
        </div>
      </Canvas>
    </div>
  );
};

export default Questions;
