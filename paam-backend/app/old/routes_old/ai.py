from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.exceptions import HTTPException
from app.db.redis import get_redisdb, RedisCacheDB

from app.schemas.analyze_schemas import ChatSchema
from app.engine.ai import PAAMSupervisor, QuestionnaireCreator, Extract_Chain

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver 

import os

router = APIRouter()

llm = ChatOpenAI(model='gpt-3.5-turbo', streaming=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), cache_db: RedisCacheDB=Depends(get_redisdb)):
    try:
        file_location = f"/uploads/{file.filename}"
        cache_db.set("design_file_location", file_location)
        with open(file_location, "wb") as f:
            f.write(await file.read())
            
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error during file upload: {e}"}
        )
        
@router.post("/create")
async def create_questionnaire(request: CreateSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    print(request)
    survey_config = cache_db.get("configuration")
    
    extraction_chain = Extract_Chain(api_key=os.environ.get("OPENAI_API_KEY"))

    creator = QuestionnaireCreator(
        questionnaire_design_path=cache_db.get("design_file_location"), 
        extract_chain=extraction_chain, 
        api_key=survey_config["api_key"]
    )
    
    creator.create("12710083")
    
    return {"message": "Questionnaire created successfully"}

paam = PAAMSupervisor(llm)

class MemoryContainer:
    def __init__(self):
        self.memory = MemorySaver()

    def get_memory(self):
        return self.memory
    

memory_container = MemoryContainer()

@router.post("/chat")
async def chat(request: ChatSchema, cache_db: RedisCacheDB=Depends(get_redisdb), memory: MemorySaver = Depends(memory_container.get_memory)):
    survey = cache_db.get_survey()
    survey.initialize()
    
    paam.add_survey(survey)
                    
    builder = paam.initialize()
    
    graph = builder.compile(checkpointer=memory)
    
    inputs = {"messages": [HumanMessage(content=request.message)]}

    async def token_generator():
        try:
            async for msg, metadata in graph.astream(input=inputs, config=paam.config, stream_mode="messages"):
                if msg.content and not isinstance(msg, HumanMessage):
                    yield msg.content
        except Exception as e:
            yield f"Error during streaming: {e}"
    try:
        return StreamingResponse(token_generator(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error when AI answering: {e}")
        