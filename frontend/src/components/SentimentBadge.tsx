import React from 'react';

interface SentimentBadgeProps {
  sentiment: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL' | string;
  size?: 'sm' | 'md' | 'lg';
}

export const SentimentBadge: React.FC<SentimentBadgeProps> = ({ sentiment, size = 'md' }) => {
  const norm = sentiment.toUpperCase();

  const styles = {
    POSITIVE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    NEGATIVE: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
    NEUTRAL: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
  }[norm] || 'bg-slate-500/10 text-slate-400 border-slate-500/30';

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5 border',
    md: 'text-xs px-3 py-1 border font-medium tracking-wide',
    lg: 'text-sm px-4 py-1.5 border font-semibold tracking-wider',
  }[size];

  const dotColor = {
    POSITIVE: 'bg-emerald-400',
    NEGATIVE: 'bg-rose-400',
    NEUTRAL: 'bg-cyan-400',
  }[norm] || 'bg-slate-400';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full ${styles} ${sizeClasses}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotColor} animate-pulse`} />
      {norm}
    </span>
  );
};

