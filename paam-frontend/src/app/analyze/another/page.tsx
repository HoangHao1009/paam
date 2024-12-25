import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";

const Another = () => {
  const items = ["Crosstab", "Another"];
  return (
    <div>
      <Canvas>
        <CanvasNavBar items={items} current="analyze"/>
      </Canvas>
    </div>
  );
};

export default Another;
