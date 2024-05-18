import React, { createContext, useContext, useState } from 'react';

interface ValueProviderProps {
  children: React.ReactNode;
}
                                                                              
interface ValueContextType {
  responseCtx: string;
  setResponseCtx: (responseCtx: string) => void; 
}                                                                         
                                                                         
const ValueContext = createContext<ValueContextType | undefined>(undefined);

export default function ValueProvider({ children }: ValueProviderProps) {

  const [responseCtx, setResponseCtx] = useState('');
                                                                          
  return (                                                                
    <ValueContext.Provider value={{ responseCtx, setResponseCtx }}>
      {children}
    </ValueContext.Provider>
  );
};

export const useResponseCtx = () => {
  const context = useContext(ValueContext);                   
  if (!context) {                                            
    throw new Error('useResponseCtx must be used within a ValueProvider');
  }
  return context;
};

