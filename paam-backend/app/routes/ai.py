from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException

from app.schemas.ai_schemas import ChatSchema

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatSchema):
    message = request.message
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    inputs = [
        {'role': 'user',
         'content': message}
    ]

    # async def token_generator():
    #     async for event in graph.astream_events({'message': inputs}, version='v2'):
    #         yield event["event"]

    # return StreamingResponse(token_generator(), media_type="text/plain")
    

    return {"message": "TEST CHAT"}