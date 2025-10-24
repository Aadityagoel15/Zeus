import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const metadata = {
  title: 'Zeus: AI Supply Chain Dashboard and Analytics',
  description: 'AI-powered shipment analytics and disruption insights',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="font-sans">{children}</body>
      </html>
    </ClerkProvider>
  );
}
