# 🚀 AI-Powered Task Management Agent

An intelligent task management system where you interact with an AI agent through natural language to create, update, delete, and organize your tasks. Built with **Next.js**, **FastAPI**, **LangGraph**, and **Gemini AI**.

![Task Management Agent Demo](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=AI+Task+Management+Agent)

## 🌟 Features

### 💬 Natural Language Chat Interface
- Chat with your AI assistant using natural language
- Commands like "Add a task to buy groceries tomorrow" 
- "Show me all high priority tasks"
- "Mark the meeting task as completed"

### 📋 Real-time Task Management
- Create, update, delete, and list tasks
- Filter by status, priority, due date
- Live updates between chat and task list
- Checkbox toggles for quick status changes

### 🧠 AI-Powered Agent
- **LangGraph** workflow orchestration
- **Google Gemini AI** for natural language understanding
- Context-aware task operations
- Intelligent intent parsing and extraction

### 🎨 Modern UI/UX
- **Two-panel layout**: Chat interface + Task list
- **Responsive design** with TailwindCSS
- **Real-time updates** across components
- **Dark/Light mode support** (bonus feature)

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐
│     Frontend        │    │      Backend        │
│   (Next.js)         │    │   (FastAPI)         │
│                     │    │                     │
│  ┌───────────────┐  │    │  ┌───────────────┐  │
│  │ Chat Interface│  │    │  │ LangGraph     │  │
│  └───────────────┘  │◄──►│  │ Agent         │  │
│  ┌───────────────┐  │    │  └───────────────┘  │
│  │ Task List     │  │    │  ┌───────────────┐  │
│  └───────────────┘  │    │  │ FastAPI       │  │
└─────────────────────┘    │  │ Endpoints     │  │
                           │  └───────────────┘  │
                           │  ┌───────────────┐  │
                           │  │ PostgreSQL    │  │
                           │  │ Database      │  │
                           │  └───────────────┘  │
                           └─────────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - AI agent orchestration
- **Google Gemini AI** - Large language model
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database
- **WebSockets** - Real-time communication

### Frontend
- **Next.js 14** - React framework with App Router
- **TailwindCSS** - Utility-first CSS framework
- **TypeScript** - Type safety
- **React Hooks** - State management

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD (bonus)

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ 
- **Python** 3.11+
- **PostgreSQL** 15+
- **Google API Key** (for Gemini AI)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd task-manage
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings:
# - DATABASE_URL=postgresql://postgres:password@localhost:5432/task_management
# - GOOGLE_API_KEY=your_google_api_key_here

# Set up database
createdb task_management  # or use your PostgreSQL client

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Run the frontend
npm run dev
```

### 4. Using Docker (Recommended)
```bash
# Create .env file in root directory
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

# Start all services
docker-compose up --build

# The application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🎯 Usage Examples

### Basic Task Management
```
User: "Add a task to call mom tomorrow at 3 PM"
AI: "I've created a task 'Call mom' with due date tomorrow at 3 PM!"

User: "Show me all urgent tasks"
AI: "Here are your urgent tasks: [lists urgent tasks]"

User: "Mark the grocery shopping task as completed"
AI: "Great! I've marked 'Grocery shopping' as completed."
```

### Advanced Queries
```
User: "What tasks are due this week?"
User: "Create a high priority task to prepare presentation for Friday"
User: "Delete all completed tasks from last month"
User: "Show me tasks that contain 'meeting' in the title"
```

## 📁 Project Structure

```
task-manage/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agents/         # LangGraph agents
│   │   ├── api/            # API endpoints
│   │   ├── database/       # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── tools/          # LangGraph tools
│   │   └── main.py         # FastAPI app
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # React components
│   │   ├── lib/            # Utilities
│   │   └── types/          # TypeScript types
│   ├── Dockerfile
│   ├── package.json
│   └── .env.local.example
├── docker-compose.yml      # Docker orchestration
└── README.md
```

## 🔧 Environment Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/task_management
GOOGLE_API_KEY=your_google_api_key_here
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### Using Docker
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment
1. Set up PostgreSQL database
2. Deploy backend to your preferred platform (Heroku, Railway, DigitalOcean)
3. Deploy frontend to Vercel/Netlify
4. Update environment variables

## 🎨 Bonus Features Implemented

- ✅ **Real-time WebSocket communication**
- ✅ **Responsive design with TailwindCSS**
- ✅ **Docker containerization**
- ✅ **Comprehensive error handling**
- ✅ **Task filtering and search**
- ✅ **Animated UI components**
- ✅ **Health checks and monitoring**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph** for agent orchestration
- **Google Gemini AI** for natural language processing
- **FastAPI** for the excellent Python web framework
- **Next.js** for the React framework
- **TailwindCSS** for the utility-first CSS

---

## 📬 Contact & Demo

- **GitHub Repository**: [Your GitHub URL]
- **Live Demo**: [Your Deployed URL]
- **Loom Video Demo**: [Your Loom Video URL]

**Built with ❤️ using LangGraph, Gemini AI, Next.js, and FastAPI**