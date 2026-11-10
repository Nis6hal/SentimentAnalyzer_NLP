import React, { useState } from 'react';
import {
  Sparkles,
  Send,
  Loader2,
  ThumbsUp,
  ThumbsDown,
  RotateCcw,
  Check,
  AlertCircle,
  HelpCircle,
  Clock,
  Cpu
} from 'lucide-react';
import { sentimentApi } from '../services/api';
import type { SentimentResult } from '../types/sentiment';
import { SentimentBadge } from '../components/SentimentBadge';
import { ProbabilityBar } from '../components/ProbabilityBar';

export const SentimentAnalyzerPage: React.FC = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  const presets = [
    {
      label: 'Enthusiastic Praise',
      text: 'The new update transformed our entire workflow! Absolutely stellar performance and design.'
    },
    {
      label: 'Sarcasm / Irony',
      text: 'Oh fantastic, another unexpected flight delay right before my client meeting. Just what I needed.'
    },
    {
      label: 'Subtle Negation',
      text: 'The battery life was by no means disappointing, in fact it lasted through two full workdays.'
    },
    {
      label: 'Neutral Fact',
      text: 'The scheduled database migration commenced at 02:00 UTC and concluded in 14 minutes.'
    }
  ];

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze.');
      return;
    }
    setError(null);
    setLoading(true);
    setFeedbackSubmitted(false);

    try {
      const res = await sentimentApi.analyzeText(text.trim());
      setResult(res.result);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to analyze text.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (isCorrect: boolean) => {
    if (!result?.id || feedbackSubmitted) return;
    try {
      await sentimentApi.submitFeedback(result.id, isCorrect);
      setFeedbackSubmitted(true);
    } catch (err) {
      console.error('Failed to submit feedback', err);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleAnalyze();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Single-Text Sentiment Analyzer
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Input English sentences, customer reviews, tweets, or feedback to compute calibrated 3-class sentiment probabilities.
        </p>
      </div>

      {/* Preset Pills */}
      <div className="space-y-2">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Quick Test Presets
        </span>
        <div className="flex flex-wrap gap-2">
          {presets.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => {
                setText(preset.text);
                setError(null);
              }}
              className="text-xs px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-700 transition-colors cursor-pointer"
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>

      {/* Input Box Card */}
      <div className="p-5 sm:p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
        <div className="relative">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={5}
            placeholder="Type or paste your text here (e.g. 'The customer support team resolved my query in 5 minutes!')..."
            className="w-full bg-slate-950/80 border border-slate-800 focus:border-indigo-500 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all font-sans resize-y"
          />

          <div className="flex justify-between items-center text-xs text-slate-500 mt-2 px-1">
            <span className="font-mono">{text.length} characters</span>
            <span className="text-[11px] hidden sm:inline text-slate-500">
              Tip: Press <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono">Ctrl + Enter</kbd> to analyze
            </span>
          </div>
        </div>

        {error && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-950/40 border border-rose-900/50 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex justify-between items-center pt-2 border-t border-slate-800/80">
          <button
            onClick={() => {
              setText('');
              setResult(null);
              setError(null);
            }}
            disabled={!text && !result}
            className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Clear
          </button>

          <button
            onClick={handleAnalyze}
            disabled={loading || !text.trim()}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-medium text-xs shadow-md shadow-indigo-600/30 transition-all cursor-pointer disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing via RoBERTa...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Run Sentiment Analysis
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-800 shadow-2xl space-y-6 animate-in fade-in duration-300">
          <div className="flex flex-wrap justify-between items-start gap-4 pb-4 border-b border-slate-800">
            <div>
              <span className="text-xs text-slate-400 font-medium">Predicted Sentiment</span>
              <div className="mt-1 flex items-center gap-3">
                <SentimentBadge sentiment={result.sentiment} size="lg" />
                <span className="text-xs font-mono text-slate-400">
                  Confidence: <strong className="text-white">{(result.confidence * 100).toFixed(1)}%</strong>
                </span>
              </div>
            </div>

            <div className="flex items-center gap-3 text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1">
                <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                {result.model_id}
              </span>
              {result.latency_ms !== undefined && (
                <span className="flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5 text-emerald-400" />
                  {result.latency_ms} ms
                </span>
              )}
            </div>
          </div>

          {/* Probability Distribution */}
          <div className="space-y-4">
            <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              Class Probability Distribution (Softmax Normalized)
            </h4>

            <div className="grid sm:grid-cols-3 gap-4">
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <ProbabilityBar
                  label="Positive Probability"
                  value={result.probabilities.positive}
                  color="emerald"
                />
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <ProbabilityBar
                  label="Neutral Probability"
                  value={result.probabilities.neutral}
                  color="cyan"
                />
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <ProbabilityBar
                  label="Negative Probability"
                  value={result.probabilities.negative}
                  color="rose"
                />
              </div>
            </div>
          </div>

          {/* Feedback & Ground Truth Loop */}
          <div className="flex flex-wrap justify-between items-center gap-4 pt-4 border-t border-slate-800/80 text-xs">
            <span className="text-slate-400">
              Was this sentiment prediction accurate?
            </span>

            {feedbackSubmitted ? (
              <span className="inline-flex items-center gap-1 text-emerald-400 font-medium">
                <Check className="w-4 h-4" />
                Thank you! Feedback recorded for model retraining.
              </span>
            ) : (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleFeedback(true)}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors cursor-pointer"
                >
                  <ThumbsUp className="w-3.5 h-3.5 text-emerald-400" />
                  Yes, Accurate
                </button>
                <button
                  onClick={() => handleFeedback(false)}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors cursor-pointer"
                >
                  <ThumbsDown className="w-3.5 h-3.5 text-rose-400" />
                  Incorrect
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

