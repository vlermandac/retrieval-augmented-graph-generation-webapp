import React from 'react'
import Layout from '@/lib/layout'
import Router from '@/lib/router'
import ReactDOM from "react-dom/client";
import ValueProvider from '@/lib/response-context';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Layout>
      <ValueProvider>
        <Router />
      </ValueProvider>
    </Layout>
  </React.StrictMode>,
)
