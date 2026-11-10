import React, { useEffect, useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Activity,
  Cpu,
  Clock,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Sparkles
} from 'lucide-react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  AreaChart,
  Area,
  XAxis,
  YAxis
} from 'recharts';
import { sentimentApi } from '../services/api';
import type { AnalyticsResponse, ModelInfoResponse } from '../types/sentiment';
import { SentimentBadge } from '../components/SentimentBadge';
import type { PageId } from '../components/Navbar';

interface DashboardPageProps {
  onNavigate: (page: PageId) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ onNavigate }) => {
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfoResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [analyticsData, modelData] = await Promise.all([
        sentimentApi.getAnalytics(),
        sentimentApi.getModelInfo(),
      ]);
      setAnalytics(analyticsData);
      setModelInfo(modelData);
    } catch (err) {
      console.error('Failed to load dashboard data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading || !analytics) {
    return (
      <div className="py-24 text-center space-y-3">
        <Activity className="w-8 h-8 text-indigo-400 animate-spin mx-auto" />
        <p className="text-slate-400 text-sm">Aggregating live sentiment telemetry...</p>
      </div>
    );
  }

  const pieData = [
    { name: 'Positive', value: analytics.summary.positive, color: '#10b981' },
    { name: 'Neutral', value: analytics.summary.neutral, color: '#06b6d4' },
    { name: 'Negative', value: analytics.summary.negative, color: '#f43f5e' },
  ].filter(d => d.value > 0);

  return (
    <div className="max-w-7xl mx-auto space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Executive Intelligence Dashboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time sentiment telemetry, class distributions, and active transformer health.
          </p>
        </div>

        <button
          onClick={fetchDashboardData}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Refresh Metrics
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-lg">
          <div className="flex justify-between items-start text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">Total Records</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-white mt-2 font-mono">
            {analytics.summary.total.toLocaleString()}
          </div>
          <span className="text-[11px] text-slate-500 mt-1 block">Indexed in persistent store</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-lg">
          <div className="flex justify-between items-start text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">Avg Confidence</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-emerald-400 mt-2 font-mono">
            {(analytics.average_confidence * 100).toFixed(1)}%
          </div>
          <span className="text-[11px] text-slate-500 mt-1 block">Calibrated softmax score</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-lg">
          <div className="flex justify-between items-start text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">Avg Latency</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-cyan-400 mt-2 font-mono">
            {analytics.average_latency_ms} <span className="text-xs font-sans text-slate-400">ms</span>
          </div>
          <span className="text-[11px] text-slate-500 mt-1 block">End-to-end inference speed</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-lg">
          <div className="flex justify-between items-start text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">Active Architecture</span>
            <Cpu className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-lg font-bold text-white mt-2 truncate font-mono">
            {modelInfo?.model_type === 'champion' ? 'RoBERTa' : 'TF-IDF LogReg'}
          </div>
          <span className="text-[11px] text-emerald-400 mt-1 block">
            Macro F1: {modelInfo?.benchmark.test_macro_f1.toFixed(3) || '0.704'}
          </span>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Sentiment Distribution Donut Chart */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
            Sentiment Class Distribution
          </h3>

          <div className="h-56 relative flex items-center justify-center">
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#334155',
                      borderRadius: '0.75rem',
                      fontSize: '12px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-xs text-slate-500">No predictions recorded yet</div>
            )}
          </div>

          <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center">
            <div className="p-2 rounded-lg bg-emerald-950/20 border border-emerald-900/30">
              <span className="text-[10px] text-slate-400 block">Positive</span>
              <span className="text-xs font-bold text-emerald-400 font-mono">
                {analytics.percentages.positive}%
              </span>
            </div>
            <div className="p-2 rounded-lg bg-cyan-950/20 border border-cyan-900/30">
              <span className="text-[10px] text-slate-400 block">Neutral</span>
              <span className="text-xs font-bold text-cyan-400 font-mono">
                {analytics.percentages.neutral}%
              </span>
            </div>
            <div className="p-2 rounded-lg bg-rose-950/20 border border-rose-900/30">
              <span className="text-[10px] text-slate-400 block">Negative</span>
              <span className="text-xs font-bold text-rose-400 font-mono">
                {analytics.percentages.negative}%
              </span>
            </div>
          </div>
        </div>

        {/* Activity Stream */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
                Live Analysis Stream
              </h3>
              <button
                onClick={() => onNavigate('history')}
                className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
              >
                View Full Audit History →
              </button>
            </div>

            <div className="space-y-2.5">
              {analytics.recent_activity.length > 0 ? (
                analytics.recent_activity.slice(0, 5).map((item) => (
                  <div
                    key={item.id}
                    className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between gap-3 text-xs"
                  >
                    <div className="max-w-md truncate text-slate-300">
                      "{item.text_preview}"
                    </div>
                    <div className="flex items-center gap-3 flex-shrink-0">
                      <SentimentBadge sentiment={item.sentiment} size="sm" />
                      <span className="font-mono text-slate-400 text-[11px]">
                        {(item.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-10 text-xs text-slate-500">
                  No records yet. Launch the analyzer to process your first sentence!
                </div>
              )}
            </div>
          </div>

          <div className="p-3 rounded-xl bg-indigo-950/20 border border-indigo-900/30 flex items-center justify-between text-xs mt-4">
            <span className="text-indigo-300">
              Need to evaluate thousands of rows from customer feedback surveys?
            </span>
            <button
              onClick={() => onNavigate('batch')}
              className="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs transition-colors"
            >
              Run Batch Analysis
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

