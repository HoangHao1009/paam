"use client";

import { ReactNode } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

const Modal = ({ isOpen, onClose, children }: ModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="item-center z-100 fixed inset-0 flex justify-center bg-black bg-opacity-50">
      <div className="relative w-[800px] h-[400px] mt-20 ml-40 rounded-md bg-white p-4 shadow-lg overflow-auto">
        <button
          onClick={onClose}
          className="absolute right-2 top-2 rounded-lg bg-red-700 p-1 font-bold text-white hover:text-gray-800"
        >
          X
        </button>
        {children}
      </div>
    </div>
  );
};

export default Modal;
