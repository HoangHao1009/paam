import React, { FC, ReactNode } from "react";

interface CanvasProps {
  children: ReactNode;
  className?: string;
}

const Canvas: FC<CanvasProps> = ({ children, className = "" }) => {
  return (
    <div
      className={`h-1000 fixed mx-72 mt-20 flex h-[500px] w-[900px] rounded-3xl bg-white pl-10 pt-8 shadow-sm shadow-slate-400 ${className}`}
    >
      {children}
    </div>
  );
};

export default Canvas;
