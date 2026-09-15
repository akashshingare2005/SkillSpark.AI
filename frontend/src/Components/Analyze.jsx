  import Chatbot from './Chatbot';
  /* eslint-disable react/prop-types */
  /* eslint-disable no-unused-vars */
  import React, { useState, useEffect } from 'react';
  import axios from 'axios';
  import NavBar from './NavBar';
  import { SkillsVisualization } from './SkillsVisualization';
  import 'react-vertical-timeline-component/style.min.css';

  const SkillCheckbox = ({ skill, completed, onToggle }) => (
    <div className="flex items-center mb-2">
      <div 
        onClick={onToggle}
        className={`w-5 h-5 border-2 rounded mr-2 cursor-pointer ${completed ? 'bg-yellow-400 border-yellow-400' : 'border-gray-400'}`}
      >
        {completed && (
          <svg className="w-4 h-4 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        )}
      </div>
      <span className={`${completed ? 'line-through text-gray-500' : 'text-gray-300'}`}>{skill}</span>
    </div>
  );

  function Analyze() {
    const [highlightedSkill, setHighlightedSkill] = useState(null);
    const [animatedNumber, setAnimatedNumber] = useState(0);
    const [skills, setSkills] = useState([]);
    const [skillsData, setSkillsData] = useState({
      labels: [],
      datasets: [
        {
          label: 'Your Skills',
          data: [],
          backgroundColor: 'rgba(251, 191, 36, 0.2)',
          borderColor: 'rgba(251, 191, 36, 1)',
          pointBackgroundColor: 'rgba(251, 191, 36, 1)',
        },
        {
          label: 'Required Skills',
          data: [],
          backgroundColor: 'rgba(167, 139, 250, 0.2)',
          borderColor: 'rgba(167, 139, 250, 1)',
          pointBackgroundColor: 'rgba(167, 139, 250, 1)',
        },
      ],
    });

    const [resume, setResume] = useState(null);
    const [jobDescription, setJobDescription] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [matchRate, setMatchRate] = useState(0);
    const [marketFit, setMarketFit] = useState(0);
    const [skillsToImprove, setSkillsToImprove] = useState(0);
    const [loadingSkills, setLoadingSkills] = useState({});

    useEffect(() => {
      // Load saved data from local storage
      const savedAnalysisResult = localStorage.getItem('analysisResult');
      const savedSkills = localStorage.getItem('skills');
      const savedSkillsData = localStorage.getItem('skillsData');
      const savedMatchRate = localStorage.getItem('matchRate');
      const savedMarketFit = localStorage.getItem('marketFit');
      const savedSkillsToImprove = localStorage.getItem('skillsToImprove');
    
      if (savedAnalysisResult) {
        setAnalysisResult(JSON.parse(savedAnalysisResult));
        setSkills(JSON.parse(savedSkills));
        setSkillsData(JSON.parse(savedSkillsData));
        setMatchRate(JSON.parse(savedMatchRate));
        setMarketFit(JSON.parse(savedMarketFit));
        setSkillsToImprove(JSON.parse(savedSkillsToImprove));
      }
    }, []); // This effect runs only once on component mount
    
    useEffect(() => {
      const intervalId = setInterval(() => {
        setHighlightedSkill(prevSkill => {
          const newSkill = skills[Math.floor(Math.random() * skills.length)]?.name;
          return newSkill !== prevSkill ? newSkill : prevSkill;
        });
      }, 2000);
    
      return () => clearInterval(intervalId);
    }, [skills]); // This effect depends on skills, but won't cause unnecessary re-renders
    
    useEffect(() => {
      const animationId = setInterval(() => {
        setAnimatedNumber(prev => (prev + 1) % 101);
      }, 50);
    
      return () => clearInterval(animationId);
    }, []); // This effect runs independently of other state

    const handleResumeChange = (e) => {
      setResume(e.target.files[0]);
    };

    const handleJobDescriptionChange = (e) => {
      setJobDescription(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      setIsLoading(true);

      const formData = new FormData();
      formData.append('resume', resume);
      formData.append('job_description', jobDescription);

      try {
        const response = await axios.post('/api/skill-analyzer', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const newAnalysisResult = response.data;
        setAnalysisResult(newAnalysisResult);

        const totalRequiredSkills = newAnalysisResult.skills_required_in_job.length;
        const matchingSkillsCount = newAnalysisResult.matching_skills.length;
        const newMatchRate = Math.round(((matchingSkillsCount + 1) / totalRequiredSkills) * 100);
        setMatchRate(newMatchRate);

        const skillsToImproveCount = newAnalysisResult.skills_to_improve.length;
        setSkillsToImprove(skillsToImproveCount);

        const newMarketFit = Math.round(((skillsToImproveCount + 1) / totalRequiredSkills) * 100);
        setMarketFit(newMarketFit);

        const newSkills = newAnalysisResult.skills_to_improve.map((skill, index) => ({
          id: index + 1,
          name: skill,
          completed: false,
        }));
        setSkills(newSkills);

        const newSkillsData = {
          labels: newAnalysisResult.skills_required_in_job,
          datasets: [
            {
              label: 'Your Skills',
              data: newAnalysisResult.skills_required_in_job.map(skill => 
                newAnalysisResult.skills_from_resume.includes(skill) ? 5 : 0
              ),
              backgroundColor: 'rgba(251, 191, 36, 0.2)',
              borderColor: 'rgba(251, 191, 36, 1)',
              pointBackgroundColor: 'rgba(251, 191, 36, 1)',
            },
            {
              label: 'Required Skills',
              data: newAnalysisResult.skills_required_in_job.map(() => 5),
              backgroundColor: 'rgba(167, 139, 250, 0.2)',
              borderColor: 'rgba(167, 139, 250, 1)',
              pointBackgroundColor: 'rgba(167, 139, 250, 1)',
            },
          ],
        };
        setSkillsData(newSkillsData);

        // Save data to local storage
        localStorage.setItem('analysisResult', JSON.stringify(newAnalysisResult));
        localStorage.setItem('skills', JSON.stringify(newSkills));
        localStorage.setItem('skillsData', JSON.stringify(newSkillsData));
        localStorage.setItem('matchRate', JSON.stringify(newMatchRate));
        localStorage.setItem('marketFit', JSON.stringify(newMarketFit));
        localStorage.setItem('skillsToImprove', JSON.stringify(skillsToImproveCount));

      } catch (error) {
        console.error('Error during analysis:', error);
        // Handle error (e.g., show an error message to the user)
      } finally {
        setIsLoading(false);
      }
    };

    const toggleSkill = (id) => {
      const updatedSkills = skills.map(skill => 
        skill.id === id ? { ...skill, completed: !skill.completed } : skill
      );
      setSkills(updatedSkills);
      localStorage.setItem('skills', JSON.stringify(updatedSkills));
    };

   const sendSkillToBackend = async (e, skillName) => {
  e.preventDefault();
  e.stopPropagation();
  
  console.log('Sending skill for recommendation:', skillName);
  setLoadingSkills(prev => ({ ...prev, [skillName]: true }));
  
  try {
    const response = await axios.post('/recommend_course', 
      { resource: skillName },
      { 
        headers: { 
          'Content-Type': 'application/json' 
        },
        timeout: 15000
      }
    );
    
    console.log('Full response:', response);
    console.log('Response data:', response.data);
    
    if (response.data && response.data.recommendation) {
      let url = response.data.recommendation;
      
      console.log('Original URL:', url);
      
      // Ensure URL is properly formatted
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
        console.log('Fixed URL:', url);
      }
      
      // Test if URL is valid
      try {
        new URL(url);
        console.log('URL is valid, opening:', url);
        
        // Open in new tab
        const newWindow = window.open(url, '_blank', 'noopener,noreferrer');
        
        if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {
          // Popup blocked, redirect current page
          window.location.href = url;
        }
      } catch (urlError) {
        console.error('Invalid URL:', urlError);
        // Fallback to Udemy search
        const fallbackUrl = `https://www.udemy.com/courses/search/?src=ukw&q=${encodeURIComponent(skillName)}`;
        window.open(fallbackUrl, '_blank', 'noopener,noreferrer');
      }
    } else {
      console.error('No recommendation in response:', response.data);
      // Fallback to Udemy search
      const fallbackUrl = `https://www.udemy.com/courses/search/?src=ukw&q=${encodeURIComponent(skillName)}`;
      window.open(fallbackUrl, '_blank', 'noopener,noreferrer');
    }
  } catch (error) {
    console.error('Error details:', error);
    
    if (error.response) {
      // Server responded with error status
      console.error('Server error response:', error.response.data);
      console.error('Status code:', error.response.status);
      
      // Fallback to Udemy search
      const fallbackUrl = `https://www.udemy.com/courses/search/?src=ukw&q=${encodeURIComponent(skillName)}`;
      window.open(fallbackUrl, '_blank', 'noopener,noreferrer');
      
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received from server');
      
      // Fallback to Udemy search
      const fallbackUrl = `https://www.udemy.com/courses/search/?src=ukw&q=${encodeURIComponent(skillName)}`;
      window.open(fallbackUrl, '_blank', 'noopener,noreferrer');
      
    } else {
      // Something else happened
      console.error('Error message:', error.message);
      
      // Fallback to Udemy search
      const fallbackUrl = `https://www.udemy.com/courses/search/?src=ukw&q=${encodeURIComponent(skillName)}`;
      window.open(fallbackUrl, '_blank', 'noopener,noreferrer');
    }
  } finally {
    setLoadingSkills(prev => ({ ...prev, [skillName]: false }));
  }
};

    return (
      <div className='min-h-screen flex flex-col bg-gradient-to-r from-blue-900 via-violet-900 to-black'>
        <NavBar />
        <div className="flex-grow overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="mx-auto max-w-6xl">
            <div className="mb-8 rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-4 shadow-2xl backdrop-blur-sm sm:p-6 lg:p-8">
              <h2 className="mb-4 text-center font-sans text-3xl font-bold text-yellow-400 sm:text-4xl lg:text-5xl">Skill Analyzer</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="resume" className="mb-2 block text-sm font-medium text-yellow-400 sm:text-base">Upload Resume</label>
                  <input type="file" id="resume" onChange={handleResumeChange} className="w-full rounded bg-gray-800 p-2.5 text-sm text-white sm:text-base" />
                </div>
                <div>
                  <label htmlFor="jobDescription" className="mb-2 block text-sm font-medium text-yellow-400 sm:text-base">Upload Job Description</label>
                  <input type="file" id="jobDescription" onChange={handleJobDescriptionChange} className="w-full rounded bg-gray-800 p-2.5 text-sm text-white sm:text-base" />
                </div>
                <button type="submit" className="w-full rounded bg-yellow-400 px-4 py-3 text-sm font-bold text-black transition-colors hover:bg-yellow-500 sm:text-base">
                  {isLoading ? 'Analyzing...' : 'Analyze Skills'}
                </button>
              </form>
            </div>

            {analysisResult && (
              <div className="mb-8 rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-4 shadow-2xl backdrop-blur-sm sm:p-6 lg:p-8">
                <h2 className="mb-4 text-center font-sans text-3xl font-bold text-yellow-400 sm:text-4xl lg:text-5xl">Analysis Dashboard</h2>
                <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
                  <div className="rounded-xl bg-gray-800 p-4 text-center transition-all duration-300 hover:scale-[1.01] sm:p-6">
                    <div className="mb-2 text-4xl font-bold text-white sm:text-5xl lg:text-6xl">{matchRate}%</div>
                    <div className="text-sm text-yellow-400 sm:text-base">Match Rate</div>
                  </div>
                  <div className="rounded-xl bg-gray-800 p-4 text-center transition-all duration-300 hover:scale-[1.01] sm:p-6">
                    <div className="mb-2 text-4xl font-bold text-white sm:text-5xl lg:text-6xl">{skillsToImprove}</div>
                    <div className="text-sm text-yellow-400 sm:text-base">Skills to Improve</div>
                  </div>
                  <div className="rounded-xl bg-gray-800 p-4 text-center transition-all duration-300 hover:scale-[1.01] sm:p-6">
                    <div className="mb-2 text-4xl font-bold text-white sm:text-5xl lg:text-6xl">{marketFit}%</div>
                    <div className="text-sm text-yellow-400 sm:text-base">Market Fit</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <div className="rounded-xl bg-gray-800 p-4 sm:p-6">
                    <h3 className="mb-4 text-xl font-semibold text-yellow-400 sm:text-2xl">Your Skills</h3>
                    <ul className="list-inside list-disc space-y-2 text-sm text-white sm:text-base">
                      {analysisResult.skills_from_resume.map((skill, index) => (
                        <li key={index}>{skill}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="rounded-xl bg-gray-800 p-4 sm:p-6">
                    <h3 className="mb-4 text-xl font-semibold text-yellow-400 sm:text-2xl">Required Skills</h3>
                    <ul className="list-inside list-disc space-y-2 text-sm text-white sm:text-base">
                      {analysisResult.skills_required_in_job.map((skill, index) => (
                        <li key={index}>{skill}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}

            <div className="flex flex-col gap-8 lg:flex-row lg:space-x-8">
              <div className="w-full lg:w-2/3">
                {analysisResult && <SkillsVisualization analysisResult={analysisResult} />}

                <div className="mb-8 rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-4 shadow-2xl backdrop-blur-sm sm:p-6 lg:p-8">
                  <h3 className="mb-4 font-sans text-2xl font-semibold text-yellow-400 sm:text-3xl">Recommended Improvements</h3>
                  <div className="mb-6 grid grid-cols-1 gap-3 sm:gap-4">
                    {skills.map((skill) => (
                      <div 
                        key={skill.id}
                        className={`flex flex-col gap-3 rounded-xl p-3 transition-all duration-300 hover:scale-[1.01] sm:flex-row sm:items-center sm:justify-between sm:p-4 ${highlightedSkill === skill.name ? 'bg-yellow-400 shadow-[0_0_20px_rgba(251,191,36,0.7)]' : 'bg-gray-800'}`}
                      >
                        <span className={`font-sans text-base sm:text-lg ${highlightedSkill === skill.name ? 'text-black' : 'text-gray-300'}`}>
                          {skill.name}
                        </span>
                        <button 
                          onClick={(e) => sendSkillToBackend(e, skill.name)}
                          className={`inline-flex w-full items-center justify-center rounded px-4 py-2 text-sm font-bold text-white transition-colors duration-300 sm:w-auto ${skill.completed ? 'bg-gray-600' : 'bg-blue-500 hover:bg-blue-600'}`}
                          disabled={loadingSkills[skill.name]}
                        >
                          {loadingSkills[skill.name] ? (
                            <svg className="h-5 w-5 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                          ) : 'Get Course'}
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="w-full lg:w-1/3">
                <div className="mb-8 rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-4 shadow-2xl backdrop-blur-sm sm:p-6">
                  <h3 className="mb-3 font-sans text-2xl font-semibold text-yellow-400">Skills to Improve</h3>
                  <div className="max-h-60 overflow-y-auto">
                    {skills.map((skill) => (
                      <SkillCheckbox 
                        key={skill.id}
                        skill={skill.name}
                        completed={skill.completed}
                        onToggle={() => toggleSkill(skill.id)}
                      />
                    ))}
                  </div>
                </div>

                <div className="mb-8 rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-4 shadow-2xl backdrop-blur-sm sm:p-6">
                  <h3 className="mb-3 font-sans text-2xl font-semibold text-yellow-400">Estimated Study Time</h3>
                  <p className="text-base text-white sm:text-lg">
                    Total time to master all skills:
                  </p>
                  <p className="mt-2 text-2xl font-bold text-yellow-400 sm:text-3xl">
                    ~{skills.length * 10} hours
                  </p>
                  <p className="mt-2 text-xs text-gray-400 sm:text-sm">
                    (Assuming an average of 10 hours per skill)
                  </p>
                </div>
              </div>
            </div>
          </div>
          <Chatbot />
        </div>
      </div>
    );
  }

  export default Analyze;