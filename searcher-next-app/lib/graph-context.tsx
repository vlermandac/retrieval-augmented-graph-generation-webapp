'use client';
import React, { createContext, useContext, useState } from 'react';

interface GraphProviderProps {
  children: React.ReactNode;
}
                                                                              
interface GraphContextType {                                              
  graph: number[];                                                          
  setGraph: (graph: number[]) => void;                                      
}                                                                         
                                                                         
const GraphContext = createContext<GraphContextType | undefined>(undefined);
                                                                          
export default function GraphContextProvider({ children }: GraphProviderProps) {

  const [graph, setGraph] = useState<number[]>([]);
                                                                          
  return (                                                                
    <GraphContext.Provider value={{ graph, setGraph }}>                   
      {children}                                                          
    </GraphContext.Provider>                                              
  );                                                                      
};

export const useGraphCtx = () => {
  const context = useContext(GraphContext);                   
  if (!context) {                                            
    throw new Error('useGraphCtx must be used within a ValueProvider');
  }
  return context;
};

