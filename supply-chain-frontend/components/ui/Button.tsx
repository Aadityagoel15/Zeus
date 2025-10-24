'use client';

import React from 'react';
import clsx from 'clsx';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'solid' | 'outline';
}

export function Button({ variant = 'solid', className, ...props }: ButtonProps) {
  return (
    <button
      className={clsx(
        'rounded-lg px-4 py-2 font-medium transition-colors',
        variant === 'solid'
          ? 'bg-blue-600 text-white hover:bg-blue-700'
          : 'border border-blue-600 text-blue-600 hover:bg-blue-50',
        className
      )}
      {...props}
    />
  );
}
