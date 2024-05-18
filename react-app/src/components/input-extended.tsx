import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/input';
import { useResponseCtx } from '@/lib/response-context';
import { useGraphCtx } from '@/lib/graph-context';

export default function InputExtended() {

  const inputRef = useRef<HTMLInputElement>(null);
  const { responseCtx, setResponseCtx } = useResponseCtx();
  const { graphCtx, setGraphCtx } = useGraphCtx();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

    const apiCall = async (query: string) => {
      const response = await fetch('http://localhost:8000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body:  'user_query=' + query
      });
      const data = await response.json();
      console.log(data);
      navigate('/response');
      setResponseCtx(data.rag.content);
      setGraphCtx(data.ids);
      setLoading(false);
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (inputRef.current && event.key === 'Enter') {
      setLoading(true);
      apiCall(inputRef.current.value);
    }
  }

  return (
    <div className='px-40'>
      <Input placeholder='e.g., who is moby dick' ref={inputRef} onKeyDown={handleKeyDown} />
      {loading && <p>Loading...</p>}
    </div>
  )
}
