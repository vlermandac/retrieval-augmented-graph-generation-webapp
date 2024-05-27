import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/input';
import { useContextValues } from '@/lib/response-context';

export default function InputExtended() {

  const inputRef = useRef<HTMLInputElement>(null);
  const { setResponseCtx, setResponseCtxId } = useContextValues();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const apiCall = async (query: string) => {
    const res = await fetch('http://localhost:8000/rag', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'query=' + query
    });
    const data = await res.json();
    setResponseCtx(data.rag.content);
    setResponseCtxId(data.ids);
    navigate('/response');
    setLoading(false);
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (inputRef.current && event.key === 'Enter') {
      setLoading(true);
      apiCall(inputRef.current.value);
    }
  }

  return (
    <div className='md:px-20'>
      <Input placeholder='Ask something' ref={inputRef} onKeyDown={handleKeyDown} />
      {loading && <p>Loading...</p>}
    </div>
  )
}
