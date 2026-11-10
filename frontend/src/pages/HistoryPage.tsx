import React, { useEffect, useState } from 'react';
import {
  History,
  Filter,
  ChevronLeft,
  ChevronRight,
  Clock,
  Eye,
  RotateCcw,
  Activity,
  X
} from 'lucide-react';
import { sentimentApi } from '../services/api';
import type { HistoryItem } from '../types/sentiment';
import { SentimentBadge } from '../components/SentimentBadge';

export const HistoryPage: React.FC = () => {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(15);
  const [sentimentFilter, setSentimentFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await sentimentApi.getHistory(page, pageSize, sentimentFilter);
      setItems(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to load history', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [page, sentimentFilter]);

  const totalPages = Math.ceil(total / pageSize) || 1;

  return (
    <div className="max-w-7xl mx-auto space-y-6 py-6">
      {/* Header */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Analysis Audit History
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Complete indexed record of all single and batched sentiment classifications with probability distributions.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2">
          {['ALL', 'POSITIVE', 'NEUTRAL', 'NEGATIVE'].map((tab) => (
            <button
              key={tab}
              onClick={() => {
                setSentimentFilter(tab);
                setPage(1);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                sentimentFilter === tab
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {tab}
            </button>
          ))}
          <button
            onClick={fetchHistory}
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
            title="Refresh"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* History Table */}
      <div className="rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl overflow-hidden">
        {loading ? (
          <div className="py-20 text-center space-y-2">
            <Activity className="w-7 h-7 text-indigo-400 animate-spin mx-auto" />
            <p className="text-xs text-slate-400">Loading audit log...</p>
          </div>
        ) : items.length === 0 ? (
          <div className="py-20 text-center space-y-2">
            <History className="w-8 h-8 text-slate-600 mx-auto" />
            <p className="text-sm text-slate-400">No records found matching criteria.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 uppercase font-mono tracking-wider border-b border-slate-800">
                <tr>
                  <th className="p-3.5 w-16">ID</th>
                  <th className="p-3.5">Text Sample</th>
                  <th className="p-3.5 w-32">Sentiment</th>
                  <th className="p-3.5 w-24">Confidence</th>
                  <th className="p-3.5 w-44">Probabilities (Neg / Neu / Pos)</th>
                  <th className="p-3.5 w-36">Timestamp</th>
                  <th className="p-3.5 w-20 text-center">Inspect</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {items.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-3.5 font-mono text-slate-500">#{row.id}</td>
                    <td className="p-3.5 text-slate-200 max-w-md truncate" title={row.text}>
                      {row.text_preview}
                    </td>
                    <td className="p-3.5">
                      <SentimentBadge sentiment={row.sentiment} size="sm" />
                    </td>
                    <td className="p-3.5 font-mono font-medium text-slate-200">
                      {(row.confidence * 100).toFixed(1)}%
                    </td>
                    <td className="p-3.5 font-mono text-[11px] text-slate-400">
                      <span className="text-rose-400">{(row.probabilities.negative * 100).toFixed(0)}%</span> /{' '}
                      <span className="text-cyan-400">{(row.probabilities.neutral * 100).toFixed(0)}%</span> /{' '}
                      <span className="text-emerald-400">{(row.probabilities.positive * 100).toFixed(0)}%</span>
                    </td>
                    <td className="p-3.5 text-slate-500 font-mono text-[11px]">
                      {new Date(row.created_at).toLocaleString()}
                    </td>
                    <td className="p-3.5 text-center">
                      <button
                        onClick={() => setSelectedItem(row)}
                        className="p-1 rounded-md hover:bg-slate-800 text-indigo-400 hover:text-indigo-300 transition-colors"
                        title="View Full Text & Inspection"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Bar */}
        <div className="p-4 bg-slate-950/60 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400">
          <div>
            Showing {items.length > 0 ? (page - 1) * pageSize + 1 : 0} to{' '}
            {Math.min(page * pageSize, total)} of {total} records
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page === 1}
              className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-mono text-slate-300">
              Page {page} of {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page >= totalPages}
              className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Inspect Modal */}
      {selectedItem && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 space-y-4 shadow-2xl relative">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs text-slate-500 font-mono">Record #{selectedItem.id}</span>
                <div className="flex items-center gap-2 mt-1">
                  <SentimentBadge sentiment={selectedItem.sentiment} size="md" />
                  <span className="text-xs font-mono text-slate-300">
                    Confidence: {(selectedItem.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
              <button
                onClick={() => setSelectedItem(null)}
                className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800/80 text-xs text-slate-200 leading-relaxed font-sans max-h-60 overflow-y-auto">
              {selectedItem.text}
            </div>

            <div className="grid grid-cols-3 gap-2 text-center text-xs">
              <div className="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-900/40">
                <span className="text-[10px] text-slate-400 block">Positive</span>
                <span className="font-mono font-bold text-emerald-400">
                  {(selectedItem.probabilities.positive * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-2.5 rounded-lg bg-cyan-950/30 border border-cyan-900/40">
                <span className="text-[10px] text-slate-400 block">Neutral</span>
                <span className="font-mono font-bold text-cyan-400">
                  {(selectedItem.probabilities.neutral * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-2.5 rounded-lg bg-rose-950/30 border border-rose-900/40">
                <span className="text-[10px] text-slate-400 block">Negative</span>
                <span className="font-mono font-bold text-rose-400">
                  {(selectedItem.probabilities.negative * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            <div className="text-[11px] text-slate-500 font-mono flex justify-between pt-2 border-t border-slate-800">
              <span>Model: {selectedItem.model_id}</span>
              <span>{new Date(selectedItem.created_at).toLocaleString()}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

