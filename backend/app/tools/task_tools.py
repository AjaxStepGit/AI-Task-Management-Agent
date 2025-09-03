from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field

from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskFilter
from app.models.task import TaskStatus, TaskPriority
from app.database.connection import AsyncSessionLocal


@tool
async def create_task(
    title: str = Field(..., description="The title of the task"),
    description: Optional[str] = Field(None, description="The description of the task"),
    due_date: Optional[str] = Field(None, description="Due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"),
    priority: Optional[str] = Field("medium", description="Priority: low, medium, high, urgent")
) -> Dict[str, Any]:
    """Create a new task with the given parameters."""
    async with AsyncSessionLocal() as db:
        task_service = TaskService(db)
        
        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {"error": f"Invalid date format: {due_date}. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"}
        
        # Parse priority
        task_priority = TaskPriority.MEDIUM
        if priority:
            try:
                task_priority = TaskPriority(priority.lower())
            except ValueError:
                return {"error": f"Invalid priority: {priority}. Use: low, medium, high, urgent"}
        
        task_data = TaskCreate(
            title=title,
            description=description,
            due_date=parsed_due_date,
            priority=task_priority
        )
        
        try:
            task = await task_service.create_task(task_data)
            return {
                "success": True,
                "task": task.to_dict(),
                "message": f"Task '{title}' created successfully!"
            }
        except Exception as e:
            return {"error": f"Failed to create task: {str(e)}"}


@tool
async def update_task(
    identifier: str = Field(..., description="Task ID (number) or task title (string)"),
    title: Optional[str] = Field(None, description="New title for the task"),
    description: Optional[str] = Field(None, description="New description for the task"),
    status: Optional[str] = Field(None, description="New status: pending, in_progress, completed"),
    due_date: Optional[str] = Field(None, description="New due date in ISO format"),
    priority: Optional[str] = Field(None, description="New priority: low, medium, high, urgent")
) -> Dict[str, Any]:
    """Update an existing task by ID or title."""
    async with AsyncSessionLocal() as db:
        task_service = TaskService(db)
        
        # Parse due date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {"error": f"Invalid date format: {due_date}"}
        
        # Parse status
        task_status = None
        if status:
            try:
                task_status = TaskStatus(status.lower())
            except ValueError:
                return {"error": f"Invalid status: {status}. Use: pending, in_progress, completed"}
        
        # Parse priority
        task_priority = None
        if priority:
            try:
                task_priority = TaskPriority(priority.lower())
            except ValueError:
                return {"error": f"Invalid priority: {priority}. Use: low, medium, high, urgent"}
        
        update_data = TaskUpdate(
            title=title,
            description=description,
            status=task_status,
            due_date=parsed_due_date,
            priority=task_priority
        )
        
        try:
            # Try to parse as ID first
            try:
                task_id = int(identifier)
                task = await task_service.update_task(task_id, update_data)
            except ValueError:
                # If not a number, treat as title
                task = await task_service.update_task_by_title(identifier, update_data)
            
            if task:
                return {
                    "success": True,
                    "task": task.to_dict(),
                    "message": f"Task '{task.title}' updated successfully!"
                }
            else:
                return {"error": f"Task not found: {identifier}"}
        except Exception as e:
            return {"error": f"Failed to update task: {str(e)}"}


@tool
async def delete_task(
    identifier: str = Field(..., description="Task ID (number) or task title (string)")
) -> Dict[str, Any]:
    """Delete a task by ID or title."""
    async with AsyncSessionLocal() as db:
        task_service = TaskService(db)
        
        try:
            # Try to parse as ID first
            try:
                task_id = int(identifier)
                success = await task_service.delete_task(task_id)
            except ValueError:
                # If not a number, treat as title
                success = await task_service.delete_task_by_title(identifier)
            
            if success:
                return {
                    "success": True,
                    "message": f"Task '{identifier}' deleted successfully!"
                }
            else:
                return {"error": f"Task not found: {identifier}"}
        except Exception as e:
            return {"error": f"Failed to delete task: {str(e)}"}


@tool
async def list_tasks(
    limit: int = Field(50, description="Maximum number of tasks to return")
) -> Dict[str, Any]:
    """List all tasks."""
    async with AsyncSessionLocal() as db:
        task_service = TaskService(db)
        
        try:
            tasks = await task_service.get_tasks(limit=limit)
            return {
                "success": True,
                "tasks": [task.to_dict() for task in tasks],
                "count": len(tasks),
                "message": f"Found {len(tasks)} tasks"
            }
        except Exception as e:
            return {"error": f"Failed to list tasks: {str(e)}"}


@tool
async def filter_tasks(
    status: Optional[str] = Field(None, description="Filter by status: pending, in_progress, completed"),
    priority: Optional[str] = Field(None, description="Filter by priority: low, medium, high, urgent"),
    search: Optional[str] = Field(None, description="Search in title and description"),
    due_before: Optional[str] = Field(None, description="Tasks due before this date (ISO format)"),
    due_after: Optional[str] = Field(None, description="Tasks due after this date (ISO format)")
) -> Dict[str, Any]:
    """Filter tasks based on various criteria."""
    async with AsyncSessionLocal() as db:
        task_service = TaskService(db)
        
        # Parse status
        task_status = None
        if status:
            try:
                task_status = TaskStatus(status.lower())
            except ValueError:
                return {"error": f"Invalid status: {status}"}
        
        # Parse priority
        task_priority = None
        if priority:
            try:
                task_priority = TaskPriority(priority.lower())
            except ValueError:
                return {"error": f"Invalid priority: {priority}"}
        
        # Parse dates
        due_before_date = None
        if due_before:
            try:
                due_before_date = datetime.fromisoformat(due_before.replace('Z', '+00:00'))
            except ValueError:
                return {"error": f"Invalid due_before date format: {due_before}"}
        
        due_after_date = None
        if due_after:
            try:
                due_after_date = datetime.fromisoformat(due_after.replace('Z', '+00:00'))
            except ValueError:
                return {"error": f"Invalid due_after date format: {due_after}"}
        
        filter_criteria = TaskFilter(
            status=task_status,
            priority=task_priority,
            search=search,
            due_date_before=due_before_date,
            due_date_after=due_after_date
        )
        
        try:
            tasks = await task_service.filter_tasks(filter_criteria)
            return {
                "success": True,
                "tasks": [task.to_dict() for task in tasks],
                "count": len(tasks),
                "message": f"Found {len(tasks)} tasks matching criteria"
            }
        except Exception as e:
            return {"error": f"Failed to filter tasks: {str(e)}"}