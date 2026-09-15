import Chatbot from './Chatbot';
/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NavBar from './NavBar';
import profileImg from '../assets/image.png';
import { FaGithub, FaLinkedin, FaTwitter, FaEnvelope, FaCode, FaPlus, FaEdit } from 'react-icons/fa';
import { VerticalTimeline, VerticalTimelineElement } from 'react-vertical-timeline-component';
import 'react-vertical-timeline-component/style.min.css';

function Profile() {
  const [newSkill, setNewSkill] = useState('');
  const [skills, setSkills] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [position, setPosition] = useState('');
  const [tagline, setTagline] = useState('"Catchy Tagline!"');
  const [error, setError] = useState(null);
  const [userName, setUserName] = useState('User');
  useEffect(() => {
    fetchUserName();
    fetchPosition();
    fetchTagline();
    fetchSkills();
  }, []);
  const fetchUserName = () => {
    const userString = localStorage.getItem('user');
    if (userString) {
      const user = JSON.parse(userString);
      setUserName(user.name || 'User');
    }
  };
  const fetchPosition = async () => {
    try {
      const userString = localStorage.getItem('user');
      const user = userString ? JSON.parse(userString) : null;
      if (!user || !user.email) {
        console.error('User email not found in local storage');
        return;
      }
      
      const response = await axios.get(`https://SkillSpark.AI.onrender.com/api/user/job?email=${encodeURIComponent(user.email)}`);
      if (response.data && response.data.job) {
        setPosition(response.data.job);
      }
    } catch (error) {
      console.error('Error fetching position:', error);
      setPosition('Developer');  // Set default job if there's an error
    }
  };
  
  const savePosition = async () => {
    try {
      const userString = localStorage.getItem('user');
      const user = userString ? JSON.parse(userString) : null;
      if (!user || !user.email) {
        console.error('User email not found in local storage');
        return;
      }
      
      const jobToSave = position.trim() || 'Developer';
      
      await axios.post('https://SkillSpark.AI.onrender.com/api/user/job', { 
        email: user.email, 
        job: jobToSave
      });
      console.log('Position updated successfully');
      setPosition(jobToSave); // Update the state immediately
      fetchPosition(); // Refetch to ensure we have the latest data
    } catch (error) {
      console.error('Error saving position:', error);
    }
  };
  
  const fetchSkills = async () => {
    try {
      const userString = localStorage.getItem('user');
      const user = userString ? JSON.parse(userString) : null;
      if (!user || !user.email) {
        console.error('User email not found in local storage');
        return;
      }
      
      const response = await axios.get(`https://SkillSpark.AI.onrender.com/api/skills?email=${encodeURIComponent(user.email)}`);
      if (response.data && Array.isArray(response.data.skills)) {
        setSkills(response.data.skills);
      } else {
        setSkills([]);
      }
    } catch (error) {
      console.error('Error fetching skills:', error);
      setSkills([]);
    }
  };
  
  const addNewSkill = async (e) => {
    e.preventDefault();
    if (newSkill.trim() !== '') {
      try {
        const userString = localStorage.getItem('user');
        const user = userString ? JSON.parse(userString) : null;
        if (!user || !user.email) {
          console.error('User email not found in local storage');
          return;
        }
        const response = await axios.post('https://SkillSpark.AI.onrender.com/api/skills', { 
          email: user.email, 
          skill: newSkill.trim() 
        });
        setSkills([...skills, response.data.skill]);
        setNewSkill('');
      } catch (error) {
        console.error('Error adding new skill:', error);
      }
    }
  };
  

  // Fetch tagline
const fetchTagline = async () => {
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.email) {
      throw new Error('User email not found');
    }
    const response = await axios.get(`https://SkillSpark.AI.onrender.com/api/user/tagline?email=${encodeURIComponent(user.email)}`);
    setTagline(response.data.tagline);
  } catch (error) {
    console.error('Error fetching tagline:', error);
    setTagline('A catchy tagline!');
  }
};

// Update tagline
const saveTagline = async () => {
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.email) {
      throw new Error('User email not found');
    }
    await axios.post('https://SkillSpark.AI.onrender.com/api/user/tagline', {
      email: user.email,
      tagline: tagline
    });
    console.log('Tagline updated successfully');
  } catch (error) {
    console.error('Error saving tagline:', error);
  }
};

  const handleEdit = () => {
    setIsEditing(!isEditing);
  };

  const handleInputBlur = () => {
    setIsEditing(false);
    const updatedPosition = position.trim() || 'Developer';
  const updatedTagline = tagline.trim() || 'A catchy tagline!';
  setPosition(updatedPosition);
  setTagline(updatedTagline);
  savePosition();
  saveTagline();
  };

  if (error) {
    return <div className="text-red-500 text-center mt-10">{error}</div>;
  }

  return (
    <div className='min-h-screen flex flex-col bg-gradient-to-r from-blue-900 via-violet-900 to-black'>
      <NavBar className="sticky top-0 z-50" />
      <div className="mt-8 flex flex-grow flex-col gap-8 px-4 sm:px-6 lg:mt-16 lg:flex-row lg:px-12">
        <div className="w-full space-y-8 lg:w-1/2">
          <div className="rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-6 shadow-2xl backdrop-blur-sm transition-all duration-300 hover:scale-[1.01] hover:border-yellow-500 sm:p-8 lg:p-10">
            <button 
              onClick={handleEdit}
              className="absolute left-4 top-4 rounded-full bg-yellow-400 p-2 shadow-lg transition-all duration-300 hover:scale-110 hover:bg-yellow-500"
            >
              <FaEdit className="text-black" size={20} />
            </button>
            <div className="relative mx-auto mb-6 h-32 w-32 sm:mb-8 sm:h-40 sm:w-40 lg:h-48 lg:w-48">
              <div className="flex h-full w-full items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-indigo-100 via-violet-500 to-blue-700 shadow-lg">
                <div className="absolute inset-0 bg-black opacity-10"></div>
                <span className="relative z-10 font-sans text-5xl font-extrabold tracking-wider text-white sm:text-6xl lg:text-7xl">
                  {userName.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="absolute -bottom-3 -right-3 rounded-full bg-yellow-400 p-3 shadow-lg transition-transform duration-300 hover:rotate-0 sm:p-3">
                <FaCode className="text-black" size={20} />
              </div>
              <div className="absolute left-0 top-0 h-full w-full rounded-full border-4 border-yellow-300 opacity-50 animate-pulse"></div>
            </div> 
            <h2 className="mb-3 text-center font-sans text-3xl font-bold text-yellow-400 sm:text-4xl lg:text-5xl">{userName}</h2>
            {isEditing ? (
        <div className="space-y-2">
          <input
            type="text"
            value={position}
            onChange={(e) => setPosition(e.target.value)}
            onBlur={handleInputBlur}
            className="w-full rounded-lg border-b border-yellow-400 bg-transparent px-2 py-1 text-center font-sans text-xl text-white focus:border-yellow-500 focus:outline-none sm:text-2xl"
          />
          <input
            type="text"
            value={tagline}
            onChange={(e) => setTagline(e.target.value)}
            onBlur={handleInputBlur}
            className="w-full rounded-lg border-b border-yellow-400 bg-transparent px-2 py-1 text-center font-sans text-base italic text-gray-300 focus:border-yellow-500 focus:outline-none sm:text-lg"
          />
        </div>
      ) : (
        <>
          <p className="mb-4 text-center font-sans text-xl text-white sm:text-2xl">{position}</p>
          <p className="mb-6 text-center font-sans text-base italic text-gray-300 sm:mb-8 sm:text-lg">{tagline}</p>
        </>
      )}
            <div className="flex justify-center space-x-4 sm:space-x-6">
              {[FaGithub, FaLinkedin, FaTwitter, FaEnvelope].map((Icon, index) => (
                <a key={index} href="#" className="rounded-full bg-gray-800 p-3 shadow-lg transition-all duration-300 hover:scale-110 hover:bg-yellow-400 sm:p-4">
                  <Icon className="text-gray-300 hover:text-black" size={20} />
                </a>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-6 shadow-2xl backdrop-blur-sm transition-all duration-300 hover:scale-[1.01] hover:border-yellow-500 sm:p-8 lg:p-10">
            <h3 className="mb-6 font-sans text-2xl font-semibold text-yellow-400 sm:text-3xl lg:text-4xl">Skills</h3>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6">
              {skills.map((skill, index) => (
                <div 
                  key={index} 
                  className="flex items-center justify-center rounded-xl bg-gray-800 p-4 transition-all duration-300 hover:scale-105 hover:bg-yellow-400 hover:shadow-[0_0_20px_rgba(251,191,36,0.7)]"
                >
                  <span className="font-sans text-base text-gray-300 hover:text-black sm:text-lg">
                    {skill.title}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="w-full rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-4 shadow-2xl backdrop-blur-sm sm:p-6 lg:w-1/2 lg:p-6">
          <h3 className="mb-6 text-center font-sans text-2xl font-semibold text-yellow-400 sm:text-3xl lg:text-4xl">Timeline</h3>
          <VerticalTimeline layout="1-column" lineColor="rgba(251, 191, 36, 0.3)">
            {/* Add Skill Input */}
            <VerticalTimelineElement
              className="vertical-timeline-element--work"
              contentStyle={{ 
                background: 'rgba(31, 41, 55, 0.8)', 
                color: '#fff', 
                boxShadow: '0 3px 0 #fbbf24', 
                borderRadius: '15px',
                padding: '20px'
              }}
              contentArrowStyle={{ borderRight: '7px solid rgba(31, 41, 55, 0.8)' }}
              iconStyle={{ background: '#fbbf24', color: '#1f2937' }}
              icon={<FaPlus />}
            >
              <form onSubmit={addNewSkill} className="flex flex-col">
                <input
                  type="text"
                  value={newSkill}
                  onChange={(e) => setNewSkill(e.target.value)}
                  className="w-full p-3 bg-transparent text-yellow-400 text-2l font-bold mb-1 font-sans border-b-2 border-yellow-400 focus:outline-none focus:border-yellow-500 transition-all duration-300"
                  placeholder="Press Enter to add a new skill"
                />
              </form>
            </VerticalTimelineElement>
            {/* Existing Skills */}
            {skills.map((skill, index) => (
              <VerticalTimelineElement
                key={index}
                className="vertical-timeline-element--work"
                contentStyle={{ background: 'rgba(31, 41, 55, 0.8)', color: '#fff', boxShadow: '0 3px 0 #fbbf24', borderRadius: '15px' }}
                contentArrowStyle={{ borderRight: '7px solid rgba(31, 41, 55, 0.8)' }}
                date={skill.date}
                iconStyle={{ background: '#fbbf24', color: '#1f2937' }}
                icon={<FaCode />}
              >
                <h3 className="text-yellow-400 text-2xl font-bold mb-1 font-sans">{skill.title}</h3>
                <p className="text-gray-300 font-sans">Mastered {skill.title}</p>
              </VerticalTimelineElement>
            ))}
          </VerticalTimeline>
        </div>
      </div>
      <Chatbot />
    </div>
  );
}

export default Profile;
