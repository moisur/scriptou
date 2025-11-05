import React, { useState } from 'react';
import { ChevronDownIcon } from './ui/icons';

const faqData = [
  {
    question: 'Est-ce conforme aux Conditions d\'Utilisation de YouTube ?',
    answer: 'Oui, notre outil utilise l\'API de données YouTube V3 officielle pour accéder aux données de commentaires publics, ce qui est entièrement conforme à leurs conditions d\'utilisation. Nous ne collectons pas de données d\'une manière qui viole leurs politiques.'
  },
  {
    question: 'Combien de commentaires puis-je analyser ?',
    answer: 'Le nombre de commentaires que vous pouvez analyser dépend du forfait que vous avez choisi. Notre forfait de base est généreux, et nos forfaits Pro et Entreprise offrent des limites nettement plus élevées, adaptées même aux vidéos les plus populaires.'
  },
  {
    question: 'Ai-je besoin de ma propre clé API Google/YouTube ?',
    answer: 'Non, vous n\'en avez pas besoin. Notre service gère toutes les interactions avec l\'API de notre côté. Il vous suffit de fournir l\'URL de la vidéo, et nous nous occupons du reste, ce qui rend le processus transparent pour vous.'
  },
  {
    question: 'Quelle est la précision de l\'analyse des sentiments ?',
    answer: 'Notre analyse des sentiments est alimentée par le modèle Gemini de pointe de Google, qui offre un haut degré de précision. Il comprend les nuances, le sarcasme et le contexte mieux que de nombreux modèles traditionnels. Cependant, comme toute IA, il n\'est pas parfait, mais il fournit une excellente vue d\'ensemble.'
  },
  {
    question: 'Puis-je exporter les données d\'analyse ?',
    answer: 'Oui ! Nos forfaits Pro et Entreprise vous permettent d\'exporter l\'analyse complète, y compris les scores de sentiment et les commentaires thématiques, dans un fichier CSV. C\'est parfait pour l\'intégration dans vos propres rapports et présentations.'
  }
];

const AccordionItem: React.FC<{
  question: string;
  answer: string;
  isOpen: boolean;
  onClick: () => void;
}> = ({ question, answer, isOpen, onClick }) => {
  return (
    <div className="border-b" style={{ borderColor: 'var(--border-color)' }}>
      <button
        onClick={onClick}
        className="flex justify-between items-center w-full py-5 text-left"
        aria-expanded={isOpen}
      >
        <span className="text-lg font-medium" style={{ color: 'var(--text-dark)' }}>{question}</span>
        <ChevronDownIcon
          className={`h-6 w-6 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
          style={{ color: 'var(--text-secondary)' }}
        />
      </button>
      <div
        style={{ maxHeight: isOpen ? '200px' : '0px' }}
        className="overflow-hidden transition-all duration-500 ease-in-out"
      >
        <div className="pb-5 pt-2 leading-relaxed" style={{ color: 'var(--text-medium)' }}>
            {answer}
        </div>
      </div>
    </div>
  );
};


const FAQ: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const handleClick = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="py-20 md:py-28" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight" style={{ color: 'var(--text-dark)' }}>
            Foire Aux Questions
          </h2>
          <p className="mt-4 text-lg" style={{ color: 'var(--text-medium)' }}>
            Vous avez des questions ? Nous avons des réponses. Si vous ne trouvez pas ce que vous cherchez, n'hésitez pas à nous contacter.
          </p>
        </div>

        <div className="mt-12 max-w-3xl mx-auto">
          {faqData.map((item, index) => (
            <AccordionItem
              key={index}
              question={item.question}
              answer={item.answer}
              isOpen={openIndex === index}
              onClick={() => handleClick(index)}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FAQ;
