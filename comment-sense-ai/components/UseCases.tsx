import React, { useState } from 'react';

const useCasesData = [
  {
    id: 'analyst',
    title: 'Pour l\'Analyste de Marque',
    subtitle: 'Suivez les sentiments et trouvez des informations concurrentielles.',
    content: 'Surveillez en temps réel le sentiment des consommateurs lors des lancements de produits. Comprenez ce que les clients aiment ou n\'aiment pas dans les produits de vos concurrents en analysant les commentaires de leurs vidéos. Obtenez des retours bruts et non filtrés pour éclairer votre stratégie de marque.',
    img: 'téléchargement (1).jpg'
  },
  {
    id: 'creator',
    title: 'Pour le Créateur de Contenu',
    subtitle: 'Découvrez ce que votre public veut vraiment.',
    content: 'Écoutez les retours de votre public à grande échelle. Identifiez les questions courantes pour votre prochaine vidéo Q&R, découvrez quel contenu résonne le plus, et trouvez une mine d\'or de nouvelles idées de vidéos directement de vos fans les plus engagés.',
    img: 'téléchargement (2).jpg'
  },
  {
    id: 'researcher',
    title: 'Pour le Chercheur de Marché',
    subtitle: 'Repérez les tendances émergentes avant tout le monde.',
    content: 'Analysez les commentaires sur les vidéos leaders de l\'industrie pour identifier les tendances émergentes, les nouveaux besoins des consommateurs et les changements du marché. Synthétisez des milliers de points de données en thèmes concis pour étayer vos rapports de recherche.',
    img: 'téléchargement (3).jpg'
  },
  {
    id: 'student',
    title: 'Pour les Étudiants & Universitaires',
    subtitle: 'Accélérez vos recherches et vos études.',
    content: 'Rassemblez rapidement l\'opinion publique sur des sujets spécifiques pour des travaux de recherche ou des études de cas. Utilisez des données du monde réel pour étayer vos arguments sans collecte de données manuelle.',
    img: 'téléchargement (4).jpg'
  },
  {
    id: 'journalist',
    title: 'Pour les Journalistes',
    subtitle: 'Évaluez la réaction du public aux dernières nouvelles.',
    content: 'Comprenez instantanément le consensus public sur les sujets d\'actualité traités sur YouTube. Extrayez des citations et identifiez les points de vue clés pour vos articles.',
    img: 'téléchargement (6).jpg'
  }
];

const UseCases: React.FC = () => {
  const [activeTab, setActiveTab] = useState(useCasesData[0].id);

  const activeUseCase = useCasesData.find(uc => uc.id === activeTab);

  return (
    <section id="use-cases" className="py-20 md:py-28" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight" style={{ color: 'var(--text-dark)' }}>
            Un Outil pour Chaque Vision
          </h2>
          <p className="mt-4 text-lg" style={{ color: 'var(--text-medium)' }}>
            Que vous construisiez une marque, développiez une audience ou étudiiez un marché, Youtube Sniffer fournit les informations spécifiques dont vous avez besoin pour réussir.
          </p>
        </div>

        <div className="mt-12">
          <div className="flex justify-center flex-wrap gap-2 md:gap-4 border-b" style={{ borderColor: 'var(--border-color)' }}>
            {useCasesData.map(useCase => (
              <button
                key={useCase.id}
                onClick={() => setActiveTab(useCase.id)}
                className={`px-4 py-3 md:px-6 font-medium text-sm md:text-base -mb-px transition-all duration-300 ${
                  activeTab === useCase.id
                    ? 'border-b-2 text-white'
                    : 'hover:text-white border-b-2 border-transparent'
                }`}
                style={{
                  color: activeTab === useCase.id ? 'var(--primary-color)' : 'var(--text-medium)',
                  borderColor: activeTab === useCase.id ? 'var(--primary-color)' : 'transparent'
                }}
              >
                {useCase.title}
              </button>
            ))}
          </div>
          
          <div className="mt-8">
            {activeUseCase && (
              <div key={activeUseCase.id} className="grid md:grid-cols-2 gap-8 md:gap-12 items-center p-8 rounded-lg border animate-fadeIn" style={{ backgroundColor: 'var(--background-card)', borderColor: 'var(--border-color)' }}>
                <div>
                  <h3 className="text-2xl font-bold" style={{ color: 'var(--primary-color)' }}>{activeUseCase.subtitle}</h3>
                  <p className="mt-4 leading-relaxed" style={{ color: 'var(--text-medium)' }}>{activeUseCase.content}</p>
                </div>
                <div>
                    <img src={activeUseCase.img} alt={activeUseCase.title} className="rounded-lg shadow-2xl w-full h-auto object-cover" />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default UseCases;
