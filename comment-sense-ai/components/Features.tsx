import React from 'react';
import { BotIcon, SearchIcon, BarChartIcon, GlobeIcon, FileText, ZapIcon } from './ui/icons';

const features = [
  {
    icon: <ZapIcon className="w-12 h-12 text-blue-500" />,
    title: "Analyse Sémantique Avancée",
    description: "Notre IA ne se contente pas de lire les mots, elle en comprend le sens, les nuances et les intentions cachées.",
  },
  {
    icon: <SearchIcon className="w-12 h-12 text-green-500" />,
    title: "Détection de Thèmes Émergents",
    description: "Identifiez automatiquement les sujets de conversation récurrents et les tendances qui animent votre communauté.",
  },
  {
    icon: <BotIcon className="w-12 h-12 text-purple-500" />,
    title: "Synthèse par IA Générative",
    description: "Recevez des résumés clairs et concis pour chaque thème, rédigés par une IA de pointe pour une compréhension instantanée.",
  },
  {
    icon: <BarChartIcon className="w-12 h-12 text-red-500" />,
    title: "Analyse de Sentiments Fine",
    description: "Sachez non seulement ce que les gens disent, mais aussi ce qu'ils ressentent, avec une analyse de sentiments précise.",
  },
  {
    icon: <FileText className="w-12 h-12 text-yellow-500" />,
    title: "Export de Rapports Détaillés",
    description: "Générez des rapports complets pour partager vos découvertes et prendre des décisions basées sur des données tangibles.",
  },
  {
    icon: <GlobeIcon className="w-12 h-12 text-indigo-500" />,
    title: "Compréhension de l'Audience",
    description: "Découvrez les questions, les suggestions et les préoccupations de votre audience pour mieux y répondre.",
  },
];

const Features: React.FC = () => {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold" style={{ color: 'var(--text-main)' }}>
            Une Vision à 360° de Votre Communauté
          </h2>
          <p className="text-lg mt-4" style={{ color: 'var(--text-secondary)' }}>
            Allez au-delà des métriques de surface et plongez au cœur des conversations.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="p-6 rounded-lg shadow-lg" style={{ backgroundColor: 'var(--background-card)', border: `1px solid var(--border-color)` }}>
              <div className="flex justify-center mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-center mb-2" style={{ color: 'var(--text-main)' }}>
                {feature.title}
              </h3>
              <p className="text-center" style={{ color: 'var(--text-secondary)' }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
