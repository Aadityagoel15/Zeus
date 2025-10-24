'use client';

import Link from 'next/link';
import { UserButton, SignedIn, SignedOut } from '@clerk/nextjs';

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-white shadow">
      <Link href="/" className="font-semibold text-xl text-blue-700">
        SupplyChain
      </Link>

      <div className="flex items-center gap-4">
        <SignedOut>
          <Link href="/sign-in" className="text-gray-700 hover:text-blue-600">
            Sign In
          </Link>
          <Link href="/sign-up" className="text-gray-700 hover:text-blue-600">
            Sign Up
          </Link>
        </SignedOut>

        <SignedIn>
          <UserButton afterSignOutUrl="/" />
        </SignedIn>
      </div>
    </nav>
  );
}
