'use client';

import { useRouter } from 'next/navigation';
import { Button } from '../components/ui/Button';
import Navbar from '../components/ui/Navbar';

export default function HomePage() {
  const router = useRouter();

  return (
    <div>
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen text-center">
        <h1 className="text-4xl font-bold mb-4">Supply Chain Alert System</h1>
        <p className="text-gray-600 mb-6">
          Manage shipments, detect risks, and analyze data in real-time.
        </p>
        <div className="flex gap-4">
          <Button onClick={() => router.push('/sign-in')}>Sign In</Button>
          <Button variant="outline" onClick={() => router.push('/sign-up')}>
            Sign Up
          </Button>
        </div>
      </div>
    </div>
  );
}
