#!/bin/bash

# AI Task Management Agent Setup Script
echo "🚀 Setting up AI Task Management Agent..."

# Check if required tools are installed
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install $1 and run this script again."
        exit 1
    else
        echo "✅ $1 is installed"
    fi
}

echo "Checking dependencies..."
check_dependency "docker"
check_dependency "docker-compose"
check_dependency "node"
check_dependency "python3"

# Create environment files
echo "📝 Creating environment files..."

# Backend environment
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env - Please update with your Google API key"
else
    echo "⚠️  backend/.env already exists"
fi

# Frontend environment
if [ ! -f "frontend/.env.local" ]; then
    cp frontend/.env.local.example frontend/.env.local
    echo "✅ Created frontend/.env.local"
else
    echo "⚠️  frontend/.env.local already exists"
fi

# Root environment for Docker
if [ ! -f ".env" ]; then
    echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
    echo "✅ Created root .env file - Please update with your Google API key"
else
    echo "⚠️  Root .env already exists"
fi

echo ""
echo "🔧 Setup Options:"
echo "1. Run with Docker (Recommended)"
echo "2. Run manually (Development)"
echo "3. Exit"
echo ""

read -p "Choose an option (1-3): " choice

case $choice in
    1)
        echo "🐳 Starting with Docker..."
        echo "Please make sure you've added your Google API key to the .env file"
        read -p "Press Enter when ready to continue..."
        docker-compose up --build
        ;;
    2)
        echo "🛠️  Manual setup instructions:"
        echo ""
        echo "Backend:"
        echo "  cd backend"
        echo "  python -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        echo "  uvicorn app.main:app --reload"
        echo ""
        echo "Frontend:"
        echo "  cd frontend"
        echo "  npm install"
        echo "  npm run dev"
        echo ""
        echo "Database:"
        echo "  Make sure PostgreSQL is running and create 'task_management' database"
        ;;
    3)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"