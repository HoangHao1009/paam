import React, { FC, ReactNode } from "react";

interface CanvasProps {
  children: ReactNode;
  className?: string;
}

const Canvas: FC<CanvasProps> = ({ children, className = "" }) => {
  return <div className={`fixed mx-72 mt-20 flex w-[900px] h-1000 rounded-3xl bg-white pt-8 h-[500px] shadow-sm shadow-slate-400 ${className}`}>{children}</div>;
};

export default Canvas;
