'use client';

import { useEffect } from 'react';
import { useStore } from '@/lib/store';
import LoginForm from '@/components/LoginForm';
import Dashboard from '@/components/Dashboard';

export default function Home() {
  const { isAuthenticated } = useStore();

  return (
    <main>
      {isAuthenticated ? <Dashboard /> : <LoginForm />}
    </main>
  );
}
