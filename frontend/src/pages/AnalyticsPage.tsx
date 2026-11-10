import React, { useEffect, useState } from 'react';
import {
  TrendingUp,
  BarChart3,
  Calendar,
  Activity,
  Layers,
  Sparkles,
  RotateCcw
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { sentimentApi } from '../services/api';
import type { AnalyticsResponse } from '../types/sentiment';

export const AnalyticsPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const data = await sentimentApi.getAnalytics();
      setAnalytics(data);
    } catch (err) {
      console.error('Failed to load analytics', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading || !analytics) {
    return (
      <div className="py-24 text-center space-y-3">
        <Activity className="w-8 h-8 text-indigo-400 animate-spin mx-auto" />
        <p className="text-slate-400 text-sm">Aggregating historical intelligence metrics...</p>
      </div>
    );
  }

  const barData = [
    { sentiment: 'Positive', count: analytics.summary.positive, fill: '#10b981' },
    { sentiment: 'Neutral', count: analytics.summary.neutral, fill: '#06b6d4' },
    { sentiment: 'Negative', count: analytics.summary.negative, fill: '#f43f5e' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Sentiment Analytics & Historical Trends
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Deep longitudinal telemetry on class trends, volume frequency, and confidence dispersion.
          </p>
        </div>

        <button
          onClick={fetchAnalytics}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Refresh
        </button>
      </div>

      {/* Main Charts */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Timeline Area Chart */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-indigo-400" />
              Temporal Sentiment Trajectory
            </h3>
            <span className="text-xs text-slate-500 font-mono">Daily grouping</span>
          </div>

          <div className="h-72">
            {analytics.timeline.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={analytics.timeline}>
                  <defs>
                    <linearGradient id="posColor" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.6}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="negColor" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.6}/>
                      <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#334155',
                      borderRadius: '0.75rem',
                      fontSize: '12px',
                    }}
                  />
                  <Legend />
                  <Area type="monotone" dataKey="positive" stroke="#10b981" fillOpacity={1} fill="url(#posColor)" />
                  <Area type="monotone" dataKey="neutral" stroke="#06b6d4" fillOpacity={0.2} fill="#06b6d4" />
                  <Area type="monotone" dataKey="negative" stroke="#f43f5e" fillOpacity={1} fill="url(#negColor)" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-500">
                Timeline data will appear as analysis records accumulate over time.
              </div>
            )}
          </div>
        </div>

        {/* Volume Breakdown Bar Chart */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-indigo-400" />
              Volume Distribution by Class
            </h3>
            <span className="text-xs text-slate-500 font-mono">Total count</span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="sentiment" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '0.75rem',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Summary Matrix Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-semibold uppercase text-slate-400 tracking-wider">
            Positivity Ratio
          </span>
          <div className="text-3xl font-extrabold text-emerald-400 font-mono mt-2">
            {analytics.percentages.positive}%
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Percentage of total evaluated corpus classified as POSITIVE.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-semibold uppercase text-slate-400 tracking-wider">
            Neutral Ratio
          </span>
          <div className="text-3xl font-extrabold text-cyan-400 font-mono mt-2">
            {analytics.percentages.neutral}%
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Objective statements, inquiries, and balanced reviews.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-semibold uppercase text-slate-400 tracking-wider">
            Negativity Ratio
          </span>
          <div className="text-3xl font-extrabold text-rose-400 font-mono mt-2">
            {analytics.percentages.negative}%
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Critical feedback, customer complaints, and dissatisfaction signals.
          </p>
        </div>
      </div>
    </div>
  );
};

