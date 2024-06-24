import React from 'react';                                                
import { useNavigate } from 'react-router-dom';                            
import { FaHome } from 'react-icons/fa';                           
import { Settings } from '@/components/settings';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const goHome = () => {
    navigate('/search');
  };
  return (                                                              
    <header className="sticky top-0 flex z-20 justify-between items-center p-4 px-8 shadow-md">
      <div className="icon cursor-pointer transition-opacity duration-200 hover:opacity-20" onClick={goHome}>                       
        <FaHome size={33} />                                      
      </div>                                                        
      <Settings />
    </header>                                                         
  );                                                                    
};                                                                        
                                                                          
export default Header;
