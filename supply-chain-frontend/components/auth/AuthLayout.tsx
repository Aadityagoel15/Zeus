'use client';

import React from 'react';

interface AuthLayoutProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}

export default function AuthLayout({ title, subtitle, children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-md rounded-2xl bg-white shadow-lg p-8">
        <h1 className="text-2xl font-semibold mb-2 text-center">{title}</h1>
        {subtitle && <p className="text-gray-500 text-center mb-6">{subtitle}</p>}
        {children}
      </div>
    </div>
  );
}
