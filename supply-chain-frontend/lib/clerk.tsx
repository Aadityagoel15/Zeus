import { ClerkProvider } from "@clerk/nextjs";
import { ReactNode } from "react";

export const clerkConfig = {
  publishableKey: process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!,
};

export const withClerkProvider = (children: ReactNode) => (
  <ClerkProvider publishableKey={clerkConfig.publishableKey}>
    {children}
  </ClerkProvider>
);
