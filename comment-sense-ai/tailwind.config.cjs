/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}", // Ajout du dossier components
  ],
  theme: {
    extend: {
      colors: {
        'brand-blue': '#007AFF', // Une couleur bleue vive et moderne
        'brand-dark': '#1a202c', // Un gris foncé pour le texte
        'primary-color': '#007AFF', // Couleur primaire pour les boutons et icônes
      },
    },
  },
  plugins: [],
}
