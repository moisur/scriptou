import React from 'react';

interface AuthFormProps {
  onSwitch: (view: 'login' | 'signup' | 'recover') => void;
  onLoginSuccess?: () => void;
}

const GoogleIcon: React.FC = () => (
    <svg className="h-5 w-5 mr-3" viewBox="0 0 24 24">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"></path>
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
    </svg>
);

const OrSeparator: React.FC = () => (
    <div className="relative my-6">
        <div className="absolute inset-0 flex items-center" aria-hidden="true">
            <div className="w-full border-t border-gray-300" />
        </div>
        <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">OU</span>
        </div>
    </div>
);


export const LoginForm: React.FC<{ message?: string | null; onSwitch: (view: 'signup' | 'recover') => void, onLoginSuccess: () => void; }> = ({ message, onSwitch, onLoginSuccess }) => {
  return (
    <div>
      {message && (
        <div className="text-center font-semibold p-3 rounded-md mb-6" style={{ backgroundColor: 'rgba(0, 158, 250, 0.1)', color: '#009EFA' }}>
          <p>{message}</p>
        </div>
      )}
      <h2 className="text-2xl font-bold text-brand-dark text-center mb-2">Connexion</h2>
      <p className="text-center text-gray-600 mb-6">Heureux de vous revoir !</p>
      
      <button 
        type="button"
        onClick={onLoginSuccess}
        className="w-full flex items-center justify-center py-2.5 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-blue"
      >
          <GoogleIcon />
          Continuer avec Google
      </button>

      <OrSeparator />

      <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); onLoginSuccess(); }}>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">Adresse e-mail</label>
          <input type="email" name="email" id="email" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#009EFA] focus:border-[#009EFA] sm:text-sm" placeholder="vous@exemple.com" />
        </div>
        <div>
          <div className="flex justify-between">
            <label htmlFor="password"  className="block text-sm font-medium text-gray-700">Mot de passe</label>
            <button type="button" onClick={() => onSwitch('recover')} className="text-sm hover:underline" style={{ color: '#009EFA' }}>Mot de passe oublié ?</button>
          </div>
          <input type="password" name="password" id="password" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#009EFA] focus:border-[#009EFA] sm:text-sm" placeholder="********" />
        </div>
        <button type="submit" className="w-full text-white font-bold py-3 px-4 rounded-lg shadow-sm transition-transform transform hover:scale-105" style={{ backgroundColor: '#009EFA' }}>
          Connexion
        </button>
      </form>
      <p className="mt-6 text-center text-sm text-gray-600">
        Pas encore de compte ?{' '}
        <button onClick={() => onSwitch('signup')} className="font-medium hover:underline" style={{ color: '#009EFA' }}>
          S'inscrire
        </button>
      </p>
    </div>
  );
};

export const SignUpForm: React.FC<{ onSwitch: (view: 'login') => void, onLoginSuccess: () => void; }> = ({ onSwitch, onLoginSuccess }) => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-brand-dark text-center mb-2">Créer un compte</h2>
      <p className="text-center text-gray-600 mb-6">Rejoignez-nous et analysez en quelques clics.</p>

       <button 
        type="button"
        onClick={onLoginSuccess}
        className="w-full flex items-center justify-center py-2.5 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-blue"
      >
          <GoogleIcon />
          Continuer avec Google
      </button>

      <OrSeparator />

      <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); onLoginSuccess(); }}>
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">Nom complet</label>
          <input type="text" name="name" id="name" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm" placeholder="Votre Nom" />
        </div>
        <div>
          <label htmlFor="signup-email" className="block text-sm font-medium text-gray-700">Adresse e-mail</label>
          <input type="email" name="signup-email" id="signup-email" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm" placeholder="vous@exemple.com" />
        </div>
        <div>
          <label htmlFor="signup-password"  className="block text-sm font-medium text-gray-700">Mot de passe</label>
          <input type="password" name="signup-password" id="signup-password" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm" placeholder="Créez un mot de passe sécurisé" />
        </div>
        <div>
          <label htmlFor="confirm-password"  className="block text-sm font-medium text-gray-700">Confirmez le mot de passe</label>
          <input type="password" name="confirm-password" id="confirm-password" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm" placeholder="Retapez votre mot de passe" />
        </div>
        <button type="submit" className="w-full text-white font-bold py-3 px-4 rounded-lg shadow-sm transition-transform transform hover:scale-105" style={{ backgroundColor: '#009EFA' }}>
          S'inscrire
        </button>
      </form>
      <p className="mt-6 text-center text-sm text-gray-600">
        Vous avez déjà un compte ?{' '}
        <button onClick={() => onSwitch('login')} className="font-medium hover:underline" style={{ color: '#009EFA' }}>
          Se connecter
        </button>
      </p>
    </div>
  );
};

export const PasswordRecoveryForm: React.FC<{ onSwitch: (view: 'login') => void }> = ({ onSwitch }) => {
  return (
    <div>
      <h2 className="text-2xl font-bold text-brand-dark text-center mb-2">Récupérer le mot de passe</h2>
      <p className="text-center text-gray-600 mb-6">Entrez votre email pour recevoir un lien de réinitialisation.</p>
      <form className="space-y-4">
        <div>
          <label htmlFor="recover-email" className="block text-sm font-medium text-gray-700">Adresse e-mail</label>
          <input type="email" name="recover-email" id="recover-email" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm" placeholder="vous@exemple.com" />
        </div>
        <button type="submit" className="w-full text-white font-bold py-3 px-4 rounded-lg shadow-sm transition-transform transform hover:scale-105" style={{ backgroundColor: '#009EFA' }}>
          Envoyer le lien de récupération
        </button>
      </form>
      <p className="mt-6 text-center text-sm text-gray-600">
        Vous vous souvenez de votre mot de passe ?{' '}
        <button onClick={() => onSwitch('login')} className="font-medium hover:underline" style={{ color: '#009EFA' }}>
          Retour à la connexion
        </button>
      </p>
    </div>
  );
};