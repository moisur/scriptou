import React from 'react';

interface ModalProps {
  show: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
}

const Modal: React.FC<ModalProps> = ({ show, onClose, children, title }) => {
  if (!show) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
      <div className="relative p-5 border w-96 shadow-lg rounded-md" style={{ backgroundColor: 'var(--background-card)', borderColor: 'var(--border-color)' }}>
        <div className="flex justify-between items-center mb-4">
          {title && <h3 className="text-lg font-semibold" style={{ color: 'var(--text-main)' }}>{title}</h3>}
          <button onClick={onClose} className="text-2xl leading-none font-semibold" style={{ color: 'var(--text-secondary)' }}>&times;</button>
        </div>
        <div className="mt-2" style={{ color: 'var(--text-secondary)' }}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
