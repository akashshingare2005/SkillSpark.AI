/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import { getAuthenticated, setAuthenticated } from '../utils/auth';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaCode } from 'react-icons/fa';

function AccountSidebar({ isOpen, onClose }) {
  const [userData, setUserData] = useState(null);
  const [editingField, setEditingField] = useState(null);
  const [showPrompt, setShowPrompt] = useState(false);
  const [promptField, setPromptField] = useState(null);
  const [newValue, setNewValue] = useState('');
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUserData(JSON.parse(storedUser));
    }
  }, []);

  const handleEdit = (field) => {
    if (field !== 'email') {
      setEditingField(field);
      setNewValue(field === 'password' ? '' : userData[field]);
    }
  };

  const handleSave = () => {
    setPromptField(editingField);
    setShowPrompt(true);
  };

  const updateUserData = async () => {
    try {
      const response = await axios.put('https://SkillSpark.AI.onrender.com/api/user/update', {
        email: userData.email,
        field: editingField,
        value: newValue
      });
  
      if (response.status === 200) {
        const updatedUserData = { ...userData, [editingField]: newValue };
        setUserData(updatedUserData);
        localStorage.setItem('user', JSON.stringify(updatedUserData));
        setEditingField(null);
      } else {
        console.error('Failed to update user data');
      }
    } catch (error) {
      console.error('Error updating user data:', error);
    }
  };

  const handleConfirm = () => {
    updateUserData();
    setShowPrompt(false);
    setPromptField(null);
    setNewValue('');
  };

  const handleCancel = () => {
    setShowPrompt(false);
    setEditingField(null);
    setPromptField(null);
    setNewValue('');
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleSignOut = () => {
    onClose();
    setAuthenticated(false);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
    setUserData(null);
    console.log("Signed out. New auth status:", getAuthenticated());
    navigate('/');
  };
   
  if (!userData) return null;

  return (
    <>
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50"
          onClick={handleOverlayClick}
        ></div>
      )}
      <div className={`fixed left-0 top-0 z-50 h-full w-full max-w-sm overflow-y-auto bg-gradient-to-br from-black to-violet-900 text-white shadow-lg backdrop-blur-lg transition-all duration-300 ease-in-out sm:max-w-md md:w-2/5 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className={`absolute inset-0 transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0'}`}>
          <div className="p-4 sm:p-6 md:p-8">
            <div className="rounded-3xl border border-yellow-500/30 bg-black bg-opacity-50 p-6 shadow-2xl backdrop-blur-sm transition-all duration-300 hover:scale-[1.01] hover:border-yellow-500">
              <div className="relative mx-auto mb-6 h-32 w-32 sm:h-36 sm:w-36 lg:h-48 lg:w-48">
                <div className="flex h-full w-full items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-indigo-100 via-violet-500 to-blue-700 shadow-lg">
                  <div className="absolute inset-0 bg-black opacity-10"></div>
                  <span className="relative z-10 font-sans text-5xl font-extrabold tracking-wider text-white sm:text-6xl">
                    {userData.name.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div className="absolute -bottom-3 -right-3 rounded-full bg-yellow-400 p-3 shadow-lg transition-transform duration-300 hover:rotate-0">
                  <FaCode className="text-black" size={20} />
                </div>
                <div className="absolute left-0 top-0 h-full w-full rounded-full border-4 border-yellow-300 opacity-50 animate-pulse"></div>
              </div>
            </div>
            <div className="mt-6 space-y-4">
              {['name', 'email', 'password'].map((field, index) => (
                <div key={field} className={`flex items-center justify-between rounded-lg bg-white/20 p-3 backdrop-blur-sm transition-all duration-300 ${isOpen ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}`} style={{transitionDelay: `${(index + 1) * 100}ms`}}>
                  <div className="flex-grow">
                    <label className="mb-1 block text-xs font-medium text-gray-200">{field.charAt(0).toUpperCase() + field.slice(1)}</label>
                    {editingField === field ? (
                      <input
                        type={field === 'password' ? 'password' : 'text'}
                        value={newValue}
                        onChange={(e) => setNewValue(e.target.value)}
                        className="w-full border-b border-gray-300 bg-transparent text-sm text-white focus:border-yellow-400 focus:outline-none"
                      />
                    ) : (
                      <p className="text-sm">
                        {field === 'password' ? '********' : userData[field]}
                      </p>
                    )}
                  </div>
                  {field !== 'email' && (
                    <>
                      {editingField === field ? (
                        <button onClick={handleSave} className="ml-2 text-yellow-400 transition-colors duration-200 hover:text-yellow-300">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                        </button>
                      ) : (
                        <button onClick={() => handleEdit(field)} className="ml-2 text-yellow-400 transition-colors duration-200 hover:text-yellow-300">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                          </svg>
                        </button>
                      )}
                    </>
                  )}
                </div>
              ))}
              <div className={`pt-6 transition-all duration-300 ${isOpen ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`} style={{transitionDelay: '400ms'}}>
                <button onClick={handleSignOut} className="w-full rounded-lg bg-yellow-500 px-6 py-3 text-lg font-semibold text-white transition-all duration-200 hover:scale-105 hover:from-red-600/90 hover:to-pink-600/90 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50">
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      {showPrompt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="w-full max-w-sm rounded-lg bg-gradient-to-br from-black to-violet-900 p-6 text-white shadow-lg">
            <h2 className="mb-4 text-xl font-bold">Confirm Change</h2>
            <p className="mb-6">Are you sure you want to change your {promptField}?</p>
            <div className="flex justify-end space-x-4">
              <button onClick={handleCancel} className="rounded bg-gray-600 px-4 py-2 text-white transition-colors duration-200 hover:bg-gray-700">
                Cancel
              </button>
              <button onClick={handleConfirm} className="rounded bg-yellow-500 px-4 py-2 text-white transition-colors duration-200 hover:bg-yellow-600">
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default AccountSidebar;
