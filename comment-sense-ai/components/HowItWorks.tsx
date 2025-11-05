import React from 'react';
import { YoutubeIcon, BotIcon, FileText } from './ui/icons';

const steps = [
    {
        icon: <YoutubeIcon style={{ color: 'var(--primary-color)' }} className="h-10 w-10" />,
        title: "1. Fournissez une Vidéo YouTube",
        description: "Collez simplement l'URL de la vidéo YouTube que vous souhaitez analyser. Aucune extension ou téléchargement n'est nécessaire."
    },
    {
        icon: <BotIcon style={{ color: 'var(--secondary-color)' }} className="h-10 w-10" />,
        title: "2. L'IA Scanne & Analyse",
        description: "Notre système récupère les commentaires et utilise Gemini pour effectuer une analyse approfondie du texte."
    },
    {
        icon: <FileText style={{ color: 'var(--accent-color)' }} className="h-10 w-10" />,
        title: "3. Obtenez Votre Rapport",
        description: "Recevez un rapport complet avec l'analyse des sentiments, les thèmes clés et des informations exploitables."
    }
]

const HowItWorks: React.FC = () => {
  return (
    <section id="how-it-works" className="py-20 md:py-28" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight" style={{ color: 'var(--text-dark)' }}>
            Des Commentaires Bruts aux Riches Aperçus en <span style={{ color: 'var(--primary-color)' }}>3 Étapes Simples</span>
          </h2>
          <p className="mt-4 text-lg" style={{ color: 'var(--text-medium)' }}>
            Notre processus simplifié rend l'analyse complexe sans effort. Découvrez comment transformer les retours de l'audience en décisions stratégiques.
          </p>
        </div>
        <div className="mt-16 grid md:grid-cols-3 gap-8 md:gap-12 relative">
            <div className="absolute top-12 left-0 w-full h-px hidden md:block" style={{ backgroundColor: 'var(--border-color)' }} aria-hidden="true">
            </div>
            
            {steps.map((step, index) => (
                 <div key={index} className="relative p-8 rounded-2xl border text-center z-10" style={{ backgroundColor: 'var(--background-card)', borderColor: 'var(--border-color)' }}>
                    <div className="inline-flex h-20 w-20 items-center justify-center rounded-full mb-6 border-2" style={{ backgroundColor: 'rgba(var(--primary-color-rgb), 0.1)', borderColor: 'var(--border-color)' }}>
                        {step.icon}
                    </div>
                    <h3 className="text-xl font-bold mb-2" style={{ color: 'var(--text-dark)' }}>{step.title}</h3>
                    <p style={{ color: 'var(--text-medium)' }}>{step.description}</p>
                </div>
            ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
