import os
import re
import uuid
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskFilter
from app.models.task import TaskStatus, TaskPriority
from app.database.connection import AsyncSessionLocal
from datetime import datetime, timedelta


class SimpleTaskAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )

    async def chat(self, user_input: str, conversation_id: str = None) -> Dict[str, Any]:
        """Simple rule-based chat interface with direct task operations"""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        user_lower = user_input.lower().strip()
        tasks_affected = []
        action_type = "chat"

        try:
            async with AsyncSessionLocal() as db:
                task_service = TaskService(db)

                # Task Creation Patterns
                if any(keyword in user_lower for keyword in ["add task", "create task", "new task", "remind me", "create a task", "add a task", "make task", "build"]):
                    # Extract task title and description
                    title, description = self._extract_task_title_and_description(user_input)
                    priority = self._extract_priority(user_input)
                    due_date = self._extract_due_date(user_input)

                    if title:
                        task_data = TaskCreate(
                            title=title,
                            description=description,
                            priority=priority,
                            due_date=due_date
                        )
                        task = await task_service.create_task(task_data)
                        tasks_affected = [task.to_dict()]
                        action_type = "Create Task"
                        response_text = f"Perfect! I've created the task '{title}' for you. It's now in your task list!"
                    else:
                        response_text = "I'd be happy to create a task for you! Could you tell me what you'd like to add?"

                # Task Listing
                elif any(keyword in user_lower for keyword in ["show tasks", "list tasks", "my tasks", "what tasks"]):
                    tasks = await task_service.get_tasks()
                    tasks_affected = [task.to_dict() for task in tasks]
                    action_type = "List Tasks"
                    if len(tasks) == 0:
                        response_text = "You don't have any tasks yet. Feel free to create some by saying 'Add a task to [your task here]'."
                    else:
                        response_text = f"Here are your {len(tasks)} task(s). You can see them in the task list on the right!"

                # Task Completion
                elif any(keyword in user_lower for keyword in ["mark", "complete", "done", "finished"]):
                    task_title = self._extract_task_reference(user_input)
                    if task_title:
                        task = await task_service.get_task_by_title(task_title)
                        if task:
                            update_data = TaskUpdate(status=TaskStatus.COMPLETED)
                            updated_task = await task_service.update_task(task.id, update_data)
                            tasks_affected = [updated_task.to_dict()]
                            action_type = "Update Task"
                            response_text = f"Great! I've marked '{task_title}' as completed."
                        else:
                            response_text = f"I couldn't find a task matching '{task_title}'. Please check the spelling or try again."
                    else:
                        response_text = "Which task would you like to mark as complete?"

                # Priority Filtering
                elif any(priority in user_lower for priority in ["high priority", "urgent", "medium priority", "low priority"]):
                    if "high" in user_lower or "urgent" in user_lower:
                        priority = TaskPriority.HIGH if "high" in user_lower else TaskPriority.URGENT
                    elif "medium" in user_lower:
                        priority = TaskPriority.MEDIUM
                    else:
                        priority = TaskPriority.LOW
                    
                    filter_criteria = TaskFilter(priority=priority)
                    tasks = await task_service.filter_tasks(filter_criteria)
                    tasks_affected = [task.to_dict() for task in tasks]
                    action_type = "Filter Tasks"
                    response_text = f"Found {len(tasks)} {priority.value} priority task(s). Check the task list to see them!"

                # Task Deletion
                elif any(keyword in user_lower for keyword in ["delete", "remove"]):
                    task_title = self._extract_task_reference(user_input)
                    if task_title:
                        success = await task_service.delete_task_by_title(task_title)
                        if success:
                            action_type = "Delete Task"
                            response_text = f"Task '{task_title}' has been deleted successfully!"
                        else:
                            response_text = f"I couldn't find a task matching '{task_title}' to delete."
                    else:
                        response_text = "Which task would you like to delete?"

                # General Conversation
                else:
                    prompt = f"""You are a helpful AI task management assistant. The user said: "{user_input}"

Respond conversationally and helpfully. Here are some examples of what you can help with:
- Creating tasks: "Add a task to buy groceries"
- Listing tasks: "Show me my tasks" 
- Completing tasks: "Mark the grocery task as done"
- Filtering tasks: "Show me high priority tasks"
- Deleting tasks: "Delete the meeting task"

Keep responses friendly and concise."""

                    response = self.llm.invoke(prompt)
                    response_text = response.content if hasattr(response, 'content') else "Hello! I'm your task management assistant. Try asking me to create a task!"

                return {
                    "response": response_text,
                    "conversation_id": conversation_id,
                    "tasks_affected": tasks_affected,
                    "action_type": action_type
                }

        except Exception as e:
            print(f"Simple agent error: {str(e)}")
            return {
                "response": "I encountered an error. Please try again.",
                "conversation_id": conversation_id,
                "tasks_affected": [],
                "action_type": "error"
            }

    def _extract_task_title(self, text: str) -> str:
        """Extract task title from user input"""
        text_lower = text.lower()
        
        # Common patterns for task creation
        patterns = [
            r"add (?:a )?task (?:to |called )?(?:'([^']+)'|(.+))",
            r"create (?:a )?task (?:to |for |called )?(?:'([^']+)'|(.+))",
            r"remind me to (.+)",
            r"new task:? (.+)",
            r"task:? (.+)",
            r"i need to (.+)",
            r"(?:create|add|make|build) (?:a )?task (.+)",
            r"create a task to (.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Handle cases where we have multiple capture groups (quoted vs unquoted)
                groups = match.groups()
                for group in groups:
                    if group and group.strip():
                        return group.strip()
        
        return ""

    def _extract_priority(self, text: str) -> TaskPriority:
        """Extract priority from user input"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["urgent", "asap", "immediately"]):
            return TaskPriority.URGENT
        elif any(word in text_lower for word in ["high priority", "important", "high"]):
            return TaskPriority.HIGH
        elif any(word in text_lower for word in ["low priority", "low", "sometime"]):
            return TaskPriority.LOW
        else:
            return TaskPriority.MEDIUM

    def _extract_due_date(self, text: str) -> datetime:
        """Extract due date from user input"""
        text_lower = text.lower()
        now = datetime.now()
        
        if "today" in text_lower:
            return now.replace(hour=23, minute=59, second=59, microsecond=0)
        elif "tomorrow" in text_lower:
            return (now + timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
        elif "next week" in text_lower:
            return (now + timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=0)
        elif "friday" in text_lower:
            # Find next Friday
            days_ahead = 4 - now.weekday()  # Friday is 4
            if days_ahead <= 0:
                days_ahead += 7
            return (now + timedelta(days=days_ahead)).replace(hour=23, minute=59, second=59, microsecond=0)
        
        return None

    def _extract_task_reference(self, text: str) -> str:
        """Extract task reference for updates/deletions"""
        text_lower = text.lower()
        
        # Remove common action words to extract the task reference
        text_lower = re.sub(r"^(mark|complete|delete|remove|finish)\s+(the\s+)?", "", text_lower)
        text_lower = re.sub(r"\s+(task|as\s+done|as\s+completed).*$", "", text_lower)
        
        return text_lower.strip()


# Global simple agent instance
simple_agent = SimpleTaskAgent()