"use client";
import { isPagesAPIRouteMatch } from "next/dist/server/route-matches/pages-api-route-match";
import { useRouter } from "next/navigation";

interface SidebarProps {
  items: Array<string>;
  defaultRoute: Record<string, string>;
}

const Sidebar = ({ items, defaultRoute }: SidebarProps) => {
  const router = useRouter();

  const handleClick = (page: string) => {
    router.push(page);
  };

  return (
    <div className="h-1000 fixed z-50 mx-4 mt-5 flex h-[550px] w-60 flex-col items-center rounded-3xl bg-white pt-8 shadow-sm shadow-slate-400">
      <p className="mb-10 mt-5 font-mono text-4xl font-bold italic">PAAM</p>
      <div className="flex flex-col items-center gap-10">
        {items.map((item, index) => (
          <div
            key={index}
            className="relative items-center justify-center font-sans"
          >
            <button
              className="transition hover:font-bold"
              onClick={() => handleClick(defaultRoute[item])}
            >
              {item}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
