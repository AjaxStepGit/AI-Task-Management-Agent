from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.connection import get_async_session
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskFilter

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Get all tasks with pagination"""
    task_service = TaskService(db)
    tasks = await task_service.get_tasks(skip=skip, limit=limit)
    return tasks


@router.post("/tasks", response_model=TaskResponse)
async def create_task_endpoint(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new task"""
    task_service = TaskService(db)
    return await task_service.create_task(task)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get a task by ID"""
    task_service = TaskService(db)
    task = await task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update a task by ID"""
    task_service = TaskService(db)
    task = await task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
async def delete_task_endpoint(
    task_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Delete a task by ID"""
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.post("/tasks/filter", response_model=List[TaskResponse])
async def filter_tasks_endpoint(
    task_filter: TaskFilter,
    db: AsyncSession = Depends(get_async_session)
):
    """Filter tasks based on criteria"""
    task_service = TaskService(db)
    tasks = await task_service.filter_tasks(task_filter)
    return tasks


@router.patch("/tasks/{task_id}/toggle")
async def toggle_task_status(
    task_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Toggle task status between pending and completed"""
    task_service = TaskService(db)
    task = await task_service.toggle_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task status updated to {task.status.value}", "task": task.to_dict()}