'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role?: string;
}

interface AuthContextType {
  isLoggedIn: boolean;
  user: User | null;
  token: string | null;
  login: (token: string, refresh: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Check auth state on mount and listen for storage changes
    const checkAuth = () => {
      const storedToken = localStorage.getItem('token');
      const userStr = localStorage.getItem('user');
      if (storedToken && userStr) {
        setIsLoggedIn(true);
        setToken(storedToken);
        try {
          setUser(JSON.parse(userStr));
        } catch {
          setUser(null);
        }
      } else {
        setIsLoggedIn(false);
        setToken(null);
        setUser(null);
      }
    };

    checkAuth();

    // Listen for storage events (cross-tab sync) and custom auth events
    const handleStorageChange = () => checkAuth();
    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('authChange', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('authChange', handleStorageChange);
    };
  }, []);

  const login = (token: string, refresh: string, user: User) => {
    localStorage.setItem('token', token);
    localStorage.setItem('refresh', refresh);
    localStorage.setItem('user', JSON.stringify(user));
    setIsLoggedIn(true);
    setToken(token);
    setUser(user);
    // Dispatch custom event to notify other components
    window.dispatchEvent(new Event('authChange'));
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    localStorage.removeItem('user');
    setIsLoggedIn(false);
    setToken(null);
    setUser(null);
    // Dispatch custom event
    window.dispatchEvent(new Event('authChange'));
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
