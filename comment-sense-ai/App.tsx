import React from 'react';
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

const App: React.FC = () => {
  return (
    <div className="antialiased" style={{ backgroundColor: 'var(--background-light)', color: 'var(--text-dark)' }}>
      <Header />
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
        <Pricing />
        <FAQ />
      </main>
      <Footer />
    </div>
  );
};

export default App;
