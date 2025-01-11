from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.exceptions import HTTPException

from app.db.redis import get_redisdb, RedisCacheDB
from app.schemas.analyze_schemas import CrossTabSchema, ChatSchema
from app.engine.ai import PAAMSupervisor

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver 

router = APIRouter()

@router.post("/crosstab")
async def crosstab(crosstab_schema: CrossTabSchema, cache_db: RedisCacheDB=Depends(get_redisdb)):
    survey = cache_db.get_survey()
    
    crosstab = survey.crosstab(base=crosstab_schema.base, target=crosstab_schema.target, deep_by=crosstab_schema.deepBy)
    crosstab.config.alpha = crosstab_schema.alpha
    crosstab.config.pct = crosstab_schema.pct
    
    html_table = crosstab.df.to_html()
        
    return JSONResponse(
        content={
            'crosstabData': html_table
        },
        status_code=200
    )
    
    
llm = ChatOpenAI(model='gpt-3.5-turbo', streaming=True)
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
    
    paam.add_survey(survey)
                    
    builder = paam.initialize()
    
    graph = builder.compile(checkpointer=memory)
    
    inputs = {"messages": [HumanMessage(content=request.message)]}

    async def token_generator():
        try:
            async for msg, metadata in graph.astream(input=inputs, config=paam.config, stream_mode="messages"):
                if msg.content and not isinstance(msg, HumanMessage):
                    tool_calling = True if isinstance(msg, ToolMessage) else False
                    if tool_calling:
                        yield f'<p class="font-bold italic">Tool Call: <p>{msg.content}<br>'
                    else:
                        yield msg.content
        except Exception as e:
            yield f"Error during streaming: {e}"
    try:
        return StreamingResponse(token_generator(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error when AI answering: {e}")