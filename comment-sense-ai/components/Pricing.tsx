import React from 'react';

const CheckIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" fill="#00BFFF" fillOpacity="0.1"/>
    <path d="M9.5 12.5L11.5 14.5L14.5 10" stroke="#00BFFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const tiers = [
  {
    name: 'Créateur',
    price: '19€',
    description: 'Parfait pour les créateurs individuels et les petites entreprises.',
    features: [
      'Analyse jusqu\'à 50 vidéos par mois',
      '10 000 commentaires par vidéo',
      'Analyse des Sentiments',
      'Détection des Thèmes Clés',
      'Support par e-mail',
    ],
    cta: 'Choisir le Forfait Créateur',
    priceId: 'price_12345', // Replace with your actual Price ID from Stripe
    popular: false,
  },
  {
    name: 'Pro',
    price: '49€',
    description: 'Pour les utilisateurs avancés et les analystes de marque qui en veulent plus.',
    features: [
      'Analyse jusqu\'à 200 vidéos par mois',
      '50 000 commentaires par vidéo',
      'Toutes les fonctionnalités Créateur',
      'Exportation des données en CSV',
      'Support Prioritaire',
    ],
    cta: 'Choisir le Forfait Pro',
    priceId: 'price_67890', // Replace with your actual Price ID from Stripe
    popular: true,
  },
  {
    name: 'Entreprise',
    price: 'Contactez-nous',
    description: 'Solutions sur mesure pour les agences et les grandes équipes.',
    features: [
      'Analyse vidéo illimitée',
      'Commentaires illimités',
      'Accès API',
      'Gestionnaire de Compte Dédié',
      'Intégrations Personnalisées',
    ],
    cta: 'Contacter les Ventes',
    priceId: null,
    popular: false,
  },
];

const Pricing: React.FC = () => {
  const handleCheckout = async (priceId: string | null) => {
    if (!priceId) {
      window.location.href = 'mailto:sales@scriptou.com'; // Replace with your sales email
      return;
    }
    // The checkout logic will be implemented later.
  };

  return (
    <section id="pricing" className="py-20" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4" style={{ color: 'var(--text-main)' }}>Trouvez le Forfait Idéal</h2>
          <p className="text-lg max-w-3xl mx-auto" style={{ color: 'var(--text-secondary)' }}>
            Commencez gratuitement, ou choisissez un forfait qui évolue avec vos besoins. Pas de frais cachés, annulez à tout moment.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto items-stretch">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className={`rounded-2xl p-8 flex flex-col ${tier.popular ? 'border-2 border-[#00BFFF] shadow-2xl relative' : 'border border-gray-200'}`}
              style={{ backgroundColor: 'var(--background-card)' }}
            >
              {tier.popular && (
                <div className="absolute top-0 -translate-y-1/2 left-1/2 -translate-x-1/2">
                  <span className="bg-[#00BFFF] text-white px-4 py-1 rounded-full text-sm font-bold whitespace-nowrap">
                    LE PLUS POPULAIRE
                  </span>
                </div>
              )}
              <div className="flex-grow">
                <h3 className="text-2xl font-bold mb-2" style={{ color: 'var(--text-main)' }}>{tier.name}</h3>
                <p className="mb-6" style={{ color: 'var(--text-secondary)', minHeight: '5rem' }}>{tier.description}</p>
                
                {tier.price === 'Contactez-nous' ? (
                  <div className="text-left my-8">
                      <h4 className="text-4xl font-extrabold" style={{ color: 'var(--text-main)' }}>Contactez-nous</h4>
                  </div>
                ) : (
                  <div className="mb-8">
                    <span className="text-5xl font-extrabold" style={{ color: 'var(--text-main)' }}>{tier.price.split('€')[0]}</span>
                    <span className="text-4xl font-extrabold" style={{ color: 'var(--text-main)' }}>€</span>
                    <span className="text-xl" style={{ color: 'var(--text-secondary)' }}> / mois</span>
                  </div>
                )}
                
                <ul className="space-y-4">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-start">
                      <div className="flex-shrink-0 pt-1">
                        <CheckIcon />
                      </div>
                      <span className="ml-3" style={{ color: 'var(--text-main)' }}>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-auto pt-8">
                  <button
                    onClick={() => handleCheckout(tier.priceId)}
                    className={`w-full py-3 rounded-lg font-bold text-lg transition-transform transform hover:scale-105 ${
                      tier.popular ? 'text-white' : 'text-gray-700'
                    }`}
                    style={{
                      backgroundColor: tier.popular ? '#00BFFF' : '#F7FAFC',
                      border: tier.popular ? 'none' : '1px solid #E2E8F0'
                    }}
                  >
                    {tier.cta}
                  </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Pricing;