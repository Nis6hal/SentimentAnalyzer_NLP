import React, { useState } from 'react';
import {
  Upload,
  FileSpreadsheet,
  Download,
  Loader2,
  AlertCircle,
  CheckCircle2,
  Layers,
  FileText
} from 'lucide-react';
import { sentimentApi } from '../services/api';
import type { SentimentResult } from '../types/sentiment';
import { SentimentBadge } from '../components/SentimentBadge';

export const BatchAnalyzerPage: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<Array<{ text: string; result: SentimentResult }>>([]);
  const [avgLatency, setAvgLatency] = useState<number | null>(null);

  const sampleCSV = `text
"The hotel breakfast was delicious and the staff was courteous."
"Flight was canceled without compensation, dreadful experience."
"The conference will start promptly at 9:00 AM in Hall B."
"The software is okay, but lacks advanced export features."
"Outstanding battery longevity, lasted over 36 hours continuous use."`;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      if (content) {
        setInputText(content);
        setError(null);
      }
    };
    reader.readAsText(file);
  };

  const parseLines = (raw: string): string[] => {
    // If it's a CSV with quotes or standard lines
    const lines = raw.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
    // If first line is header "text" or "review", drop it
    if (lines.length > 0 && /^(text|sentence|review|comment)/i.test(lines[0])) {
      lines.shift();
    }
    // Clean quotes
    return lines.map(line => line.replace(/^"|"$/g, '').trim()).filter(l => l.length > 0);
  };

  const handleRunBatch = async () => {
    const texts = parseLines(inputText);
    if (texts.length === 0) {
      setError('Please provide at least one sentence or CSV row to analyze.');
      return;
    }
    if (texts.length > 500) {
      setError(`Batch size exceeds 500 lines (got ${texts.length}). Please reduce input.`);
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const res = await sentimentApi.analyzeBatch(texts);
      const combined = texts.map((t, idx) => ({
        text: t,
        result: res.results[idx]
      }));
      setResults(combined);
      setAvgLatency(res.average_latency_ms);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to process batch.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    if (results.length === 0) return;
    const headers = ['Text', 'Sentiment', 'Confidence', 'Negative_Prob', 'Neutral_Prob', 'Positive_Prob', 'Model_ID'];
    const rows = results.map(r => [
      `"${r.text.replace(/"/g, '""')}"`,
      r.result.sentiment,
      r.result.confidence,
      r.result.probabilities.negative,
      r.result.probabilities.neutral,
      r.result.probabilities.positive,
      r.result.model_id
    ]);

    const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `sentimentiq_batch_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 py-6">
      {/* Page Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Batch Sentiment Processor
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Upload bulk CSV datasets or paste multiple text reviews to process hundreds of inputs simultaneously.
        </p>
      </div>

      {/* Upload and Input Section */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
          <div className="flex justify-between items-center">
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
              Input Text or CSV Rows (One per line)
            </label>
            <button
              onClick={() => setInputText(sampleCSV)}
              className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
            >
              Load Sample Data
            </button>
          </div>

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={8}
            placeholder="Paste multiple sentences or CSV contents here..."
            className="w-full bg-slate-950/80 border border-slate-800 focus:border-indigo-500 rounded-xl p-4 text-xs font-mono text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all resize-y"
          />

          {error && (
            <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-950/40 border border-rose-900/50 text-rose-300 text-xs">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div className="flex flex-wrap justify-between items-center gap-4 pt-2 border-t border-slate-800">
            <span className="text-xs text-slate-400 font-mono">
              Lines detected: {parseLines(inputText).length}
            </span>

            <button
              onClick={handleRunBatch}
              disabled={loading || !inputText.trim()}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-medium text-xs shadow-md shadow-indigo-600/30 transition-all cursor-pointer disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Processing Vectorized Batch...
                </>
              ) : (
                <>
                  <Layers className="w-4 h-4" />
                  Process Batch ({parseLines(inputText).length} items)
                </>
              )}
            </button>
          </div>
        </div>

        {/* File Dropzone Card */}
        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
              <FileSpreadsheet className="w-4 h-4 text-indigo-400" />
              CSV Upload
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Upload a UTF-8 encoded .csv or .txt file containing a column of customer reviews or sentences.
            </p>
          </div>

          <label className="border-2 border-dashed border-slate-700 hover:border-indigo-500 rounded-xl p-6 text-center cursor-pointer transition-colors block group">
            <input
              type="file"
              accept=".csv,.txt"
              onChange={handleFileUpload}
              className="hidden"
            />
            <Upload className="w-8 h-8 text-slate-500 group-hover:text-indigo-400 mx-auto mb-2 transition-colors" />
            <span className="text-xs font-medium text-slate-300 block">
              Click to browse or drop CSV
            </span>
            <span className="text-[11px] text-slate-500 block mt-1">
              Supports up to 500 rows per batch
            </span>
          </label>

          <div className="text-[11px] text-slate-500 space-y-1">
            <div>• Header row is automatically detected</div>
            <div>• All records saved to persistent DB</div>
          </div>
        </div>
      </div>

      {/* Batch Results Table */}
      {results.length > 0 && (
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
          <div className="flex flex-wrap justify-between items-center gap-4">
            <div>
              <h3 className="text-base font-semibold text-white">
                Batch Results ({results.length} processed)
              </h3>
              {avgLatency !== null && (
                <span className="text-xs text-emerald-400 font-mono">
                  Average inference time: {avgLatency} ms/item
                </span>
              )}
            </div>

            <button
              onClick={handleExportCSV}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition-colors cursor-pointer"
            >
              <Download className="w-4 h-4 text-indigo-400" />
              Download Annotated CSV
            </button>
          </div>

          <div className="overflow-x-auto rounded-xl border border-slate-800">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 uppercase font-mono tracking-wider border-b border-slate-800">
                <tr>
                  <th className="p-3 w-12">#</th>
                  <th className="p-3">Text Sample</th>
                  <th className="p-3 w-32">Sentiment</th>
                  <th className="p-3 w-24">Confidence</th>
                  <th className="p-3 w-48">Probabilities (Neg / Neu / Pos)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {results.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-3 text-slate-500 font-mono">{idx + 1}</td>
                    <td className="p-3 text-slate-200 max-w-md truncate" title={row.text}>
                      {row.text}
                    </td>
                    <td className="p-3">
                      <SentimentBadge sentiment={row.result.sentiment} size="sm" />
                    </td>
                    <td className="p-3 font-mono font-medium text-slate-300">
                      {(row.result.confidence * 100).toFixed(1)}%
                    </td>
                    <td className="p-3 font-mono text-[11px] text-slate-400">
                      <span className="text-rose-400">{(row.result.probabilities.negative * 100).toFixed(0)}%</span> /{' '}
                      <span className="text-cyan-400">{(row.result.probabilities.neutral * 100).toFixed(0)}%</span> /{' '}
                      <span className="text-emerald-400">{(row.result.probabilities.positive * 100).toFixed(0)}%</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

