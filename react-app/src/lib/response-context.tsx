import React, { createContext, useContext, useState } from 'react';

interface ValueProviderProps {
  children: React.ReactNode;
}

interface ValueContextType {
  responseCtx: string;
  responseCtxId: number[];
  setResponseCtx: (responseCtx: string) => void; 
  setResponseCtxId: (idList: number[]) => void;
}

const ValueContext = createContext<ValueContextType | undefined>(undefined);

export default function ValueProvider({ children }: ValueProviderProps) {

  const [responseCtx, setResponseCtx] = useState('');
  const [responseCtxId, setResponseCtxId] = useState<number[]>([]);

  return (
    <ValueContext.Provider value={{ responseCtx, responseCtxId, setResponseCtx, setResponseCtxId }}>
      {children}
    </ValueContext.Provider>
  );
};

export const useContextValues = () => {
  const context = useContext(ValueContext);                   
  if (!context) throw new Error('Context values must be used within a ValueProvider');
  return context;
};
