from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[TaskStatus] = Field(TaskStatus.PENDING, description="Task status")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    priority: Optional[TaskPriority] = Field(TaskPriority.MEDIUM, description="Task priority")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    priority: Optional[TaskPriority] = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date_before: Optional[datetime] = None
    due_date_after: Optional[datetime] = None
    search: Optional[str] = None


# Chat-related schemas
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    tasks_affected: Optional[list[TaskResponse]] = None
    action_type: Optional[str] = None  # create, update, delete, list, filter
    conversation_id: str