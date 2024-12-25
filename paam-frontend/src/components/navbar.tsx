"use client";
import { FC } from "react";
import { useRouter } from "next/navigation";

interface CanvasNavBarProps {
  items: Array<string>;
  current?: string;
  className?: string;
}

const CanvasNavBar: FC<CanvasNavBarProps> = ({ items, current, className = "" }) => {
  const router = useRouter();
  return (
    <div className={`flex flex-row items-start gap-10 ${className}`}>
      {items.map((item, index) => {
        const itemRoute = `/${current}/${item.toLowerCase()}`;
        const handleClick = () => {
          router.push(itemRoute);
        }

        return (
          <button
            key={index}
            className="rounded-lg bg-white p-2 hover:bg-slate-200"
            onClick={handleClick}
          >
            {item}
          </button>
        );
      })}
    </div>
  );
};

export default CanvasNavBar;
