import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import UseCases from './components/UseCases';
import Features from './components/Features';
import Automations from './components/Automations';
import FutureFeatures from './components/FutureFeatures';
import InteractiveDemo from './components/InteractiveDemo';
import Pricing from './components/Pricing';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import TrustedBy from './components/TrustedBy';
import Testimonials from './components/Testimonials';
import Modal from './components/Modal';
import { LoginForm, SignUpForm, PasswordRecoveryForm } from './components/AuthForms';

type ModalView = 'login' | 'signup' | 'recover' | null;

const App: React.FC = () => {
  const [modalView, setModalView] = useState<ModalView>(null);
  const [modalMessage, setModalMessage] = useState<string | null>(null);

  const openModal = (view: ModalView, message: string | null = null) => {
    setModalMessage(message);
    setModalView(view);
  };

  const closeModal = () => {
    setModalView(null);
    setModalMessage(null);
  };

  const handleLoginSuccess = () => {
    closeModal();
    // Ici, vous pouvez ajouter une logique de redirection ou de mise à jour de l'état de l'interface utilisateur
  };

  return (
    <div className="antialiased" style={{ backgroundColor: 'var(--background-light)', color: 'var(--text-dark)' }}>
      <Header openLoginModal={() => openModal('login')} openSignupModal={() => openModal('signup')} />
      <main>
        <Hero />
        <TrustedBy />
        <Features />
        <HowItWorks />
        <InteractiveDemo />
        <UseCases />
        <Automations />
        <FutureFeatures />
        <Testimonials />
        <Pricing setModalView={setModalView} setModalMessage={setModalMessage} />
        <FAQ />
      </main>
      <Footer />

      <Modal show={modalView !== null} onClose={closeModal}>
        {modalView === 'login' && <LoginForm message={modalMessage} onSwitch={setModalView} onLoginSuccess={handleLoginSuccess} />}
        {modalView === 'signup' && <SignUpForm onSwitch={setModalView} onLoginSuccess={handleLoginSuccess} />}
        {modalView === 'recover' && <PasswordRecoveryForm onSwitch={setModalView} />}
      </Modal>
    </div>
  );
};

export default App;
