/* eslint-disable no-unused-vars */
import { useState, useEffect, useRef, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import profileImg from '../assets/image.png';
import AccountSidebar from './AccountSidebar';
import { getAuthenticated, setAuthenticated } from '../utils/auth';
import { FaCode } from 'react-icons/fa';

function NavBar() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userData, setUserData] = useState(null);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  const handleAnalyze = () => {
    const isAuthenticated = getAuthenticated(); // Retrieve authentication status
    if (isAuthenticated) {
      navigate('/Analyze'); // Navigate to SignIn if not authenticated
    } else {
      navigate('/SignIn'); // Navigate to analyze if authenticated
    }
  }

  const checkAuthStatus = useCallback(() => {
    const authStatus = getAuthenticated();
    console.log("Current auth status:", authStatus);
    setIsAuthenticated(authStatus);
    if (authStatus) {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        setUserData(JSON.parse(storedUser));
      }
    } else {
      setUserData(null);
    }
  }, []);

  useEffect(() => {
    checkAuthStatus();
    // Set up an interval to check auth status every 5 seconds
    const intervalId = setInterval(checkAuthStatus, 5000);
    return () => clearInterval(intervalId);
  }, [checkAuthStatus]);

  const toggleDropdown = () => {
    setDropdownOpen(prevState => !prevState);
  };

  const openSidebar = () => {
    setSidebarOpen(true);
    setDropdownOpen(false);
  };

  const openProfile = () => {
    navigate('/profile');
    setDropdownOpen(false);
  };

  const handleNavAction = (path) => {
    navigate(path);
    setMenuOpen(false);
  };

  const handleClickOutside = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setDropdownOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSignOut = () => {
    setAuthenticated(false);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
    setUserData(null);
    console.log("Signed out. New auth status:", getAuthenticated());
    navigate('/');
  };

  console.log("Rendering NavBar. isAuthenticated:", isAuthenticated);
  return (
    <nav className="relative z-20 bg-black/95 shadow-md backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2 text-white">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-yellow-400 via-violet-500 to-blue-600 text-lg font-bold text-black shadow-lg sm:h-10 sm:w-10">
            S
          </div>
          <span className="text-lg font-bold tracking-wide sm:text-xl">SkillSpark.AI</span>
        </div>

        <div className="hidden items-center gap-6 md:flex">
          <ul className="flex items-center gap-6 text-white">
            <li className="relative group">
              <Link to="/" className="block py-2 text-lg font-mono transition hover:text-yellow-400">
                Home
              </Link>
              <span className="absolute bottom-0 left-0 h-0.5 w-0 bg-yellow-400 transition-all duration-500 group-hover:w-full"></span>
            </li>
            <li className="relative group">
              <button onClick={handleAnalyze} className="block py-2 text-lg font-mono transition hover:text-yellow-400">
                Analyze
              </button>
              <span className="absolute bottom-0 left-0 h-0.5 w-0 bg-yellow-400 transition-all duration-500 group-hover:w-full"></span>
            </li>
          </ul>

          {isAuthenticated ? (
            <div className="relative">
              <button
                type="button"
                className="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                id="user-menu-button"
                aria-expanded={dropdownOpen}
                onClick={toggleDropdown}
              >
                <span className="sr-only">Open user menu</span>
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-indigo-100 via-violet-500 to-blue-700">
                  <span className="text-base font-bold text-white">
                    {userData?.name?.charAt(0).toUpperCase()}
                  </span>
                </div>
              </button>
              {dropdownOpen && (
                <div
                  ref={dropdownRef}
                  className="absolute right-0 mt-2 w-48 rounded-md bg-white py-1 shadow-lg dark:bg-gray-700 dark:divide-gray-600"
                  id="user-dropdown"
                >
                  <div className="px-4 py-3">
                    <span className="block text-sm text-gray-900 dark:text-white">{userData.name}</span>
                    <span className="block truncate text-sm text-gray-500 dark:text-gray-400">{userData.email}</span>
                  </div>
                  <ul className="py-2" aria-labelledby="user-menu-button">
                    <li>
                      <button
                        className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                        onClick={openSidebar}
                      >
                        Account
                      </button>
                    </li>
                    <li>
                      <button
                        className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                        onClick={openProfile}
                      >
                        Profile
                      </button>
                    </li>
                    <li>
                      <button
                        className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
                        onClick={handleSignOut}
                      >
                        Sign out
                      </button>
                    </li>
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <Link to="/SignIn" className="text-base font-mono text-white transition hover:text-yellow-400">Sign In</Link>
          )}
        </div>

        <div className="flex items-center gap-3 md:hidden">
          {isAuthenticated ? (
            <button
              type="button"
              className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-indigo-100 via-violet-500 to-blue-700 text-sm font-bold text-white"
              onClick={toggleDropdown}
            >
              {userData?.name?.charAt(0).toUpperCase()}
            </button>
          ) : (
            <Link to="/SignIn" className="text-sm font-mono text-white">Sign In</Link>
          )}

          <button
            type="button"
            className="flex h-10 w-10 items-center justify-center rounded-md border border-white/20 bg-white/5 text-xl text-white"
            onClick={() => setMenuOpen((prev) => !prev)}
            aria-label="Toggle menu"
          >
            ☰
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="border-t border-white/10 bg-black/95 px-4 py-3 md:hidden">
          <div className="flex flex-col space-y-3 text-white">
            <button onClick={() => handleNavAction('/')} className="text-left text-base font-mono">Home</button>
            <button onClick={handleAnalyze} className="text-left text-base font-mono">Analyze</button>
            {isAuthenticated && (
              <>
                <button onClick={openSidebar} className="text-left text-base font-mono">Account</button>
                <button onClick={openProfile} className="text-left text-base font-mono">Profile</button>
                <button onClick={handleSignOut} className="text-left text-base font-mono">Sign out</button>
              </>
            )}
          </div>
        </div>
      )}

      <AccountSidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
    </nav>
  );
}

export default NavBar;
