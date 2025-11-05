import React from 'react';

const TrustedBy: React.FC = () => {
  return (
    <section className="py-12" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-6 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>
          Approuvé par les équipes les plus innovantes au monde
        </p>
        <div className="mt-6 flex flex-wrap justify-center items-center gap-x-8 gap-y-4 md:gap-x-12 lg:gap-x-16" style={{ color: 'var(--grey-dark)' }}>
          <span className="font-bold text-xl tracking-tight">InnovateCorp</span>
          <span className="font-bold text-xl tracking-tight">QuantumLeap</span>
          <span className="font-bold text-xl tracking-tight">FutureBrand</span>
          <span className="font-bold text-xl tracking-tight">MarketPulse</span>
          <span className="font-bold text-xl tracking-tight">CreatorHub</span>
        </div>
      </div>
    </section>
  );
};

export default TrustedBy;
