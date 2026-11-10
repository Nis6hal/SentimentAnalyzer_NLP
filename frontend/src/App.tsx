import React, { useState, useEffect } from 'react';
import { Navbar, type PageId } from './components/Navbar';
import { LandingPage } from './pages/LandingPage';
import { SentimentAnalyzerPage } from './pages/SentimentAnalyzerPage';
import { BatchAnalyzerPage } from './pages/BatchAnalyzerPage';
import { DashboardPage } from './pages/DashboardPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { HistoryPage } from './pages/HistoryPage';
import { ModelInfoPage } from './pages/ModelInfoPage';
import { ApiDocsPage } from './pages/ApiDocsPage';
import { SettingsPage } from './pages/SettingsPage';
import { sentimentApi } from './services/api';

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<PageId>('landing');
  const [modelId, setModelId] = useState<string>('RoBERTa-v1.0');

  useEffect(() => {
    sentimentApi.getModelInfo()
      .then((info) => {
        if (info.model_id) {
          setModelId(info.model_id);
        }
      })
      .catch((err) => {
        console.warn('Could not fetch model info on load', err);
      });
  }, []);

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage onNavigate={setCurrentPage} />;
      case 'analyzer':
        return <SentimentAnalyzerPage />;
      case 'batch':
        return <BatchAnalyzerPage />;
      case 'dashboard':
        return <DashboardPage onNavigate={setCurrentPage} />;
      case 'analytics':
        return <AnalyticsPage />;
      case 'history':
        return <HistoryPage />;
      case 'model-info':
        return <ModelInfoPage />;
      case 'api-docs':
        return <ApiDocsPage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <SentimentAnalyzerPage />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        currentPage={currentPage}
        onSelectPage={setCurrentPage}
        modelId={modelId}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
        {renderCurrentPage()}
      </main>

      <footer className="border-t border-slate-900 bg-slate-950/60 py-8 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-400">SentimentIQ</span>
            <span>—</span>
            <span>Enterprise NLP Sentiment Intelligence</span>
          </div>
          <div className="text-[11px] font-mono text-slate-600">
            PyTorch • RoBERTa • FastAPI • SQLAlchemy • React • Tailwind CSS
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

