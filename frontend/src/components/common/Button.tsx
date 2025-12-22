import React from 'react';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: 'primary' | 'secondary';
};

export default function Button({ children, variant = 'primary', ...props }: ButtonProps) {
    return (
        <button {...props} className={`btn ${variant}`}>
            {children}
        </button>
    );
}
