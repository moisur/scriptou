import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { CheckIcon } from './ui/icons';

const stripePromise = loadStripe(process.env.VITE_STRIPE_PUBLISHABLE_KEY || 'pk_test_TYooMQauvdEDq54NiTphI7jx');

const tiers = [
  {
    name: 'Essentiel',
    description: 'Idéal pour visualiser et structurer des idées à partir de vidéos.',
    features: [
      'Mindmaps illimités',
      'Analyse de transcriptions',
      'Export en Markdown & PDF',
      'Support standard',
    ],
    cta: 'Choisir Essentiel',
    popular: false,
    pricing: {
      monthly: { price: '7.99€', priceSuffix: '/ mois', priceId: 'price_1P6ZqHJb2q1Vq9Q8Z1Z2Z3Z4' },
      annually: { price: '6.58€', priceSuffix: '/ mois', priceId: 'price_ANNUAL_ESSENTIEL_PLACEHOLDER', annualBilling: 'facturé 79€ / an' },
    }
  },
  {
    name: 'Pro',
    description: 'L\'outil complet pour les créateurs et analystes de marque.',
    features: [
      'Toutes les fonctionnalités Essentiel',
      'Analyse de commentaires par IA',
      'Détection de thèmes et sentiments',
      'Idées de vidéos générées par IA',
      'Exportation des données en CSV',
      'Automatisations (Récapitulatifs YouTube)',
      'Support prioritaire',
    ],
    cta: 'Choisir Pro',
    popular: true,
    pricing: {
        monthly: { price: '9.99€', priceSuffix: '/ mois', priceId: 'price_1P6ZrHJb2q1Vq9Q8iJkLmNoP' },
        annually: { price: '8.25€', priceSuffix: '/ mois', priceId: 'price_ANNUAL_PRO_PLACEHOLDER', annualBilling: 'facturé 99€ / an' },
    }
  },
  {
    name: 'Entreprise',
    description: 'Pour les agences et les entreprises avec des besoins spécifiques.',
    features: [
      'Toutes les fonctionnalités Pro',
      'Analyses de vidéos en volume',
      'Limites de commentaires personnalisées',
      'Accès API',
      'Gestionnaire de compte dédié',
    ],
    cta: 'Contacter les ventes',
    popular: false,
    pricing: {
        monthly: { price: 'Contactez-nous', priceSuffix: '', priceId: null },
        annually: { price: 'Contactez-nous', priceSuffix: '', priceId: null },
    }
  },
];


interface PricingProps {
  setModalView: (view: 'login' | 'signup' | 'recover') => void;
  setModalMessage: (message: string) => void;
}

const Pricing: React.FC<PricingProps> = ({ setModalView, setModalMessage }) => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annually'>('monthly');

  const handleCheckout = async (priceId: string | null) => {
    if (!priceId) {
      window.location.href = 'mailto:sales@scriptou.com';
      return;
    }
    setModalMessage("Veuillez vous connecter ou créer un compte pour choisir votre forfait.");
    setModalView('login');
  };

  return (
    <section id="pricing" className="py-20" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4" style={{ color: 'var(--text-main)' }}>Un Forfait Adapté à Vos Ambitions</h2>
          <p className="text-lg max-w-3xl mx-auto" style={{ color: 'var(--text-secondary)' }}>
            Des forfaits mensuels simples et transparents pour répondre à vos besoins. Pas d'engagement annuel, juste de la puissance à la demande.
          </p>
        </div>

        <div className="flex justify-center items-center gap-4 mb-10">
            <span className={`font-semibold ${billingCycle === 'monthly' ? 'text-[#009EFA]' : 'text-gray-500'}`}>
                Mensuel
            </span>
            <button
                onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annually' : 'monthly')}
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-[#009EFA] focus:ring-offset-2 ${
                    billingCycle === 'annually' ? 'bg-[#009EFA]' : 'bg-gray-200'
                }`}
            >
                <span
                    className={`inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                        billingCycle === 'annually' ? 'translate-x-5' : 'translate-x-0'
                    }`}
                />
            </button>
            <span className={`font-semibold ${billingCycle === 'annually' ? 'text-[#009EFA]' : 'text-gray-500'}`}>
                Annuel <span className="text-green-600 font-bold">(Économisez 17%)</span>
            </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto items-stretch">
          {tiers.map((tier) => {
            const currentPrice = tier.pricing[billingCycle];
            return (
                <div
                key={tier.name}
                className={`rounded-2xl p-8 flex flex-col ${tier.popular ? 'border-2 border-[#009EFA] shadow-2xl relative' : 'border border-gray-200'}`}
                style={{ backgroundColor: 'var(--background-card)' }}
                >
                {tier.popular && (
                    <div className="absolute top-0 -translate-y-1/2 left-1/2 -translate-x-1/2">
                    <span className="bg-[#009EFA] text-white px-4 py-1 rounded-full text-sm font-bold whitespace-nowrap">
                        LE PLUS POPULAIRE
                    </span>
                    </div>
                )}
                <div className="flex-grow">
                    <h3 className="text-2xl font-bold mb-2" style={{ color: 'var(--text-main)' }}>{tier.name}</h3>
                    <p className="mb-6" style={{ color: 'var(--text-secondary)', minHeight: '5rem' }}>{tier.description}</p>
                    
                    <div className="mb-8" style={{ minHeight: '6rem' }}>
                        {currentPrice.priceId === null ? (
                             <div className="text-left my-8">
                                <h4 className="text-4xl font-extrabold" style={{ color: 'var(--text-main)' }}>Contactez-nous</h4>
                            </div>
                        ) : (
                            <div>
                                <span className="text-5xl font-extrabold" style={{ color: 'var(--text-main)' }}>
                                    {currentPrice.price.replace('€', '')}
                                </span>
                                <span className="text-4xl font-extrabold" style={{ color: 'var(--text-main)' }}>€</span>
                                <span className="text-xl" style={{ color: 'var(--text-secondary)' }}>{currentPrice.priceSuffix}</span>
                            </div>
                        )}
                        {billingCycle === 'annually' && 'annualBilling' in currentPrice && currentPrice.annualBilling && (
                           <p className="text-sm text-gray-500 mt-1">{currentPrice.annualBilling}</p>
                        )}
                    </div>
                    
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
                    onClick={() => handleCheckout(currentPrice.priceId)}
                    className={`w-full py-3 rounded-lg font-bold text-lg transition-transform transform hover:scale-105 ${
                    tier.popular ? 'text-white' : 'text-gray-700'
                    }`}
                    style={{
                        backgroundColor: tier.popular ? '#009EFA' : '#F7FAFC',
                        border: tier.popular ? 'none' : '1px solid #E2E8F0'
                    }}
                >
                    {tier.cta}
                </button>
                </div>
                </div>
            )
          })}
        </div>
      </div>
    </section>
  );
};

export default Pricing;