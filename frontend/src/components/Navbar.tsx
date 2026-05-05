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
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            ArtiSANs NG
          </Link>

          <div className="hidden md:flex space-x-8">
            {user?.role === 'artisan' ? (
              <Link href="/jobs" className="text-gray-700 hover:text-blue-600">
                Find Jobs
              </Link>
            ) : (
              <Link href="/search" className="text-gray-700 hover:text-blue-600">
                Find Artisans
              </Link>
            )}
            {isLoggedIn && (
              <Link href="/dashboard" className="text-gray-700 hover:text-blue-600">
                Dashboard
              </Link>
            )}
            {user?.role === 'client' && (
              <Link href="/jobs/post" className="text-gray-700 hover:text-blue-600">
                Post a Job
              </Link>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-blue-600 text-sm">
                  Dashboard
                </Link>
                <Link href="/profile/edit" className="text-gray-700 hover:text-blue-600 text-sm">
                  Profile
                </Link>
                <span className="text-sm text-gray-600">
                  {user?.username} ({user?.role})
                </span>
                <button
                  onClick={handleLogout}
                  className="bg-red-50 text-red-600 px-4 py-2 rounded hover:bg-red-100"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                href="/auth"
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
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
