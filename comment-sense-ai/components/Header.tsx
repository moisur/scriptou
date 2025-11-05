import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50" style={{ backgroundColor: 'var(--background-card)', borderBottom: '1px solid var(--border-color)' }}>
      <div className="container mx-auto px-6 py-3 flex justify-between items-center">
        <a href="#" className="flex items-center">
          <img src="/Scriptou.png" alt="Scriptou Logo" className="h-10 mr-3"/>
          <span className="text-xl font-bold tracking-tighter" style={{ color: 'var(--text-dark)' }}>
            Scriptou
          </span>
        </a>
        <nav className="hidden md:flex items-center space-x-8">
          <a href="#features" className="text-sm font-medium" style={{ color: 'var(--text-medium)' }}>Fonctionnalités</a>
          <a href="#demo" className="text-sm font-medium" style={{ color: 'var(--text-medium)' }}>Démo</a>
          <a href="#use-cases" className="text-sm font-medium" style={{ color: 'var(--text-medium)' }}>Cas d'Usage</a>
          <a href="#pricing" className="text-sm font-medium" style={{ color: 'var(--text-medium)' }}>Tarifs</a>
        </nav>
        <a
          href="#pricing"
          className="text-white font-semibold text-sm py-2 px-5 rounded-full transition-all duration-300 transform hover:scale-105"
          style={{ backgroundColor: 'var(--primary-color)' }}
        >
          Commencer
        </a>
      </div>
    </header>
  );
};

export default Header;