
import type { CommentAnalysisResult } from '../types';

// Type simple pour un commentaire, à affiner si nécessaire
interface Comment {
  id: string;
  text: string;
  // ... autres champs si besoin
}

export const getComments = async (videoUrl: string): Promise<Comment[]> => {
    const response = await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: videoUrl }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Failed to fetch comments' }));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.comments;
};


export const analyzeCommentsBatch = async (comments: Comment[]): Promise<CommentAnalysisResult> => {
    const response = await fetch('/api/analyze_batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments: comments }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'An unknown error occurred during analysis' }));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
};
