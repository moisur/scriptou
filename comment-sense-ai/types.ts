
export interface Sentiment {
  comment_id: string;
  text: string;
  sentiment: 'positif' | 'négatif' | 'neutre';
  confidence: number;
}

export interface Analysis {
  keywords: string[];
  questions: string[];
  sentiments: Sentiment[];
}

export interface Summary {
  message: string;
  processedCount: number;
}

export interface CommentAnalysisResult {
  summary: Summary;
  analysis: Analysis;
}
