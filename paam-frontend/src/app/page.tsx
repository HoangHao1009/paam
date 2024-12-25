import Sidebar from "@/components/sidebar";
import Canvas from "@/components/canvas";

export default function Home() {
  return (
    <div>
      <Canvas className="font-sans text-3xl font-semibold gap-10">
        <p>Hello. Welcome to PAAM!</p>
        <p>Feel free to discover and make sth</p>
      </Canvas>
    </div>
  );
}
