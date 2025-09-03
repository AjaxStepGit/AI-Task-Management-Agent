from fastapi import APIRouter, HTTPException
from app.schemas.task import ChatMessage, ChatResponse
from app.agents.simple_agent import simple_agent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    """Chat with the task management agent"""
    try:
        logger.info(f"Received chat message: {message.message}")
        
        response = await simple_agent.chat(
            user_input=message.message,
            conversation_id=message.conversation_id
        )
        
        return ChatResponse(
            response=response["response"],
            tasks_affected=response.get("tasks_affected", []),
            action_type=response.get("action_type", "chat"),
            conversation_id=response["conversation_id"]
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/chat/health")
async def chat_health():
    """Health check for chat functionality"""
    return {"status": "healthy", "agent": "ready"}