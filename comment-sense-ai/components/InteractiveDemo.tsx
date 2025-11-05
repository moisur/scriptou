import React, { useState, useCallback, useEffect } from 'react';
import { getComments, analyzeCommentsBatch } from '../services/geminiService';
import type { CommentAnalysisResult } from '../types';
import { BarChartIcon, BotIcon } from './ui/icons';

const personas = [
    { id: 'brand_analyst', name: 'Analyste de Marque', promptPath: 'prompt/brand_analyst.txt' },
    { id: 'content_creator', name: 'Créateur de Contenu', promptPath: 'prompt/content_creator.txt' },
    { id: 'market_researcher', name: 'Chercheur de Marché', promptPath: 'prompt/market_researcher.txt' },
    { id: 'student', name: 'Étudiant & Universitaire', promptPath: 'prompt/student.txt' },
    { id: 'journalist', name: 'Journaliste', promptPath: 'prompt/journalist.txt' },
];

type AnalysesState = {
    [key: string]: CommentAnalysisResult | null;
};

const InteractiveDemo: React.FC = () => {
    const [url, setUrl] = useState('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
    const [isLoading, setIsLoading] = useState<string | null>(null); // Store persona ID
    const [analyses, setAnalyses] = useState<AnalysesState>({});
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<string | null>(null);

    useEffect(() => {
        const savedAnalyses = localStorage.getItem('commentAnalyses');
        if (savedAnalyses) {
            setAnalyses(JSON.parse(savedAnalyses));
            const firstAnalysis = Object.keys(JSON.parse(savedAnalyses))[0];
            if (firstAnalysis) {
                setActiveTab(firstAnalysis);
            }
        }
    }, []);

    const handleAnalysis = useCallback(async (personaId: string) => {
        if (!url) {
            setError('Veuillez entrer une URL YouTube.');
            return;
        }
        setIsLoading(personaId);
        setError(null);

        try {
            const comments = await getComments(url);
            if (comments.length === 0) {
                setError("Aucun commentaire trouvé pour cette vidéo ou impossible de les récupérer.");
                setIsLoading(null);
                return;
            }
            const result = await analyzeCommentsBatch(comments);
            const newAnalyses = { ...analyses, [personaId]: result };
            setAnalyses(newAnalyses);
            setActiveTab(personaId);
            localStorage.setItem('commentAnalyses', JSON.stringify(newAnalyses));
        } catch (err) {
            setError(`Échec de l'analyse. Veuillez réessayer.`);
            console.error(err);
        } finally {
            setIsLoading(null);
        }
    }, [url, analyses]);

    const getSentimentStyle = (sentiment: 'positif' | 'négatif' | 'neutre') => {
        switch (sentiment) {
            case 'positif': return { color: 'var(--success-color)', icon: '👍' };
            case 'négatif': return { color: 'var(--error-color)', icon: '👎' };
            case 'neutre': return { color: 'var(--secondary-color)', icon: '🤔' };
            default: return { color: 'var(--text-secondary)', icon: ' ' };
        }
    };

    const currentAnalysis = activeTab ? analyses[activeTab] : null;

    return (
        <section id="demo" className="py-20 md:py-28" style={{ backgroundColor: 'var(--background-light)' }}>
            <div className="container mx-auto px-6">
                <div className="text-center max-w-3xl mx-auto">
                    <h2 className="text-3xl md:text-4xl font-bold tracking-tight" style={{ color: 'var(--text-dark)' }}>
                        Voyez la Magie en Action
                    </h2>
                    <p className="mt-4 text-lg" style={{ color: 'var(--text-medium)' }}>
                        Collez une URL YouTube et choisissez un profil pour lancer une analyse IA des commentaires.
                    </p>
                </div>

                <div className="mt-12 max-w-2xl mx-auto">
                    <div className="flex flex-col sm:flex-row gap-2 p-2 rounded-xl border shadow-lg" style={{ backgroundColor: 'var(--background-card)', borderColor: 'var(--border-color)' }}>
                        <input
                            type="text"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="https://www.youtube.com/watch?v=..."
                            className="flex-grow bg-transparent rounded-lg px-4 py-3 focus:outline-none transition-all w-full"
                            style={{ color: 'var(--text-dark)' }}
                        />
                    </div>
                </div>

                {error && <p className="text-center mt-6" style={{ color: 'var(--error-color)' }}>{error}</p>}

                <div className="mt-12 max-w-5xl mx-auto">
                    <div className="text-center mb-8">
                        <p className="mb-4 font-semibold" style={{ color: 'var(--text-medium)' }}>Choisissez votre rôle pour commencer ou ajouter une analyse :</p>
                        <div className="flex flex-wrap justify-center gap-3">
                            {personas.map((persona) => (
                                <button
                                    key={persona.id}
                                    onClick={() => handleAnalysis(persona.id)}
                                    disabled={!!isLoading}
                                    className="disabled:cursor-not-allowed text-white font-semibold py-2 px-5 rounded-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center"
                                    style={{ backgroundColor: 'var(--primary-color)' }}
                                >
                                    {isLoading === persona.id ? (
                                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                    ) : <BotIcon className="h-5 w-5 mr-2"/> }
                                    <span className="ml-2">{isLoading === persona.id ? 'Analyse...' : persona.name}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {Object.keys(analyses).length > 0 && (
                        <>
                            <div className="border-b" style={{ borderColor: 'var(--border-color)' }}>
                                <nav className="-mb-px flex space-x-6" aria-label="Tabs">
                                    {personas.map((persona) => (
                                        analyses[persona.id] && (
                                            <button
                                                key={persona.id}
                                                onClick={() => setActiveTab(persona.id)}
                                                className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors
                                                    ${activeTab === persona.id
                                                        ? 'border-indigo-500 text-indigo-600'
                                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                                    }`}
                                            >
                                                {persona.name}
                                            </button>
                                        )
                                    ))}
                                </nav>
                            </div>

                            {currentAnalysis && (
                                <div className="mt-8 p-6 sm:p-8 rounded-2xl border animate-fadeIn" style={{ backgroundColor: 'var(--background-card)', borderColor: 'var(--border-color)' }}>
                                    <div className="mb-6 text-center p-4 rounded-lg" style={{backgroundColor: 'var(--background-light)'}}>
                                        <p className="font-semibold text-lg" style={{color: 'var(--text-dark)'}}>{currentAnalysis.summary?.message}</p>
                                    </div>

                                    <div className="grid lg:grid-cols-2 gap-8">
                                        <div>
                                            <h3 className="text-lg font-bold mb-4" style={{ color: 'var(--text-dark)' }}>Mots-clés</h3>
                                            <div className="flex flex-wrap gap-2">
                                                {currentAnalysis.analysis?.keywords.map((keyword, index) => (
                                                    <span key={index} className="text-sm font-medium px-3 py-1 rounded-full" style={{ backgroundColor: 'var(--primary-color-light)', color: 'var(--primary-color-dark)' }}>
                                                        {keyword}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                        <div>
                                            <h3 className="text-lg font-bold mb-4" style={{ color: 'var(--text-dark)' }}>Questions des utilisateurs</h3>
                                            <ul className="space-y-2">
                                                {currentAnalysis.analysis?.questions.map((question, index) => (
                                                    <li key={index} className="flex items-start">
                                                        <span className="mr-3 mt-1" style={{ color: 'var(--primary-color)' }}>&#10067;</span>
                                                        <span style={{ color: 'var(--text-medium)' }}>{question}</span>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>

                                    <div className="mt-8">
                                        <h3 className="text-lg font-bold mb-4" style={{ color: 'var(--text-dark)' }}>Analyse des Sentiments</h3>
                                        <div className="overflow-x-auto">
                                            <table className="min-w-full divide-y divide-gray-200" style={{ borderColor: 'var(--border-color)' }}>
                                                <thead style={{ backgroundColor: 'var(--background-light)' }}>
                                                    <tr>
                                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>Sentiment</th>
                                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>Confiance</th>
                                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>Commentaire</th>
                                                    </tr>
                                                </thead>
                                                <tbody className="divide-y divide-gray-200" style={{ borderColor: 'var(--border-color)', backgroundColor: 'var(--background-card)' }}>
                                                    {currentAnalysis.analysis?.sentiments.map((item) => {
                                                        const style = getSentimentStyle(item.sentiment);
                                                        return (
                                                            <tr key={item.comment_id}>
                                                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium" style={{ color: style.color }}>
                                                                    <span className="mr-2">{style.icon}</span>
                                                                    {item.sentiment.charAt(0).toUpperCase() + item.sentiment.slice(1)}
                                                                </td>
                                                                <td className="px-6 py-4 whitespace-nowrap text-sm" style={{ color: 'var(--text-medium)' }}>{(item.confidence * 100).toFixed(0)}%</td>
                                                                <td className="px-6 py-4 text-sm" style={{ color: 'var(--text-medium)' }}>{item.text}</td>
                                                            </tr>
                                                        );
                                                    })}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </section>
    );
};

export default InteractiveDemo;
