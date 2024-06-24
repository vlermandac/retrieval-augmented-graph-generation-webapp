import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from '@/app/page';
import ResponsePage from '@/app/response/page'
import Login from '@/app/login/page'

function Router() {                                                          
  return (                                                                
    <BrowserRouter>                                                       
      <Routes>                                                            
        <Route path="/" element={<Login />} />
        <Route path="/search" element={<HomePage />} />                    
        <Route path="/response" element={<ResponsePage />} />             
        <Route path="/login" element={<Login />} />
      </Routes>                                                           
    </BrowserRouter>                                                      
  );                                                                      
}                                                                         
                                                                          
export default Router; 
