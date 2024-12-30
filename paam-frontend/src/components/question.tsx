interface AnswerProps {
  answerCode: string;
  answerScale: number;
  answerText: string;
  answerRespondents: Array<string>;
}

interface QuestionProps {
  questionCode: string;
  questionText: string;
  questionType: string;
  questionRespondents: Array<string>;
  questionAnswers: Array<AnswerProps>;
  ctabMode: boolean;
}

const Question = ({
  questionCode,
  questionText,
  questionType,
  questionRespondents,
  questionAnswers,
  ctabMode,
}: QuestionProps) => {
  return (
    <div className="flex flex-col gap-2 rounded-md bg-slate-400 p-2 w-1/2">
      <div className="flex flex-row gap-2">
        <p>{questionCode}</p>
        <p>{questionText}</p>
      </div>
      <div className="flex flex-row gap-2">
        <p>{questionType}</p>
        <p>n: {questionRespondents.length}</p>
      </div>
    </div>
  );
};

export default Question;
