import React from 'react';
import Hero from './Hero';
import Features from './Features';
import HowItWorks from './HowItWorks';
import Pricing from './Pricing';
import FAQ from './FAQ';
import Testimonials from './Testimonials';
import Footer from './Footer';

const Home: React.FC = () => {
    return (
        <>
            <Hero />
            <Features />
            <HowItWorks />
            <Pricing />
            <FAQ />
            <Testimonials />
            <Footer />
        </>
    );
};

export default Home;
