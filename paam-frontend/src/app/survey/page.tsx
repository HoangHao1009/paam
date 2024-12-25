import Canvas from "@/components/canvas";
import CanvasNavBar from "@/components/navbar";

const SurveyCanvas = () => {
  const items = ['Provider', 'Questions']
  return (
    <div>
        <Canvas className="font-sans font-semibold text-lg">
            <CanvasNavBar items={items} current="survey" className="pl-10"/>
        </Canvas>
      
    </div>
  )
}

export default SurveyCanvas
