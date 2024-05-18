import React from 'react'
import Layout from '@/lib/layout'
import Router from '@/lib/router'
import ReactDOM from "react-dom/client";
import ValueProvider from '@/lib/response-context';
import GraphContextProvider from '@/lib/graph-context';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Layout>
      <ValueProvider>
      <GraphContextProvider>
        <Router />
      </GraphContextProvider>
      </ValueProvider>
    </Layout>
  </React.StrictMode>,
)
