import React, { useState } from 'react';
import {
  FileCode2,
  Copy,
  Check,
  ExternalLink,
  Layers,
  Send,
  Database
} from 'lucide-react';

export const ApiDocsPage: React.FC = () => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const endpoints = [
    {
      method: 'POST',
      path: '/api/v1/analyze',
      title: 'Analyze Single Text',
      desc: 'Performs calibrated sentiment prediction on a single sentence with class probabilities.',
      curl: `curl -X POST http://localhost:8000/api/v1/analyze \\
  -H "Content-Type: application/json" \\
  -d '{"text": "The customer support team resolved my query in 5 minutes!"}'`,
      response: `{
  "success": true,
  "result": {
    "sentiment": "POSITIVE",
    "confidence": 0.9821,
    "probabilities": {
      "positive": 0.9821,
      "negative": 0.0054,
      "neutral": 0.0125
    },
    "model_version": "1.0.0",
    "model_id": "roberta-sentiment-v1.0",
    "latency_ms": 14.8
  }
}`
    },
    {
      method: 'POST',
      path: '/api/v1/analyze/batch',
      title: 'Analyze Batch',
      desc: 'Vectorized high-throughput batch processing for up to 500 sentences.',
      curl: `curl -X POST http://localhost:8000/api/v1/analyze/batch \\
  -H "Content-Type: application/json" \\
  -d '{"texts": ["Great experience", "Broken product", "Meeting at 3 PM"]}'`,
      response: `{
  "success": true,
  "results": [
    { "sentiment": "POSITIVE", "confidence": 0.9712, ... },
    { "sentiment": "NEGATIVE", "confidence": 0.9654, ... },
    { "sentiment": "NEUTRAL",  "confidence": 0.9231, ... }
  ],
  "total_processed": 3,
  "average_latency_ms": 6.2
}`
    },
    {
      method: 'GET',
      path: '/api/v1/analytics',
      title: 'Aggregate Analytics',
      desc: 'Returns overall sentiment distribution, percentages, and historical timelines.',
      curl: `curl http://localhost:8000/api/v1/analytics`,
      response: `{
  "success": true,
  "summary": { "positive": 142, "negative": 48, "neutral": 86, "total": 276 },
  "percentages": { "positive": 51.4, "negative": 17.4, "neutral": 31.2 },
  "average_confidence": 0.8924,
  "average_latency_ms": 12.4
}`
    },
    {
      method: 'GET',
      path: '/api/v1/model/info',
      title: 'Model Metadata & Benchmarks',
      desc: 'Exposes active model architecture, checkpoint name, and empirical test scores.',
      curl: `curl http://localhost:8000/api/v1/model/info`,
      response: `{
  "success": true,
  "model_id": "roberta-sentiment-v1.0",
  "model_type": "champion",
  "classes": ["NEGATIVE", "NEUTRAL", "POSITIVE"],
  "benchmark": {
    "test_macro_f1": 0.7043,
    "test_accuracy": 0.6990,
    "challenge_suite_accuracy": 0.7500
  }
}`
    }
  ];

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            REST API Reference
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Complete programmatic integration specifications with OpenAPI schemas and live cURL snippets.
          </p>
        </div>

        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 text-xs font-medium hover:bg-indigo-600/30 transition-colors"
        >
          <ExternalLink className="w-3.5 h-3.5" />
          Interactive Swagger UI (/docs)
        </a>
      </div>

      {/* Endpoints List */}
      <div className="space-y-6">
        {endpoints.map((ep, idx) => (
          <div
            key={idx}
            className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4"
          >
            <div className="flex flex-wrap justify-between items-start gap-4 pb-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <span
                  className={`px-2.5 py-1 rounded-md font-mono text-xs font-bold ${
                    ep.method === 'POST'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30'
                  }`}
                >
                  {ep.method}
                </span>
                <span className="font-mono text-sm font-semibold text-white">
                  {ep.path}
                </span>
              </div>
              <span className="text-xs text-slate-400">{ep.title}</span>
            </div>

            <p className="text-xs text-slate-300">{ep.desc}</p>

            {/* Code Snippets */}
            <div className="space-y-3">
              <div>
                <div className="flex justify-between items-center text-[11px] text-slate-400 font-mono mb-1.5">
                  <span>Example Request (cURL)</span>
                  <button
                    onClick={() => handleCopy(ep.curl, idx)}
                    className="flex items-center gap-1 hover:text-white transition-colors cursor-pointer"
                  >
                    {copiedIndex === idx ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-400" />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        Copy
                      </>
                    )}
                  </button>
                </div>
                <pre className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-200 overflow-x-auto">
                  {ep.curl}
                </pre>
              </div>

              <div>
                <div className="text-[11px] text-slate-400 font-mono mb-1.5">
                  Example Response (JSON)
                </div>
                <pre className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-indigo-300 overflow-x-auto">
                  {ep.response}
                </pre>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

