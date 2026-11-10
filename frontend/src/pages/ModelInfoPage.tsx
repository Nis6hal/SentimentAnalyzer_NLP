import React, { useEffect, useState } from 'react';
import {
  Cpu,
  CheckCircle2,
  XCircle,
  Award,
  Layers,
  Zap,
  ShieldAlert,
  GitBranch,
  BookOpen
} from 'lucide-react';
import { sentimentApi } from '../services/api';
import type { ModelInfoResponse } from '../types/sentiment';

export const ModelInfoPage: React.FC = () => {
  const [modelInfo, setModelInfo] = useState<ModelInfoResponse | null>(null);

  useEffect(() => {
    sentimentApi.getModelInfo().then(setModelInfo).catch(console.error);
  }, []);

  const challengeCases = [
    {
      id: 'neg_01',
      category: 'Negation Inversion',
      text: 'The movie was not bad at all, in fact I thoroughly enjoyed the plot twist.',
      truth: 'POSITIVE',
      basePred: 'NEGATIVE ❌',
      robertaPred: 'POSITIVE ✅ (96.4%)'
    },
    {
      id: 'sarc_01',
      category: 'Sarcasm / Irony',
      text: 'Oh fantastic, another software crash right before saving my thesis presentation.',
      truth: 'NEGATIVE',
      basePred: 'POSITIVE ❌ (Keyword bias)',
      robertaPred: 'NEGATIVE ✅ (89.1%)'
    },
    {
      id: 'neg_03',
      category: 'Subtle Negation',
      text: 'The hotel was by no means luxurious, but it was clean and centrally located.',
      truth: 'NEUTRAL',
      basePred: 'NEGATIVE ❌',
      robertaPred: 'NEUTRAL ✅ (82.7%)'
    },
    {
      id: 'info_01',
      category: 'Informal Slang',
      text: 'Bro this new track is straight heat, totally blew my mind!',
      truth: 'POSITIVE',
      basePred: 'POSITIVE ✅',
      robertaPred: 'POSITIVE ✅ (98.2%)'
    },
    {
      id: 'info_02',
      category: 'Informal Slang',
      text: 'Ngl the food was mid and the wait time was ridiculous.',
      truth: 'NEGATIVE',
      basePred: 'POSITIVE ❌',
      robertaPred: 'NEGATIVE ✅ (91.5%)'
    },
    {
      id: 'neu_01',
      category: 'Neutral Fact',
      text: 'The package arrived at 2:15 PM and was signed by reception.',
      truth: 'NEUTRAL',
      basePred: 'NEUTRAL ✅',
      robertaPred: 'NEUTRAL ✅ (94.0%)'
    }
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8 py-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Model Intelligence & Empirical Benchmarks
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Rigorous evaluation metrics comparing Champion RoBERTa against Baseline TF-IDF on held-out test splits.
        </p>
      </div>

      {/* Model Spec Hero */}
      <div className="p-6 sm:p-8 rounded-2xl bg-gradient-to-r from-indigo-950/40 via-slate-900 to-slate-900 border border-indigo-900/40 shadow-xl space-y-4">
        <div className="flex flex-wrap justify-between items-start gap-4">
          <div>
            <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
              <Award className="w-4 h-4" />
              Designated Champion Model
            </span>
            <h2 className="text-2xl font-bold text-white mt-1">
              CardiffNLP RoBERTa-Sentiment-Latest
            </h2>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              12-layer bidirectional RoBERTa transformer fine-tuned on multi-domain conversational corpora and evaluated on TweetEval 3-class.
            </p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-right">
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Primary Metric</span>
            <span className="text-2xl font-extrabold text-indigo-400 font-mono">0.7043</span>
            <span className="text-xs text-slate-400 block">Macro F1 Score</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-800/80 text-xs">
          <div>
            <span className="text-slate-500 block text-[11px]">Checkpoint</span>
            <span className="font-mono text-slate-200">twitter-roberta-base</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Inference Backend</span>
            <span className="font-mono text-slate-200">PyTorch 2.x (CPU/GPU)</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Classification Head</span>
            <span className="font-mono text-slate-200">Dense Linear (3-logits)</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Max Seq Length</span>
            <span className="font-mono text-slate-200">256 tokens</span>
          </div>
        </div>
      </div>

      {/* Benchmark Matrix Table */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <Layers className="w-4 h-4 text-indigo-400" />
          Empirical Test Set Benchmark Matrix (TweetEval Held-Out Test Set)
        </h3>

        <div className="overflow-x-auto rounded-xl border border-slate-800">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 uppercase font-mono tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-3.5">Evaluation Metric</th>
                <th className="p-3.5">Model A: Logistic Regression</th>
                <th className="p-3.5">Model C: RoBERTa (Champion)</th>
                <th className="p-3.5">Delta Advantage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              <tr className="hover:bg-slate-800/30">
                <td className="p-3.5 font-semibold text-slate-200">Macro F1-Score (Primary Metric)</td>
                <td className="p-3.5 font-mono text-slate-400">0.5837</td>
                <td className="p-3.5 font-mono font-bold text-indigo-400">0.7043</td>
                <td className="p-3.5 font-mono text-emerald-400">+12.06% (RoBERTa)</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="p-3.5 font-semibold text-slate-200">Overall Accuracy</td>
                <td className="p-3.5 font-mono text-slate-400">0.5868</td>
                <td className="p-3.5 font-mono font-bold text-slate-200">0.6990</td>
                <td className="p-3.5 font-mono text-emerald-400">+11.22%</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="p-3.5 font-semibold text-slate-200">Weighted F1-Score</td>
                <td className="p-3.5 font-mono text-slate-400">0.5865</td>
                <td className="p-3.5 font-mono font-bold text-slate-200">0.6985</td>
                <td className="p-3.5 font-mono text-emerald-400">+11.20%</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="p-3.5 font-semibold text-slate-200">F1 Negative (Minority Class)</td>
                <td className="p-3.5 font-mono text-slate-400">0.5998</td>
                <td className="p-3.5 font-mono font-bold text-rose-400">0.7009</td>
                <td className="p-3.5 font-mono text-emerald-400">+10.11%</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="p-3.5 font-semibold text-slate-200">F1 Neutral</td>
                <td className="p-3.5 font-mono text-slate-400">0.5860</td>
                <td className="p-3.5 font-mono font-bold text-cyan-400">0.6861</td>
                <td className="p-3.5 font-mono text-emerald-400">+10.02%</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="p-3.5 font-semibold text-slate-200">F1 Positive</td>
                <td className="p-3.5 font-mono text-slate-400">0.5655</td>
                <td className="p-3.5 font-mono font-bold text-emerald-400">0.7259</td>
                <td className="p-3.5 font-mono text-emerald-400">+16.04%</td>
              </tr>
              <tr className="hover:bg-slate-800/30 bg-indigo-950/20">
                <td className="p-3.5 font-semibold text-white">Challenge Evaluation Suite (16 Cases)</td>
                <td className="p-3.5 font-mono text-rose-400">37.5% (6/16)</td>
                <td className="p-3.5 font-mono font-bold text-emerald-400">75.0% (12/16)</td>
                <td className="p-3.5 font-mono text-emerald-400 font-bold">+37.5% (2x accuracy)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Challenge Suite Showcase */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <Zap className="w-4 h-4 text-emerald-400" />
          Challenge Suite Breakdown (Sarcasm, Negation & Slang)
        </h3>

        <div className="space-y-3">
          {challengeCases.map((c) => (
            <div
              key={c.id}
              className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-2 text-xs"
            >
              <div className="flex justify-between items-center text-slate-400">
                <span className="font-mono text-indigo-400 font-semibold">{c.category}</span>
                <span className="font-mono text-slate-500">Truth: <strong className="text-white">{c.truth}</strong></span>
              </div>
              <p className="text-slate-200 italic font-serif">"{c.text}"</p>
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="p-2 rounded bg-slate-900 border border-slate-800 text-[11px]">
                  <span className="text-slate-400 block">Baseline TF-IDF:</span>
                  <span className="font-medium text-slate-300">{c.basePred}</span>
                </div>
                <div className="p-2 rounded bg-indigo-950/30 border border-indigo-900/40 text-[11px]">
                  <span className="text-slate-400 block">Champion RoBERTa:</span>
                  <span className="font-medium text-emerald-400">{c.robertaPred}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

