'use client';
import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";
import axios from "axios";
import { AxiosResponse } from "axios";
import { useState, useEffect } from "react";
import Question from "@/components/question";

const Questions = () => {
  const items = ['Provider', 'Questions'];
  const [questions, setQuestions] = useState<any[]>([]);

  useEffect(() => {
    const fetchQuestions = async () => {
      const response: AxiosResponse = await axios.get("http://localhost:8000/survey/questions");
      setQuestions(response.data.questionData);
    };
    fetchQuestions();
  }, []);

  return (
    <div>
        <Canvas className="flex flex-col gap-10 pl-10">
          <CanvasNavBar items={items} current="survey" className="font-sans font-semibold text-lg"/>
          <div className="flex flex-col gap-5 pl-5 h-[350px] overflow-y-auto">
            {questions.map((questions, index) => (
              <div key={index}>
                <Question {...questions}/>
              </div>
            ))
          }
          </div>
        </Canvas>
      
    </div>
  )
}

export default Questions
