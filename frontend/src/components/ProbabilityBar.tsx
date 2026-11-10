import React from 'react';

interface ProbabilityBarProps {
  label: string;
  value: number; // 0.0 to 1.0
  color: 'emerald' | 'rose' | 'cyan' | 'indigo';
}

export const ProbabilityBar: React.FC<ProbabilityBarProps> = ({ label, value, color }) => {
  const percentage = Math.round(value * 100);

  const colorStyles = {
    emerald: {
      bar: 'bg-gradient-to-r from-emerald-500 to-teal-400',
      text: 'text-emerald-400',
      bg: 'bg-emerald-950/30'
    },
    rose: {
      bar: 'bg-gradient-to-r from-rose-500 to-pink-500',
      text: 'text-rose-400',
      bg: 'bg-rose-950/30'
    },
    cyan: {
      bar: 'bg-gradient-to-r from-cyan-500 to-blue-400',
      text: 'text-cyan-400',
      bg: 'bg-cyan-950/30'
    },
    indigo: {
      bar: 'bg-gradient-to-r from-indigo-500 to-purple-500',
      text: 'text-indigo-400',
      bg: 'bg-indigo-950/30'
    }
  }[color];

  return (
    <div className="space-y-1.5">
      <div className="flex justify-between items-center text-xs">
        <span className="text-slate-300 font-medium">{label}</span>
        <span className={`font-mono font-semibold ${colorStyles.text}`}>{percentage}%</span>
      </div>
      <div className={`h-2.5 w-full rounded-full ${colorStyles.bg} overflow-hidden p-0.5 border border-slate-800`}>
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${colorStyles.bar}`}
          style={{ width: `${Math.max(percentage, 2)}%` }}
        />
      </div>
    </div>
  );
};

