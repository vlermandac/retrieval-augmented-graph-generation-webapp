import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from '@/app/page';
import ResponsePage from '@/app/response/page'
                                                                          
function Router() {                                                          
  return (                                                                
    <BrowserRouter>                                                       
      <Routes>                                                            
        <Route path="/" element={<HomePage />} />                    
        <Route path="/response" element={<ResponsePage />} />             
        <Route path="/search" element={<HomePage />} />                    
      </Routes>                                                           
    </BrowserRouter>                                                      
  );                                                                      
}                                                                         
                                                                          
export default Router; 
