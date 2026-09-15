/* eslint-disable react/no-unescaped-entities */
/* eslint-disable no-unused-vars */
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import Logo from '../assets/Logo.png'
import { getAuthenticated, setAuthenticated } from '../utils/auth';

const SignIn = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navi = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        if (!email || !password) {
            setError('Email and password are required');
            return;
        }
        //console.log('Sending login request with:', { email, password });

        try {
            const response = await axios.post(
                '/api/login',
                { email, password },
                { headers: { 'Content-Type': 'application/json' } }
            );
            //console.log('Login successful:', response.data.message);
            setAuthenticated(true);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            console.log("Signed in. New auth status:", getAuthenticated());
            navi('/');
        } catch (error) {
            console.error('Login failed:', error);
            setError(error.response?.data?.message || 'Invalid email or password');
        }
    };

    return (
        <section className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-4 py-8 sm:px-6 lg:max-w-lg lg:px-8">
                <a href="#" className="mb-6 flex items-center text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">
                    <img className="mr-2 h-8 w-8" src={Logo} alt="logo" />
                    SkillSpark.AI
                </a>
                <div className="w-full rounded-lg bg-gradient-to-r from-blue-800 to-gray-400 shadow dark:border dark:border-gray-700 md:mt-0 xl:p-0">
                    <div className="space-y-4 p-4 sm:p-8 md:space-y-6">
                        <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 dark:text-white md:text-2xl">
                            Sign in to your account
                        </h1>
                        <form className="space-y-4 md:space-y-6" onSubmit={handleSubmit}>
                            <div>
                                <label htmlFor="email" className="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Your email</label>
                                <input type="email" name="email" id="email" className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-primary-600 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                                    placeholder="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)} required />
                            </div>
                            <div>
                                <label htmlFor="password" className="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Password</label>
                                <input type="password" name="password" id="password"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)} className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-primary-600 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500" required />
                            </div>
                            {error && <p className="text-sm text-red-500">{error}</p>}
                            <button type="submit" className="w-full rounded-lg bg-white px-5 py-2.5 text-center text-sm font-medium text-black focus:outline-none focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-800">Sign in</button>
                            <p className="text-sm font-semibold text-black">
                                Don't have an account yet? <Link to="/signup" className="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</Link>
                            </p>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default SignIn;