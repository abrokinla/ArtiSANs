import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/Navbar'
import { AuthProvider } from '@/context/AuthContext'

export const metadata: Metadata = {
  title: 'ArtiSANs NG - Connect with Trusted Local Artisans',
  description: 'Nigeria-first platform connecting clients with verified local artisans',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* DM Sans - Airbnb Cereal VF substitute */}
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet" />
      </head>
      <body className="font-sans">
        <AuthProvider>
          <Navbar />
          <main>{children}</main>
          <footer className="bg-white border-t border-gray-100 py-12 mt-16">
            <div className="container mx-auto px-4 text-center">
              <p className="text-secondary text-sm">&copy; 2026 ArtiSANs NG. All rights reserved.</p>
            </div>
          </footer>
        </AuthProvider>
      </body>
    </html>
  )
}
