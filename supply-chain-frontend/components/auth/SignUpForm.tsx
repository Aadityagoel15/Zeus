'use client';

import { SignUp } from '@clerk/nextjs';
import AuthLayout from './AuthLayout';

export default function SignUpForm() {
  return (
    <AuthLayout title="Create Account 🚀" subtitle="Join our Supply Chain System">
      <SignUp path="/sign-up" routing="path" signInUrl="/sign-in" />
    </AuthLayout>
  );
}
