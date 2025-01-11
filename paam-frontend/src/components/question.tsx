"use client";

import { ChangeEvent, useState } from "react";
import Modal from "./modal";
import { toast } from "react-toastify";
import axios from "axios";
import { AxiosResponse } from "axios";
import { useRouter } from "next/navigation";

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
  isConstructed: boolean;
  construction: Object;
  onDelete: (questionCode: string) => void;
  onUpdate: () => void;
}

const Question = ({
  questionCode,
  questionText,
  questionType,
  questionRespondents,
  questionAnswers,
  isConstructed,
  construction,
  onDelete,
  onUpdate,
}: QuestionProps) => {
  const bgColor = {
    sa: "bg-pink-200",
    ma: "bg-blue-200",
    text: "bg-green-200",
  };

  const router = useRouter();

  const [showAnswers, setShowAnswers] = useState(false);

  const [isModalOpen, setIsModalOpen] = useState(false);

  const [computeRequest, setComputeRequest] = useState({
    method: "",
    rootQuestionCode: questionCode,
    newQuestionCode: "",
    newQuestionText: "",
    construction: "",
    by: "",
  });

  const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setComputeRequest((prev) => ({ ...prev, [name]: value }));
  };

  const handleOnClick = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response: AxiosResponse = await axios.post(
        "http://localhost:8000/process/compute/",
        computeRequest,
      );
      toast.success("Compute success");
    } catch (error) {
      toast.error("Compute failed");
    } finally {
      onUpdate()
      setIsModalOpen(false)
    }
  };

  const handleDelete = async () => {
    try {
      const response: AxiosResponse = await axios.post(
        "http://localhost:8000/process/delete/",
        {questionCode: questionCode},
      );
      toast.success("Delete success");
      onDelete(questionCode)
    } catch {
      toast.error("Delete failed");
    } finally {
      router.refresh();
    }
  };

  return (
    <div className="flex w-[80%] flex-col gap-2 rounded-3xl border-2 border-black p-2 font-sans">
      <div className="mt-2 flex flex-row items-center gap-2">
        <div className="">
          <p
            className={`${!isConstructed ? "bg-black" : "bg-green-400"} mr-5 rounded-3xl p-2 font-semibold text-white`}
          >
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
        <button
          className="mt-2 self-start rounded-md bg-orange-400 p-1 text-xs font-semibold text-white hover:bg-orange-500"
          onClick={() => setIsModalOpen(true)}
        >
          Compute
        </button>
        {isConstructed && (
          <button className="mt-2 self-start rounded-md bg-red-400 p-1 text-xs font-semibold text-white hover:bg-red-500" onClick={handleDelete}>
            Delete
          </button>
        )}
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
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <h2 className="p-2 mb-2 text-lg font-semibold bg-white z-100">
          COMPUTED: {`${questionCode} - ${questionText}`}
        </h2>
        {/* <div className="flex flex-col gap-2 pt-10">
          {questionAnswers.map((question, index) => (
            <div key={index}>{question.answerText}</div>
          ))}
        </div> */}

        <div className="flex flex-col gap-5 justify-center">
          <div className="flex flex-row gap-5 items-center">
            <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
              <p className="w-full">New Code</p>
              <input
                type="text"
                name="newQuestionCode"
                className="h-7 w-20 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
            <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
              <p className="w-full">Method</p>
              <input
                type="text"
                name="method"
                className="h-7 w-20 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
            <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
              <p className="w-full">By</p>
              <input
                type="text"
                name="by"
                className="h-7 w-20 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
          </div>
          <div className="flex flex-row gap-5">
            <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
              <p className="w-20">New Text</p>
              <input
                type="text"
                name="newQuestionText"
                className="h-7 w-96 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
          </div>
          <div className="flex flex-row gap-5">
            <label className="flex flex-row items-center gap-5 font-sans text-sm font-semibold">
              <p className="w-20">Compute Construct</p>
              <input
                type="text"
                name="construction"
                className="h-20 w-96 rounded-md border-2 border-gray-300"
                onChange={handleOnChange}
              />
            </label>
          </div>
          <button
            className="h-10 w-24 rounded-md bg-slate-600 text-sm font-semibold text-white"
            onClick={handleOnClick}
          >
            COMPUTE
          </button>
        </div>
      </Modal>
    </div>
  );
};

export default Question;
