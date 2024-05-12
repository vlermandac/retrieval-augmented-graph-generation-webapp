'use client';
import React, { useState, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { useValue } from '@/lib/response-context';
import { useRouter } from 'next/navigation';
import { useGraphCtx } from '@/lib/graph-context';

export default function InputExtended() {

  const inputRef = useRef<HTMLInputElement>(null);
  const { value, setValue } = useValue();
  const { graph, setGraph } = useGraphCtx();
  const [loading, setLoading] = useState(false);
  const router = useRouter();

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
      router.push('/response');
      setValue(data.rag.content);
      setGraph(data.ids);
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
      <Input placeholder='e.g., who are the main characters in the goodfellas film' ref={inputRef} onKeyDown={handleKeyDown} />
      {loading && <p>Loading...</p>}
    </div>
  )
}
