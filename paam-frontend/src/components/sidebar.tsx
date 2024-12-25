'use client'
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
    <div className="h-1000 fixed mx-4 mt-20 flex h-[500px] w-60 flex-col items-center gap-10 rounded-3xl bg-white pt-8 shadow-sm shadow-slate-400">
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
  );
};

export default Sidebar;
