import "@/public/globals.css"
import { ReactNode } from 'react';                                        
import ValueProvider from '@/lib/response-context';
import GraphContextProvider from '@/lib/graph-context';
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

const Layout = ({ children }: { children: ReactNode }) => {
  return (
    <html>
      <body>
      <div className={`${inter.variable} font-sans`}>
        <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[linear-gradient(to_right,#f0f0f0_1px,transparent_1px),linear-gradient(to_bottom,#f0f0f0_1px,transparent_1px)] bg-[size:6rem_4rem]"></div>
        <ValueProvider>
        <GraphContextProvider>
          {children}
        </GraphContextProvider>
        </ValueProvider>
        </div>
      </body>
    </html>
  );
};

export default Layout;     
