import React, { createContext, useContext, useState } from 'react';

interface GraphCtxProviderProps {
  children: React.ReactNode;
}
                                                                              
interface ValueContextType {                                              
  graphCtx: number[];                                                          
  setGraphCtx: (graphCtx: number[]) => void;                                      
}                                                                         
                                                                         
const ValueContext = createContext<ValueContextType | undefined>(undefined);
                                                                          
export default function GraphContextProvider({ children }: GraphCtxProviderProps) {

  const [graphCtx, setGraphCtx] = useState<number[]>([]);
                                                                          
  return (                                                                
    <ValueContext.Provider value={{ graphCtx, setGraphCtx }}>                   
      {children}                                                          
    </ValueContext.Provider>                                              
  );                                                                      
};

export const useGraphCtx = () => {
  const context = useContext(ValueContext);                   
  if (!context) {                                            
    throw new Error('useGraphCtx must be used within a GraphContextProvider');
  }
  return context;
};

