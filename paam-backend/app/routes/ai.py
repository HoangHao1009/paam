from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from app.db.redis import get_redisdb, RedisCacheDB

from app.schemas.ai_schemas import ChatSchema
from app.engine.ai import PAAMSupervisor

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver 
from langgraph.checkpoint.postgres import PostgresSaver

import os
from psycopg import Connection

router = APIRouter()

llm = ChatOpenAI(model='gpt-3.5-turbo', streaming=True)

paam = PAAMSupervisor(llm)

class MemoryContainer:
    def __init__(self):
        self.memory = MemorySaver()

    def get_memory(self):
        return self.memory
    
    def get_postgres(self):
        DB_URI = os.getenv("POSTGRES_DB_URI")
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        
        conn = Connection.connect(DB_URI, **connection_kwargs)
        checkpointer = PostgresSaver(conn)
        return checkpointer

memory_container = MemoryContainer()

@router.post("/chat")
async def chat(request: ChatSchema, cache_db: RedisCacheDB=Depends(get_redisdb), memory: MemorySaver = Depends(memory_container.get_postgres)):
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
        