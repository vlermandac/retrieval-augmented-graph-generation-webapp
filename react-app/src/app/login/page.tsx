import React, { useState, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { useNavigate } from 'react-router-dom';
import { login } from '@/lib/fetch';
                                                                              
export default function Login() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [error, setError] = useState<boolean>(false);
  const navigate = useNavigate();

  const apiCall = async (passcode: string) => {
    try {
      const response = await login(passcode);
      if (response.message !== 'Login successful') {
        setError(true);
        return;
      }
      navigate('/search');
    } catch (error) {
      setError(true);
    }
  }

   const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (inputRef.current && event.key === 'Enter') {
      apiCall(inputRef.current.value);
    }
  }

  return (
    <div className="my-52 flex flex-col items-center">
      <h1 className="text-4xl font-bold text-gray-800 w-full text-center tracking-tight m-5 md:text-6xl">Insert the passcode</h1>
      <div className="w-11/12 md:w-8/12">
        <Input placeholder='...' ref={inputRef} onKeyDown={handleKeyDown} />
        {error && <p className="text-red-500 text-center">Authentication Error</p>}
      </div>
    </div>
  );
}
