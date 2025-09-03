'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import ChatInterface from '@/components/ChatInterface';
import TaskList from '@/components/TaskList';
import ThemeToggle from '@/components/ThemeToggle';

export default function Home() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTasksUpdate = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100 dark:bg-gray-900 transition-colors">
      <ThemeToggle />
      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 shadow-sm transition-colors"
      >
        <div className="flex items-center justify-between">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              🚀 AI Task Management Agent
            </h1>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Chat with your AI assistant to manage tasks naturally
            </p>
          </motion.div>
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex items-center gap-2"
          >
            <div className="flex items-center gap-1 px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full text-sm">
              <motion.div 
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-2 h-2 bg-green-500 rounded-full"
              />
              Online
            </div>
          </motion.div>
        </div>
      </motion.header>

      {/* Main Content - Two Panel Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Chat Interface */}
        <motion.div 
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="w-1/2 min-w-[400px] flex flex-col"
        >
          <ChatInterface onTasksUpdate={handleTasksUpdate} />
        </motion.div>

        {/* Right Panel - Task List */}
        <motion.div 
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="w-1/2 min-w-[400px] flex flex-col"
        >
          <TaskList 
            refreshTrigger={refreshTrigger} 
            onTaskUpdate={handleTasksUpdate}
          />
        </motion.div>
      </div>

      {/* Footer */}
      <motion.footer 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 1.0 }}
        className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-3 transition-colors"
      >
        <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-4">
            <span>© 2024 AI Task Management Agent</span>
            <span className="text-gray-300 dark:text-gray-600">|</span>
            <span>Powered by LangGraph + Gemini AI</span>
          </div>
          <div className="flex items-center gap-4">
            <span>Next.js + FastAPI</span>
          </div>
        </div>
      </motion.footer>
    </div>
  );
}
