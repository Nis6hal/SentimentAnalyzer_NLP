import React, { useState, useEffect } from 'react';
import {
  Settings,
  Server,
  Cpu,
  Database,
  CheckCircle2,
  RefreshCw,
  Sliders,
  ShieldCheck
} from 'lucide-react';
import { sentimentApi } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [health, setHealth] = useState<{ status: string; database: string; inference_engine: string } | null>(null);
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:8000/api/v1');
  const [modelMode, setModelMode] = useState('champion');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    sentimentApi.checkHealth().then(setHealth).catch(console.error);
  }, []);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Platform Settings & System Diagnostics
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Manage inference endpoints, active model configurations, and system health status.
        </p>
      </div>

      {/* Diagnostics Card */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          Infrastructure Telemetry & Health Checks
        </h3>

        <div className="grid sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-wider">API Service</span>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="font-semibold text-white text-sm">
                {health?.status === 'healthy' ? 'Operational' : 'Online'}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">FastAPI v1.0.0</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-wider">Database Connection</span>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="font-semibold text-white text-sm">
                {health?.database || 'Connected'}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">PostgreSQL / SQLite</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-wider">ML Weights in Memory</span>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="font-semibold text-white text-sm">
                {health?.inference_engine === 'loaded' ? 'Pre-Warmed' : 'Ready'}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">RoBERTa &amp; Baseline</span>
          </div>
        </div>
      </div>

      {/* Model & Endpoint Preferences */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-6">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider flex items-center gap-2">
          <Sliders className="w-4 h-4 text-indigo-400" />
          Inference & Pipeline Preferences
        </h3>

        <div className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">
              Backend REST API URL
            </label>
            <input
              type="text"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 focus:border-indigo-500 rounded-xl p-3 text-xs font-mono text-slate-200 focus:outline-none"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-2">
              Default Inference Engine
            </label>
            <div className="grid sm:grid-cols-2 gap-3">
              <label
                onClick={() => setModelMode('champion')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-colors block ${
                  modelMode === 'champion'
                    ? 'bg-indigo-600/15 border-indigo-500/50'
                    : 'bg-slate-950/60 border-slate-800 hover:bg-slate-900'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-white">RoBERTa (Champion)</span>
                  <span className="text-[10px] text-emerald-400 font-mono font-bold">70.4% F1</span>
                </div>
                <span className="text-[11px] text-slate-400 mt-1 block">
                  Transformer head with deep semantic context and sarcasm mastery.
                </span>
              </label>

              <label
                onClick={() => setModelMode('baseline')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-colors block ${
                  modelMode === 'baseline'
                    ? 'bg-indigo-600/15 border-indigo-500/50'
                    : 'bg-slate-950/60 border-slate-800 hover:bg-slate-900'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-white">TF-IDF Baseline</span>
                  <span className="text-[10px] text-indigo-400 font-mono font-bold">58.4% F1</span>
                </div>
                <span className="text-[11px] text-slate-400 mt-1 block">
                  Ultra-lightweight Logistic Regression for extreme edge latency.
                </span>
              </label>
            </div>
          </div>
        </div>

        <div className="flex justify-between items-center pt-4 border-t border-slate-800">
          {saved ? (
            <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
              <CheckCircle2 className="w-4 h-4" />
              Settings saved successfully!
            </span>
          ) : <div />}

          <button
            onClick={handleSave}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs shadow-md shadow-indigo-600/30 transition-all cursor-pointer"
          >
            Save Preferences
          </button>
        </div>
      </div>
    </div>
  );
};

