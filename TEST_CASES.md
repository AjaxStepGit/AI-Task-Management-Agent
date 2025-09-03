# 🧪 AI Task Management Agent - Test Cases

## 🚀 **Application Status**
- ✅ **Backend Server**: Running on http://localhost:8000
- ✅ **Frontend Server**: Running on http://localhost:3000
- ✅ **Database**: PostgreSQL `task_management` database created
- ✅ **API Documentation**: http://localhost:8000/docs

---

## 🎯 **Test Environment Setup**

### **Prerequisites**
- Both servers are running (backend on :8000, frontend on :3000)
- PostgreSQL database `task_management` exists
- Google Gemini API key configured

### **Access Points**
- **Main Application**: http://localhost:3000
- **API Health Check**: http://localhost:8000/health
- **Chat Health Check**: http://localhost:8000/api/chat/health
- **API Documentation**: http://localhost:8000/docs

---

## 📋 **Manual Test Cases**

### **🏠 Test Group 1: Basic Application Loading**

#### **TC-001: Application Loads Successfully**
- **Steps**: 
  1. Open http://localhost:3000 in browser
- **Expected**: 
  - Page loads without errors
  - Two-panel layout visible (Chat + Task List)
  - Header shows "🚀 AI Task Management Agent"
  - Online status indicator shows green

#### **TC-002: API Health Checks**
- **Steps**:
  1. Visit http://localhost:8000/health
  2. Visit http://localhost:8000/api/chat/health
- **Expected**:
  - Both return {"status": "healthy"}
  - No errors in console

---

### **💬 Test Group 2: Chat Interface**

#### **TC-003: Initial Chat Message**
- **Steps**: 
  1. Open application
  2. Check initial message in chat
- **Expected**: 
  - Welcome message from AI assistant appears
  - Message explains capabilities

#### **TC-004: Send Simple Message**
- **Steps**:
  1. Type "Hello" in chat input
  2. Click send or press Enter
- **Expected**:
  - Message appears in chat history
  - AI responds with acknowledgment
  - Loading indicator during processing

#### **TC-005: Chat Input Validation**
- **Steps**:
  1. Try to send empty message
  2. Try to send message with just spaces
- **Expected**:
  - Send button remains disabled
  - No empty messages sent

---

### **📝 Test Group 3: Task Creation via Chat**

#### **TC-006: Basic Task Creation**
- **Steps**:
  1. Type: "Add a task to buy groceries"
  2. Send message
- **Expected**:
  - AI confirms task creation
  - New task appears in task list
  - Task has title "buy groceries"
  - Status is "pending"
  - Priority is "medium" (default)

#### **TC-007: Task Creation with Details**
- **Steps**:
  1. Type: "Create a high priority task to finish presentation by tomorrow"
  2. Send message
- **Expected**:
  - AI confirms task creation
  - Task appears with:
    - Title contains "finish presentation"
    - Priority is "high"
    - Due date is set (tomorrow)

#### **TC-008: Task Creation with Specific Date**
- **Steps**:
  1. Type: "Add task to call mom on December 25th"
  2. Send message
- **Expected**:
  - Task created with due date December 25
  - AI confirms the specific date

#### **TC-009: Multiple Task Creation**
- **Steps**:
  1. Type: "I need to do three things: wash car, pay bills, and exercise"
  2. Send message
- **Expected**:
  - AI creates multiple tasks or asks for clarification
  - All three activities mentioned

---

### **📋 Test Group 4: Task List Operations**

#### **TC-010: Task List Display**
- **Steps**:
  1. Create several tasks via chat
  2. Check task list panel
- **Expected**:
  - All tasks visible in list
  - Each task shows: title, status, priority, created date
  - Tasks sorted by creation date (newest first)

#### **TC-011: Task Completion Toggle**
- **Steps**:
  1. Click checkbox next to a pending task
- **Expected**:
  - Task status changes to "completed"
  - Task appears with strikethrough
  - Checkbox shows checkmark
  - Green completion indicator

#### **TC-012: Task Deletion**
- **Steps**:
  1. Click delete button (trash icon) on a task
  2. Confirm deletion
- **Expected**:
  - Confirmation dialog appears
  - Task removed from list after confirmation
  - Task count updates

#### **TC-013: Task Filtering**
- **Steps**:
  1. Create tasks with different statuses and priorities
  2. Use status filter dropdown
  3. Use priority filter dropdown
  4. Use search box
- **Expected**:
  - Filters work correctly
  - Task count updates
  - Only matching tasks displayed

---

### **🤖 Test Group 5: AI Agent Capabilities**

#### **TC-014: Task Status Updates via Chat**
- **Steps**:
  1. Create a task: "Add task to water plants"
  2. Type: "Mark the water plants task as completed"
  3. Send message
- **Expected**:
  - AI finds the task
  - Updates status to completed
  - Task list reflects the change
  - AI confirms the action

#### **TC-015: Task Listing via Chat**
- **Steps**:
  1. Create multiple tasks
  2. Type: "Show me all my tasks"
  3. Send message
- **Expected**:
  - AI lists all tasks
  - Shows count of tasks
  - May summarize task statuses

#### **TC-016: Priority-based Task Queries**
- **Steps**:
  1. Create tasks with different priorities
  2. Type: "Show me all high priority tasks"
  3. Send message
- **Expected**:
  - AI lists only high priority tasks
  - Mentions priority in response
  - Task list may auto-filter

#### **TC-017: Task Deletion via Chat**
- **Steps**:
  1. Create a task: "Add task to test deletion"
  2. Type: "Delete the test deletion task"
  3. Send message
- **Expected**:
  - AI finds and deletes the task
  - Task removed from list
  - AI confirms deletion

#### **TC-018: Task Updates via Chat**
- **Steps**:
  1. Create task: "Buy milk"
  2. Type: "Change the buy milk task to urgent priority"
  3. Send message
- **Expected**:
  - AI updates task priority
  - Task list shows updated priority
  - AI confirms the change

#### **TC-019: Natural Language Date Parsing**
- **Steps**:
  1. Type: "Remind me to call doctor next Friday"
  2. Send message
- **Expected**:
  - AI calculates correct date for "next Friday"
  - Task created with proper due date
  - AI mentions the calculated date

---

### **🔄 Test Group 6: Real-time Updates**

#### **TC-020: Chat to List Synchronization**
- **Steps**:
  1. Create task via chat
  2. Immediately check task list
- **Expected**:
  - Task appears in list immediately
  - No refresh needed

#### **TC-021: List to Chat Feedback**
- **Steps**:
  1. Toggle task completion via checkbox
  2. Check if this affects next chat interactions
- **Expected**:
  - Task status change reflected in subsequent AI responses
  - AI aware of current task states

---

### **🔍 Test Group 7: Error Handling**

#### **TC-022: Invalid Task Operations**
- **Steps**:
  1. Type: "Delete a task that doesn't exist"
  2. Send message
- **Expected**:
  - AI responds gracefully
  - Explains that task wasn't found
  - No errors in console

#### **TC-023: Network Error Simulation**
- **Steps**:
  1. Stop backend server
  2. Try to send chat message
- **Expected**:
  - Frontend shows error message
  - User informed about connectivity issues
  - No application crash

#### **TC-024: Malformed Input Handling**
- **Steps**:
  1. Type very long message (>1000 characters)
  2. Type message with special characters/emojis
  3. Send messages
- **Expected**:
  - Application handles gracefully
  - No crashes or errors
  - Appropriate responses from AI

---

### **📱 Test Group 8: UI/UX**

#### **TC-025: Responsive Design**
- **Steps**:
  1. Resize browser window
  2. Test on different screen sizes
- **Expected**:
  - Layout adapts properly
  - All elements remain accessible
  - Text remains readable

#### **TC-026: Visual Feedback**
- **Steps**:
  1. Send chat messages
  2. Toggle tasks
  3. Use filters
- **Expected**:
  - Loading states shown
  - Hover effects work
  - Smooth transitions
  - Clear visual hierarchy

#### **TC-027: Accessibility**
- **Steps**:
  1. Tab through interface
  2. Check contrast ratios
  3. Test with screen reader (if available)
- **Expected**:
  - All interactive elements focusable
  - Good color contrast
  - Semantic HTML structure

---

## 🚀 **Advanced Test Scenarios**

### **Scenario A: Daily Workflow Simulation**
1. **Morning Planning**:
   - "I need to plan my day"
   - "Add high priority task to finish quarterly report"
   - "Remind me to call client at 2 PM"
   - "Schedule gym session for 6 PM"

2. **Midday Updates**:
   - "Mark the quarterly report as completed"
   - "Show me what's left for today"
   - "Change gym session to tomorrow"

3. **Evening Review**:
   - "What tasks did I complete today?"
   - "Show me all pending tasks"

### **Scenario B: Project Management**
1. **Project Setup**:
   - "Create tasks for new website project"
   - "Add task to design mockups with high priority"
   - "Add task to set up development environment"
   - "Add task to write project documentation"

2. **Progress Tracking**:
   - "Show me all website project tasks"
   - "Mark design mockups as completed"
   - "What's the status of my project tasks?"

### **Scenario C: Priority Management**
1. **Task Creation**:
   - Create 10 tasks with different priorities
   - "Show me all urgent tasks"
   - "List high priority items"
   - "What are my low priority tasks?"

2. **Dynamic Prioritization**:
   - "Make the grocery task urgent"
   - "Change all medium priority tasks to high"

---

## 📊 **Performance Test Cases**

#### **TC-028: Load Testing**
- Create 50+ tasks rapidly via chat
- Check response times remain reasonable
- Verify UI remains responsive

#### **TC-029: Data Persistence**
- Create tasks, close browser, reopen
- Verify all data persists
- Check database consistency

#### **TC-030: Concurrent Operations**
- Send multiple chat messages quickly
- Toggle multiple tasks simultaneously
- Verify system handles concurrent requests

---

## 🔧 **API Test Cases** 

#### **TC-031: Direct API Testing**
Test these endpoints directly via http://localhost:8000/docs:

1. **GET** `/api/tasks` - List all tasks
2. **POST** `/api/tasks` - Create task
3. **GET** `/api/tasks/{task_id}` - Get specific task
4. **PUT** `/api/tasks/{task_id}` - Update task
5. **DELETE** `/api/tasks/{task_id}` - Delete task
6. **PATCH** `/api/tasks/{task_id}/toggle` - Toggle task status
7. **POST** `/api/chat` - Chat with AI agent

---

## ✅ **Expected Results Summary**

After running all test cases, you should see:

### **✅ Working Features**:
- Two-panel interface loads correctly
- Chat interface responds to natural language
- AI agent creates, updates, deletes tasks
- Task list displays and updates in real-time
- Filters and search work properly
- Task completion toggles function
- Date parsing works for natural language dates
- Error handling is graceful
- Real-time synchronization between chat and list

### **🔍 What to Look For**:
- **Smooth UX**: No jarring transitions or loading delays
- **Accurate AI**: Agent correctly interprets natural language
- **Data Consistency**: Changes in chat reflect in task list instantly
- **Error Recovery**: System handles failures gracefully
- **Intuitive Interface**: Easy to understand and use

---

## 🐛 **Issue Reporting Template**

If you find any issues, document them using this format:

```
**Issue ID**: BUG-001
**Test Case**: TC-XXX
**Priority**: High/Medium/Low
**Description**: Brief description of the problem
**Steps to Reproduce**:
1. Step one
2. Step two
3. Step three
**Expected Result**: What should happen
**Actual Result**: What actually happened
**Environment**: Browser, OS version
**Screenshots**: If applicable
```

---

## 🎉 **Ready to Test!**

The application is now fully configured and both servers are running. Start with the basic test cases (TC-001 through TC-005) and work your way through the different groups. The most important tests are the natural language chat interactions (Test Group 5) as this is the core functionality of the AI agent.

**Happy Testing! 🚀**