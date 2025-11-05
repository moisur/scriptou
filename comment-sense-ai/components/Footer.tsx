import React from 'react';
import { LinkedinIcon, TwitterIcon, InstagramIcon } from './ui/icons';

const Footer: React.FC = () => {
  return (
    <footer style={{ backgroundColor: 'var(--background-card)', borderTop: '1px solid var(--border-color)' }}>
      <div className="container mx-auto px-6 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
           <div className="text-center md:text-left">
             <a href="#" className="text-lg font-bold tracking-tighter" style={{ color: 'var(--text-dark)' }}>
               Youtube Sniffer
             </a>
            <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Libérez la voix de votre audience.</p>
           </div>
          <div className="flex flex-wrap justify-center gap-x-6 gap-y-2">
            <a href="#features" className="text-sm" style={{ color: 'var(--text-medium)' }}>Fonctionnalités</a>
            <a href="#demo" className="text-sm" style={{ color: 'var(--text-medium)' }}>Démo</a>
            <a href="#pricing" className="text-sm" style={{ color: 'var(--text-medium)' }}>Tarifs</a>
            <a href="#faq" className="text-sm" style={{ color: 'var(--text-medium)' }}>FAQ</a>
          </div>
           <div className="flex justify-center items-center gap-6">
            <a href="#" aria-label="LinkedIn" style={{ color: 'var(--text-secondary)' }}><LinkedinIcon className="h-5 w-5" /></a>
            <a href="#" aria-label="Twitter" style={{ color: 'var(--text-secondary)' }}><TwitterIcon className="h-5 w-5" /></a>
            <a href="#" aria-label="Instagram" style={{ color: 'var(--text-secondary)' }}><InstagramIcon className="h-5 w-5" /></a>
          </div>
        </div>
        <div className="mt-8 pt-6 flex flex-col sm:flex-row justify-between items-center text-center text-sm gap-4" style={{ borderTop: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
          <p>&copy; {new Date().getFullYear()} Youtube Sniffer. Tous droits réservés.</p>
          <div className="flex gap-x-6 gap-y-2">
              <a href="#" style={{ color: 'var(--text-medium)' }}>Conditions d'Utilisation</a>
              <a href="#" style={{ color: 'var(--text-medium)' }}>Politique de Confidentialité</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
