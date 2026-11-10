export interface SentimentProbabilities {
  positive: number;
  negative: number;
  neutral: number;
}

export interface SentimentResult {
  sentiment: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
  confidence: number;
  probabilities: SentimentProbabilities;
  model_version: string;
  model_id: string;
  latency_ms?: number;
  id?: number;
  created_at?: string;
}

export interface AnalyzeResponse {
  success: boolean;
  result: SentimentResult;
}

export interface BatchAnalyzeResponse {
  success: boolean;
  results: SentimentResult[];
  total_processed: number;
  average_latency_ms: number;
}

export interface HistoryItem {
  id: number;
  text: string;
  text_preview: string;
  sentiment: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
  confidence: number;
  probabilities: SentimentProbabilities;
  model_id: string;
  model_version: string;
  source: string;
  latency_ms?: number;
  created_at: string;
}

export interface HistoryResponse {
  success: boolean;
  total: number;
  page: number;
  page_size: number;
  items: HistoryItem[];
}

export interface SentimentCount {
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

export interface AnalyticsResponse {
  success: boolean;
  summary: SentimentCount;
  percentages: {
    positive: number;
    negative: number;
    neutral: number;
  };
  average_confidence: number;
  average_latency_ms: number;
  timeline: Array<{
    date: string;
    positive: number;
    negative: number;
    neutral: number;
    total: number;
  }>;
  recent_activity: HistoryItem[];
}

export interface ModelInfoResponse {
  success: boolean;
  model_id: string;
  model_type: string;
  version: string;
  classes: string[];
  device: string;
  is_loaded: boolean;
  benchmark: {
    test_macro_f1: number;
    test_accuracy: number;
    challenge_suite_accuracy: number;
    f1_negative: number;
    f1_neutral: number;
    f1_positive: number;
  };
  description: string;
}

