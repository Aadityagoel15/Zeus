'use client';

import { SignIn } from '@clerk/nextjs';
import AuthLayout from './AuthLayout';

export default function SignInForm() {
  return (
    <AuthLayout title="Welcome Back 👋" subtitle="Sign in to continue">
      <SignIn path="/sign-in" routing="path" signUpUrl="/sign-up" />
    </AuthLayout>
  );
}
