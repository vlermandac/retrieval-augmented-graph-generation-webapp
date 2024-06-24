import React from 'react'
import Layout from '@/lib/layout'
import Router from '@/lib/router'
import ReactDOM from "react-dom/client";
import ValueProvider from '@/lib/response-context';
import IndexProvider from '@/lib/current-index-context';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Layout>
      <ValueProvider>
        <IndexProvider>
        <Router />
        </IndexProvider>
      </ValueProvider>
    </Layout>
  </React.StrictMode>,
)
