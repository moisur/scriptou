import React from 'react';
import { YoutubeIcon as Youtube, Clock } from './ui/icons';

const Automations: React.FC = () => {
  return (
    <section className="py-12 sm:py-16 lg:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-left">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl" style={{ color: 'var(--text-dark)' }}>
            Automatisations
          </h2>
          <p className="mt-4 text-lg leading-8" style={{ color: 'var(--text-medium)' }}>
            Laissez l'IA travailler pour vous 24/7. Nos automatisations intelligentes surveillent, analysent et digèrent continuellement le contenu pendant que vous dormez, vous assurant de ne jamais manquer les informations importantes de vos sources préférées.
          </p>
        </div>
        <div className="mt-10">
          <div className="rounded-xl border p-6" style={{ borderColor: 'var(--border-color)', backgroundColor: 'var(--background-card)' }}>
            <div className="flex items-start justify-between">
              <div className="flex items-start">
                <div className="mr-4 flex-shrink-0">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-100">
                    <Youtube className="h-6 w-6 text-red-500" />
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold" style={{ color: 'var(--text-dark)' }}>
                    Récapitulatif YouTube Quotidien
                  </h3>
                  <p className="mt-2 text-base" style={{ color: 'var(--text-medium)' }}>
                    Obtenez des résumés quotidiens des nouvelles vidéos de vos chaînes YouTube préférées, livrés chaque matin à 8h00.
                  </p>
                  <div className="mt-4 flex items-center space-x-4 text-sm" style={{ color: 'var(--text-medium)' }}>
                    <span className="flex items-center text-green-600">
                      <span className="mr-1.5 h-2 w-2 rounded-full bg-green-500"></span>
                      Actif
                    </span>
                    <span className="flex items-center">
                      <Clock className="mr-1.5 h-5 w-5" />
                      Prochaine exécution : Demain à 8:00
                    </span>
                  </div>
                </div>
              </div>
              <button className="ml-4 rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50">
                Gérer
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Automations;
