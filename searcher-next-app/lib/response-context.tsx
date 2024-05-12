'use client';
import React, { createContext, useContext, useState } from 'react';

interface ValueProviderProps {
  children: React.ReactNode;
}
                                                                              
interface ValueContextType {                                              
  value: string;                                                          
  setValue: (value: string) => void;                                      
}                                                                         
                                                                         
const ValueContext = createContext<ValueContextType | undefined>(undefined);
                                                                          
                                                                          
export default function ValueProvider({ children }: ValueProviderProps) {

  const [value, setValue] = useState('');                                 
                                                                          
  return (                                                                
    <ValueContext.Provider value={{ value, setValue }}>                   
      {children}                                                          
    </ValueContext.Provider>                                              
  );                                                                      
};

export const useValue = () => {
  const context = useContext(ValueContext);                   
  if (!context) {                                            
    throw new Error('useValue must be used within a ValueProvider');
  }
  return context;
};

