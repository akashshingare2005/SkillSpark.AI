/* eslint-disable no-unused-vars */
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

function SignUp() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSignUp = async (e) => {
        e.preventDefault();
        setError('');
        if (!email || !password || !confirmPassword) {
            setError('All fields are required');
            return;
        }
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        try {
            const response = await axios.post(
                '/api/signup',
                { name,email, password },
                { headers: { 'Content-Type': 'application/json' } }
            );
            console.log('Signup successful:', response.data.message);
            navigate('/SignIn');
        } catch (error) {
            console.error('Signup failed:', error);
            setError(error.response?.data?.message || 'Signup failed');
        }

    };
    // const handleLogin = () =>{
    //     navigate('/SignIn');
    // }

    return (
        <section className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-4 py-8 sm:px-6 lg:max-w-lg lg:px-8">
                <div className="w-full rounded-lg bg-gradient-to-r from-blue-800 to-gray-400 shadow dark:border dark:border-gray-700 md:mt-0 xl:p-0">
                    <div className="space-y-4 p-4 sm:p-8 md:space-y-6">
                        <h1 className="text-xl font-bold leading-tight tracking-tight text-black dark:text-white md:text-2xl">
                            Create an account
                        </h1>
                        <form className="space-y-4 md:space-y-6" onSubmit={handleSignUp}>
                        <div>
                                <label htmlFor="name" className="mb-2 block text-sm font-medium text-black dark:text-white">
                                    Name
                                </label>
                                <input
                                    name="name"
                                    id="name"
                                    placeholder='My name is...'
                                    className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-black focus:border-primary-600 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                                    required
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </div>
                            <div>
                                <label htmlFor="email" className="mb-2 block text-sm font-medium text-black dark:text-white">
                                    Your email
                                </label>
                                <input
                                    type="email"
                                    name="email"
                                    id="email"
                                    className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-black focus:border-primary-600 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                                    placeholder="name@company.com"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </div>
                            <div>
                                <label htmlFor="password" className="mb-2 block text-sm font-medium text-black dark:text-white">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    name="password"
                                    id="password"
                                    placeholder="••••••••"
                                    className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-black focus:border-primary-600 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            <div>
                                <label htmlFor="confirm-password" className="mb-2 block text-sm font-medium text-black dark:text-white">
                                    Confirm Password
                                </label>
                                <input
                                    type="password"
                                    name="confirm-password"
                                    id="confirm-password"
                                    placeholder="••••••••"
                                    className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-black focus:border-primary-600 focus:ring-primary-600 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                                    required
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                />
                            </div>
                            {error && <p className="text-sm text-red-500">{error}</p>}
                            <button
                                type="submit"
                                className="w-full rounded-lg bg-white px-5 py-2.5 text-center text-sm font-medium text-black focus:outline-none focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-800"
                            >
                                Create an account
                            </button>
                            <p className="text-sm font-light text-black">
                                Already have an account? <Link to={"/SignIn"} className="font-medium text-primary-600 hover:underline dark:text-primary-500">Login here</Link>
                            </p>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default SignUp;