'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export default function Navbar() {
  const { isLoggedIn, user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <nav className="navbar sticky top-0 bg-white border-b border-gray-100 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link href="/" className="text-2xl font-semibold text-text-primary tracking-tight">
            ArtiSANs<span className="text-rausch">.</span>NG
          </Link>

          {/* Center Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {user?.role === 'artisan' ? (
              <Link href="/jobs" className="text-text-secondary hover:text-text-primary transition-colors text-sm font-medium">
                Find Jobs
              </Link>
            ) : (
              <Link href="/search" className="text-text-secondary hover:text-text-primary transition-colors text-sm font-medium">
                Find Artisans
              </Link>
            )}
            {isLoggedIn && (
              <Link href="/dashboard" className="text-text-secondary hover:text-text-primary transition-colors text-sm font-medium">
                Dashboard
              </Link>
            )}
            {user?.role === 'client' && (
              <Link href="/jobs/post" className="text-text-secondary hover:text-text-primary transition-colors text-sm font-medium">
                Post a Job
              </Link>
            )}
          </div>

          {/* Right Side - Auth */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <>
                <Link href="/dashboard" className="text-text-secondary hover:text-text-primary text-sm font-medium hidden sm:block">
                  Dashboard
                </Link>
                <Link href="/profile/edit" className="text-text-secondary hover:text-text-primary text-sm font-medium hidden sm:block">
                  Profile
                </Link>
                <span className="text-sm text-text-secondary hidden sm:block">
                  {user?.username}
                </span>
                <button
                  onClick={handleLogout}
                  className="text-text-secondary hover:text-rausch text-sm font-medium transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                href="/auth"
                className="bg-text-primary text-white px-6 py-2.5 rounded-lg hover:bg-rausch transition-all text-sm font-medium"
              >
                Login / Register
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
