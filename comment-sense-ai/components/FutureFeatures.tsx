import React from 'react';
import { Mail, FileText } from './ui/icons'; // Supposant que ces icônes existent

const FutureFeatures: React.FC = () => {
  return (
    <section className="py-12 sm:py-16 lg:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-left">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl" style={{ color: 'var(--text-dark)' }}>
            Bientôt disponible
          </h2>
        </div>
        <div className="mt-10 space-y-8">
          {/* Personalized Daily Newsletter */}
          <div className="rounded-xl border p-6" style={{ borderColor: 'var(--border-color)', backgroundColor: 'var(--background-card)' }}>
            <div className="flex items-start justify-between">
              <div className="flex items-start">
                <div className="mr-4 flex-shrink-0">
                  {/* Remplacer par une icône appropriée si disponible */}
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
                     <Mail className="h-6 w-6 text-blue-500" />
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold" style={{ color: 'var(--text-dark)' }}>
                    Newsletter Quotidienne Personnalisée
                    <span className="ml-2 inline-block rounded-full bg-yellow-100 px-3 py-1 text-xs font-semibold text-yellow-800" style={{ backgroundColor: 'var(--yellow-light)', color: 'var(--text-dark)' }}>
                      Bientôt disponible
                    </span>
                  </h3>
                  <p className="mt-2 text-base" style={{ color: 'var(--text-medium)' }}>
                    Indiquez-nous vos centres d'intérêt et choisissez jusqu'à 3 sujets. Nous générerons une newsletter quotidienne basée sur le nouveau contenu YouTube de sources hautement réputées publié au cours des dernières 24 heures.
                  </p>
                </div>
              </div>
              <button disabled className="ml-4 rounded-md bg-gray-200 px-4 py-2 text-sm font-medium text-gray-500">
                Bientôt disponible
              </button>
            </div>
          </div>

          {/* Newsletter Digest */}
          <div className="rounded-xl border p-6" style={{ borderColor: 'var(--border-color)', backgroundColor: 'var(--background-card)' }}>
            <div className="flex items-start justify-between">
               <div className="flex items-start">
                <div className="mr-4 flex-shrink-0">
                  {/* Remplacer par une icône appropriée si disponible */}
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                    <FileText className="h-6 w-6 text-green-500" />
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold" style={{ color: 'var(--text-dark)' }}>
                    Résumé de Newsletters
                    <span className="ml-2 inline-block rounded-full bg-yellow-100 px-3 py-1 text-xs font-semibold text-yellow-800" style={{ backgroundColor: 'var(--yellow-light)', color: 'var(--text-dark)' }}>
                      Bientôt disponible
                    </span>
                  </h3>
                  <p className="mt-2 text-base" style={{ color: 'var(--text-medium)' }}>
                    Choisissez parmi des centaines de newsletters de premier plan dans divers secteurs. Nous digérerons les nouveaux e-mails des dernières 24 heures et les organiserons en résumés que vous pourrez lire en un seul endroit - fini le désordre dans votre boîte de réception !
                  </p>
                </div>
              </div>
              <button disabled className="ml-4 rounded-md bg-gray-200 px-4 py-2 text-sm font-medium text-gray-500">
                Bientôt disponible
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FutureFeatures;
