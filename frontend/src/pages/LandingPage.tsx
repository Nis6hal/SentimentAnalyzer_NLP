import React from 'react';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
  Activity,
  Cpu,
  Database,
  BarChart2,
  CheckCircle2,
  Lock
} from 'lucide-react';
import type { PageId } from '../components/Navbar';

interface LandingPageProps {
  onNavigate: (page: PageId) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate }) => {
  return (
    <div className="space-y-24 py-8">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20">
        {/* Glow ambient background */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-indigo-500/10 blur-[130px] rounded-full pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center space-y-6 relative">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-800/50 text-indigo-300 text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Next-Generation Natural Language Understanding</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
            High-Precision Sentiment Analysis for{' '}
            <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
              Modern Enterprise
            </span>
          </h1>

          <p className="text-lg text-slate-400 max-w-2xl mx-auto font-normal leading-relaxed">
            Architected from the ground up with fine-tuned CardiffNLP RoBERTa transformer checkpoints,
            robust TF-IDF baselines, async FastAPI pipelines, and real-time confidence distributions.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <button
              onClick={() => onNavigate('analyzer')}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm shadow-lg shadow-indigo-600/30 hover:shadow-indigo-600/50 transition-all cursor-pointer"
            >
              Analyze Sentiment Now
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => onNavigate('model-info')}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-medium text-sm transition-all cursor-pointer"
            >
              <Cpu className="w-4 h-4 text-indigo-400" />
              Explore Model Benchmark
            </button>
          </div>

          {/* Key Metric Badges */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-12 border-t border-slate-800/60 max-w-3xl mx-auto">
            <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-2xl font-bold font-mono text-indigo-400">70.4%</div>
              <div className="text-xs text-slate-400 mt-1">Primary Macro F1</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-2xl font-bold font-mono text-emerald-400">75.0%</div>
              <div className="text-xs text-slate-400 mt-1">Challenge Suite Score</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-2xl font-bold font-mono text-cyan-400">&lt; 25ms</div>
              <div className="text-xs text-slate-400 mt-1">Inference Latency</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-2xl font-bold font-mono text-purple-400">3-Class</div>
              <div className="text-xs text-slate-400 mt-1">Pos / Neg / Neutral</div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center space-y-3 mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Engineered for Production Rigor
          </h2>
          <p className="text-slate-400 text-sm max-w-xl mx-auto">
            No mockups or external APIs. Every prediction runs against fine-tuned weights with full probability distribution.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40 transition-colors">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-4 text-indigo-400">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Dual-Tier ML Engine</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              State-of-the-art RoBERTa champion model for nuanced context, paired with a Scikit-Learn TF-IDF baseline for ultra-fast fallback.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-purple-500/40 transition-colors">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-4 text-purple-400">
              <Activity className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">High-Throughput Batch Processing</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Upload multi-thousand sentence CSVs or JSON payloads. Tensor-accelerated vectorization processes hundreds of reviews in seconds.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-emerald-500/40 transition-colors">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-4 text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Audited Historical Intelligence</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Every inference record, probability distribution, and user feedback signal is persisted with timestamps in PostgreSQL / SQLite.
            </p>
          </div>
        </div>
      </section>

      {/* Challenge Suite Comparison Callout */}
      <section className="max-w-5xl mx-auto px-4">
        <div className="rounded-3xl bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-800 p-8 sm:p-12 relative overflow-hidden">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="space-y-4">
              <span className="text-xs font-semibold tracking-wider uppercase text-indigo-400">
                Empirical Evaluation
              </span>
              <h3 className="text-2xl sm:text-3xl font-bold text-white">
                Context, Sarcasm & Negation Mastery
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Traditional keyword baselines stumble on phrases like <em>"not bad at all"</em> or sarcastic comments.
                Our champion model was tested against a 16-case challenge suite, scoring <strong>75.0% accuracy</strong> versus 37.5% on the baseline.
              </p>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  Double negation inversion resolution
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  Sarcasm tone disambiguation
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  Calibrated 3-class Softmax probabilities
                </li>
              </ul>
            </div>

            <div className="bg-slate-950/80 rounded-2xl border border-slate-800/80 p-5 space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800 text-xs">
                <span className="text-slate-400 font-mono">Sample Test</span>
                <span className="text-emerald-400 font-medium">Challenge Passed</span>
              </div>
              <p className="text-sm text-slate-200 italic font-serif">
                &ldquo;The movie was not bad at all, in fact I thoroughly enjoyed the plot twist.&rdquo;
              </p>
              <div className="grid grid-cols-2 gap-3 pt-2 text-xs">
                <div className="p-2.5 rounded-lg bg-rose-950/20 border border-rose-900/30">
                  <span className="text-slate-400 block text-[11px]">TF-IDF Baseline</span>
                  <span className="text-rose-400 font-semibold">NEGATIVE ❌ (Keyword bias)</span>
                </div>
                <div className="p-2.5 rounded-lg bg-emerald-950/20 border border-emerald-900/30">
                  <span className="text-slate-400 block text-[11px]">RoBERTa Champion</span>
                  <span className="text-emerald-400 font-semibold">POSITIVE ✅ (96.4%)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

