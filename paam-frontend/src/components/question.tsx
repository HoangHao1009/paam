"use client";

import { useState } from "react";

interface AnswerProps {
  answerCode: string;
  answerScale: number;
  answerText: string;
  answerRespondents: Array<string>;
}

interface QuestionProps {
  questionCode: string;
  questionText: string;
  questionType: "sa" | "ma" | "text";
  questionRespondents: Array<string>;
  questionAnswers: Array<AnswerProps>;
}

const Question = ({
  questionCode,
  questionText,
  questionType,
  questionRespondents,
  questionAnswers,
}: QuestionProps) => {
  const bgColor = {
    sa: "bg-pink-200",
    ma: "bg-blue-200",
    text: "bg-green-200",
  };
  const [showAnswers, setShowAnswers] = useState(false);

  return (
    <div className="flex w-[80%] flex-col gap-2 rounded-3xl border-2 border-black p-2 font-sans">
      <div className="mt-2 flex flex-row items-center gap-2">
        <div className="">
          <p className="mr-5 rounded-3xl bg-black p-2 font-semibold text-white">
            {questionCode}
          </p>
        </div>
        <div className="flex flex-col justify-center gap-2">
          <div
            dangerouslySetInnerHTML={{ __html: questionText }}
            className="text-base font-semibold"
          />
          <div className="flex flex-row items-center gap-2">
            <p className={`${bgColor[questionType]} rounded-md px-1`}>
              {questionType}
            </p>
            <p className="rounded-md bg-purple-300 px-1">
              n: {questionRespondents.length}
            </p>
          </div>
        </div>
      </div>
      <div className="ml-5 flex flex-row gap-2">
        <button
          onClick={() => setShowAnswers((prev) => !prev)}
          className="mt-2 self-start rounded-md bg-blue-400 p-1 text-xs font-semibold text-white hover:bg-blue-500"
        >
          {showAnswers ? "Hide Answers" : "Show Answers"}
        </button>
        <button className="mt-2 self-start rounded-md bg-orange-400 p-1 text-xs font-semibold text-white hover:bg-orange-500">
          Compute
        </button>
        <button className="mt-2 self-start rounded-md bg-red-400 p-1 text-xs font-semibold text-white hover:bg-red-500">
          Delete
        </button>
      </div>
      {showAnswers && (
        <div className="ml-10 mt-5 flex flex-col gap-2">
          {questionAnswers.map((answer, index) => (
            <div key={index} className="flex flex-row items-center gap-2">
              <p className="mr-5 rounded-3xl bg-teal-800 p-1 text-sm font-semibold text-white">
                {answer.answerCode}
              </p>
              <div>
                <div
                  dangerouslySetInnerHTML={{ __html: answer.answerText }}
                  className="text-sm"
                />
                <p className="inline-block rounded-md bg-purple-300 px-1 text-xs">
                  n: {answer.answerRespondents.length}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Question;
