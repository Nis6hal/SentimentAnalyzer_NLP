import axios from 'axios';
import type {
  AnalyzeResponse,
  BatchAnalyzeResponse,
  HistoryResponse,
  AnalyticsResponse,
  ModelInfoResponse
} from '../types/sentiment';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

export const sentimentApi = {
  async analyzeText(text: string): Promise<AnalyzeResponse> {
    const res = await apiClient.post<AnalyzeResponse>('/analyze', { text });
    return res.data;
  },

  async analyzeBatch(texts: string[]): Promise<BatchAnalyzeResponse> {
    const res = await apiClient.post<BatchAnalyzeResponse>('/analyze/batch', { texts });
    return res.data;
  },

  async getHistory(page = 1, pageSize = 20, sentiment?: string): Promise<HistoryResponse> {
    const params: Record<string, string | number> = { page, page_size: pageSize };
    if (sentiment && sentiment !== 'ALL') {
      params.sentiment = sentiment;
    }
    const res = await apiClient.get<HistoryResponse>('/history', { params });
    return res.data;
  },

  async getAnalytics(): Promise<AnalyticsResponse> {
    const res = await apiClient.get<AnalyticsResponse>('/analytics');
    return res.data;
  },

  async getModelInfo(): Promise<ModelInfoResponse> {
    const res = await apiClient.get<ModelInfoResponse>('/model/info');
    return res.data;
  },

  async submitFeedback(
    analysisId: number,
    isCorrect: boolean,
    actualSentiment?: string,
    comment?: string
  ): Promise<{ success: boolean; message: string }> {
    const res = await apiClient.post('/feedback', {
      analysis_id: analysisId,
      is_correct: isCorrect,
      actual_sentiment: actualSentiment,
      comment,
    });
    return res.data;
  },

  async checkHealth(): Promise<{ status: string; database: string; inference_engine: string }> {
    const res = await apiClient.get('/health');
    return res.data;
  }
};

