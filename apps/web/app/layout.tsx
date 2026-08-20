import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import Footer from '../components/Footer';
import Nav from '../components/Nav';
import './globals.css';

export const metadata: Metadata = {
  title: {
    default: 'nstate',
    template: '%s — nstate',
  },
  description: 'Open-source, reproducible accountability for public spending.',
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <Nav />
        <main className="site-main">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
