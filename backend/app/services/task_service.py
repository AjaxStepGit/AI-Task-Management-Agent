from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime

from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskFilter


class TaskService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task"""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            due_date=task_data.due_date,
            priority=task_data.priority
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_task_by_title(self, title: str) -> Optional[Task]:
        """Get task by title (case-insensitive)"""
        result = await self.db.execute(
            select(Task).where(func.lower(Task.title) == func.lower(title))
        )
        return result.scalar_one_or_none()

    async def get_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination"""
        result = await self.db.execute(
            select(Task).offset(skip).limit(limit).order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def filter_tasks(self, task_filter: TaskFilter) -> List[Task]:
        """Filter tasks based on criteria"""
        query = select(Task)
        conditions = []

        if task_filter.status:
            conditions.append(Task.status == task_filter.status)

        if task_filter.priority:
            conditions.append(Task.priority == task_filter.priority)

        if task_filter.due_date_before:
            conditions.append(Task.due_date <= task_filter.due_date_before)

        if task_filter.due_date_after:
            conditions.append(Task.due_date >= task_filter.due_date_after)

        if task_filter.search:
            search_term = f"%{task_filter.search.lower()}%"
            conditions.append(
                or_(
                    func.lower(Task.title).like(search_term),
                    func.lower(Task.description).like(search_term)
                )
            )

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(Task.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task by ID"""
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task_by_title(self, title: str, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task by title"""
        task = await self.get_task_by_title(title)
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = await self.get_task_by_id(task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True

    async def delete_task_by_title(self, title: str) -> bool:
        """Delete a task by title"""
        task = await self.get_task_by_title(title)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True

    async def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """Toggle task status between pending and completed"""
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        if task.status == TaskStatus.COMPLETED:
            task.status = TaskStatus.PENDING
        else:
            task.status = TaskStatus.COMPLETED

        await self.db.commit()
        await self.db.refresh(task)
        return task