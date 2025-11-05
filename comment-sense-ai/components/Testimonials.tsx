import React from 'react';
import { StarIcon } from './ui/icons';
import { testimonials } from '../constants';

type Testimonial = typeof testimonials[0];

const TestimonialCard: React.FC<Testimonial> = ({ name, role, text }) => (
    <div className="p-6 rounded-2xl border h-full flex flex-col transition-all duration-300 hover:-translate-y-1" style={{ backgroundColor: 'var(--background-card)', borderColor: 'var(--border-color)' }}>
        <div className="flex mb-4">
            {[...Array(5)].map((_, i) => <StarIcon key={i} className="h-5 w-5" style={{ color: 'var(--yellow-dark)', fill: 'var(--yellow-dark)' }} />)}
        </div>
        <p className="mb-5 flex-grow leading-relaxed" style={{ color: 'var(--text-medium)' }}>"{text}"</p>
        <div className="mt-auto">
            <p className="font-bold" style={{ color: 'var(--text-dark)' }}>{name}</p>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{role}</p>
        </div>
    </div>
);


const Testimonials: React.FC = () => {
  return (
    <section id="testimonials" className="py-20 md:py-28" style={{ backgroundColor: 'var(--background-light)' }}>
        <div className="container mx-auto px-6">
            <div className="text-center max-w-3xl mx-auto mb-16">
                <h2 className="text-3xl md:text-4xl font-bold tracking-tight" style={{ color: 'var(--text-dark)' }}>Apprécié par les Créateurs et les Analystes</h2>
                <p className="mt-4 text-lg" style={{ color: 'var(--text-medium)' }}>Ne nous croyez pas sur parole. Découvrez comment les professionnels tirent parti de notre plateforme pour obtenir un avantage concurrentiel.</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {testimonials.map((testimonial, index) => (
                    <TestimonialCard key={index} {...testimonial} />
                ))}
            </div>
        </div>
    </section>
  );
};

export default Testimonials;
