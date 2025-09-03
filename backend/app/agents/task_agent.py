import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import uuid
import json
import asyncio

from app.tools.task_tools import create_task, update_task, delete_task, list_tasks, filter_tasks


class TaskManagementAgent:
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )
        
        # Available tools
        self.tools = [create_task, update_task, delete_task, list_tasks, filter_tasks]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
    
    async def chat(self, user_input: str, conversation_id: str = None) -> Dict[str, Any]:
        """Main chat interface"""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        try:
            # System prompt
            system_prompt = """You are a helpful AI assistant for task management. You can help users:

1. Create new tasks with title, description, due date, and priority
2. Update existing tasks (modify any field, change status, etc.)
3. Delete tasks by ID or title
4. List all tasks
5. Filter tasks by status, priority, due date, or search terms

IMPORTANT GUIDELINES:
- ALWAYS be proactive and create tasks immediately when users request them
- Use sensible defaults: medium priority, no due date unless specified
- Extract the task title from natural language (e.g., "Add a task to buy groceries" → title: "buy groceries")
- Don't ask for clarification unless absolutely necessary
- Be conversational and confirm actions after completion
- For dates, accept various formats and convert to ISO format
- When listing or filtering tasks, provide a clear summary
- If a user wants to mark a task as complete, update its status to "completed"

Current date context: Use reasonable defaults for dates when users say "today", "tomorrow", "next week", etc.

Examples of user intents and IMMEDIATE actions:
- "Add a task to buy groceries" → IMMEDIATELY call create_task(title="buy groceries", priority="medium")
- "Create a high priority task to finish report" → IMMEDIATELY call create_task(title="finish report", priority="high")
- "Mark the groceries task as done" → update_task (status=completed)  
- "Show me all high priority tasks" → filter_tasks (priority=high)
- "Delete the meeting task" → delete_task
- "What tasks are due tomorrow?" → filter_tasks with date range

ALWAYS use tools to perform actual task operations. Be proactive and take action immediately."""

            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
            
            # Get AI response with tools
            response = self.llm_with_tools.invoke(messages)
            
            tasks_affected = []
            action_type = "chat"
            
            # Execute tool calls if any
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']
                    action_type = tool_name.replace('_', ' ').title()
                    
                    # Find and execute the tool
                    for tool in self.tools:
                        if tool.name == tool_name:
                            try:
                                # Execute the tool
                                tool_result = await tool.ainvoke(tool_args)
                                
                                # Parse tool result
                                if isinstance(tool_result, dict):
                                    if tool_result.get('success') and 'task' in tool_result:
                                        tasks_affected.append(tool_result['task'])
                                    elif tool_result.get('success') and 'tasks' in tool_result:
                                        tasks_affected.extend(tool_result['tasks'])
                                elif isinstance(tool_result, str):
                                    try:
                                        parsed_result = json.loads(tool_result)
                                        if parsed_result.get('success') and 'task' in parsed_result:
                                            tasks_affected.append(parsed_result['task'])
                                        elif parsed_result.get('success') and 'tasks' in parsed_result:
                                            tasks_affected.extend(parsed_result['tasks'])
                                    except json.JSONDecodeError:
                                        pass
                                        
                            except Exception as tool_error:
                                print(f"Tool execution error: {tool_error}")
                            break
                
                # Generate final response after tool execution
                if tasks_affected:
                    if action_type == "Create Task":
                        response_text = f"Perfect! I've created the task '{tasks_affected[0].get('title', 'New Task')}' for you. It's now in your task list!"
                    elif action_type == "List Tasks":
                        count = len(tasks_affected)
                        if count == 0:
                            response_text = "You don't have any tasks yet. Feel free to create some by saying something like 'Add a task to [your task here]'."
                        else:
                            response_text = f"Here are your {count} task(s). You can see them in the task list on the right!"
                    elif action_type == "Update Task":
                        response_text = f"Great! I've updated the task '{tasks_affected[0].get('title', 'Task')}' for you."
                    elif action_type == "Delete Task":
                        response_text = "Task deleted successfully! It's been removed from your list."
                    elif action_type == "Filter Tasks":
                        count = len(tasks_affected)
                        response_text = f"Found {count} task(s) matching your criteria. Check the task list to see them!"
                    else:
                        response_text = response.content if hasattr(response, 'content') else "Task operation completed successfully!"
                else:
                    response_text = response.content if hasattr(response, 'content') else "I've processed your request!"
            else:
                # No tools called, just return the AI response
                response_text = response.content if hasattr(response, 'content') else "Hello! I'm your task management assistant. Try asking me to create a task like 'Add a task to buy groceries' or 'Show me my tasks'."
            
            return {
                "response": response_text,
                "conversation_id": conversation_id,
                "tasks_affected": tasks_affected,
                "action_type": action_type
            }
            
        except Exception as e:
            print(f"Agent error: {str(e)}")
            return {
                "response": f"I encountered an error: {str(e)}. Please try again.",
                "conversation_id": conversation_id,
                "tasks_affected": [],
                "action_type": "error"
            }


# Global agent instance
task_agent = TaskManagementAgent()