import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/ui/input';
import { useContextValues } from '@/lib/response-context';
import { fetchRAG } from '@/lib/fetch';

export default function InputExtended() {

  const inputRef = useRef<HTMLInputElement>(null);
  const { setResponseCtx, setResponseCtxId } = useContextValues();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const apiCall = async (query: string) => {
    const data = await fetchRAG(query);
    setResponseCtx(data.rag);
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
    <div className='px-4'>
      <Input placeholder='Consulta acerca de fechas, hechos, personas, instituciones, lugares, etc...' ref={inputRef} onKeyDown={handleKeyDown} />
      {loading && <p>Loading...</p>}
    </div>
  )
}
