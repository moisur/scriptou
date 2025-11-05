import React, { useState, createContext, useContext } from 'react';
import LoginPage from '../components/LoginPage';
import SignupPage from '../components/SignupPage';
import Home from '../components/Home';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Modal from '../components/Modal'; // Import the Modal component

interface AuthContextType {
    isAuthenticated: boolean;
    login: () => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('user'));

    const login = () => {
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('user');
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

const App: React.FC = () => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);

  const openLoginModal = () => {
    setShowLoginModal(true);
    setShowSignupModal(false); // Close signup if open
  };

  const closeLoginModal = () => {
    setShowLoginModal(false);
  };

  const openSignupModal = () => {
    setShowSignupModal(true);
    setShowLoginModal(false); // Close login if open
  };

  const closeSignupModal = () => {
    setShowSignupModal(false);
  };

  return (
    <AuthProvider>
        <div className="antialiased" style={{ backgroundColor: 'var(--background-light)', color: 'var(--text-dark)' }}>
            <Header openLoginModal={openLoginModal} openSignupModal={openSignupModal} />
            <main>
                <Home /> {/* Home component is always rendered as the main content */}
            </main>
            <Footer />

            <Modal show={showLoginModal} onClose={closeLoginModal} title="Connexion">
                <LoginPage onClose={closeLoginModal} />
            </Modal>

            <Modal show={showSignupModal} onClose={closeSignupModal} title="S'inscrire">
                <SignupPage onClose={closeSignupModal} />
            </Modal>
        </div>
    </AuthProvider>
  );
};

export default App;