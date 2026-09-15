/* eslint-disable no-unused-vars */
import { useState } from 'react'
import NavBar from './Components/NavBar'
import { useNavigate } from 'react-router-dom';
import StyleHeader from './Components/StyleHeader'
import { getAuthenticated, setAuthenticated } from './utils/auth';
import Chatbot from './Components/Chatbot'; // ADD THIS IMPORT

function App() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    const isAuthenticated = getAuthenticated(); // Retrieve authentication status
    
    if (!isAuthenticated) {
      navigate('/SignIn'); // Navigate to SignIn if not authenticated
    } else {
      navigate('/Analyze'); // Navigate to analyze if authenticated
    }
  };

  return (
    <div className='min-h-screen flex flex-col overflow-x-hidden'>
      <NavBar />
      <main className="flex-1 bg-gradient-to-r from-blue-800 via-violet-800 to-black flex items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
        <div className="w-full max-w-5xl text-center text-white">
          <h2 className="text-4xl sm:text-5xl md:text-6xl lg:text-8xl font-sans font-extrabold text-yellow-500 leading-tight tracking-tight">
            Welcome to SkillSpark.AI
          </h2>
          <div className="mt-5 sm:mt-7">
            <StyleHeader />
          </div>
          <div className="mt-6 sm:mt-8">
            <button
              className="inline-flex items-center justify-center rounded-lg bg-white px-6 py-3 text-sm font-semibold text-violet-800 shadow-lg transition hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400 sm:px-8 sm:text-base"
              onClick={handleGetStarted}
            >
              Get Started
            </button>
          </div>
        </div>
      </main>
      <Chatbot />
    </div>
  );
}

export default App;