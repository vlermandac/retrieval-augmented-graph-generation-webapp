import React, { createContext, useContext, useState } from 'react';

interface IndexProviderProps {
  children: React.ReactNode;
}

interface IndexContextType {
  currentIndex: string;
  setCurrentIndex: (currentIndex: string) => void; 
}

const IndexContext = createContext<IndexContextType | undefined>(undefined);

export default function IndexProvider({ children }: IndexProviderProps) {

  const [currentIndex, setCurrentIndex] = useState('');

  return (
    <IndexContext.Provider value={{ currentIndex, setCurrentIndex }}>
      {children}
    </IndexContext.Provider>
  );
};

export const useCurrentIndex = () => {
  const context = useContext(IndexContext);                   
  if (!context) throw new Error('Context values must be used within a IndexProvider');
  return context;
};
