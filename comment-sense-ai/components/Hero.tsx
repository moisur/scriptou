import React from 'react';

const Hero: React.FC = () => {
  return (
    <section className="relative text-center py-24" style={{ backgroundColor: 'var(--background-light)' }}>
      <div className="container mx-auto px-4 z-10">
        <div className="inline-block px-3 py-1 rounded-full text-sm mb-6" style={{ backgroundColor: 'rgba(37, 162, 242, 0.1)', color: '#009EFA' }}>
          Propulsé par Gemini 1.5 Flash
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold mb-4 leading-tight" style={{ color: '#1A202C' }}>
          Scriptou: Mindmaps et Analyses de<br />
          Commentaires.<br />
          <span className="text-5xl md:text-6xl" style={{ color: '#009EFA' }}>En un clic.</span>
        </h1>
        <p className="text-lg md:text-xl mb-10 max-w-4xl mx-auto" style={{ color: '#4A5568' }}>
          Générez des mindmaps instantanées à partir de n'importe quelle vidéo YouTube et analysez des milliers de commentaires pour en extraire les vrais insights.
        </p>
        <div className="flex justify-center space-x-4 mb-12">
          <a
            href="#demo"
            className="px-8 py-4 rounded-full font-bold text-white text-lg transition-transform transform hover:scale-105 shadow-lg"
            style={{
              backgroundColor: '#009EFA',
            }}
          >
            Essayer la Démo
          </a>
          <a
            href="#how-it-works"
            className="px-8 py-4 rounded-full font-bold text-lg transition-transform transform hover:scale-105"
            style={{
              backgroundColor: 'white',
              color: '#4A5568',
              border: `2px solid #CBD5E0`
            }}
          >
            Comment ça marche
          </a>
        </div>
        <p className="text-md" style={{ color: '#718096' }}>
          Rejoignez plus de 50 000 utilisateurs qui transforment les commentaires en clarté.
        </p>
      </div>
    </section>
  );
};

export default Hero;
