
/**
 * Authentication context provider.
 * 
 * This context manages authentication state across the application,
 * providing login, logout, and user information.
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/router';
import { login as apiLogin, register as apiRegister, getCurrentUser } from '../lib/api';
import { storeTokens, clearTokens, isAuthenticated } from '../lib/auth';
import type { User, LoginData, RegisterData } from '../lib/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Authentication provider component
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Load user on mount if authenticated
  useEffect(() => {
    const loadUser = async () => {
      if (isAuthenticated()) {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
        } catch (err) {
          console.error('Failed to load user:', err);
          clearTokens();
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  /**
   * Login user with email and password
   */
  const login = async (data: LoginData) => {
    setError(null);
    setLoading(true);

    try {
      const tokens = await apiLogin(data);
      storeTokens(tokens.access_token, tokens.refresh_token);

      const userData = await getCurrentUser();
      setUser(userData);

      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Register a new user
   */
  const register = async (data: RegisterData) => {
    setError(null);
    setLoading(true);

    try {
      await apiRegister(data);
      
      // Auto-login after registration
      await login({
        email: data.email,
        password: data.password,
      });
    } catch (err: any) {
      setError(err.message || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout user and clear tokens
   */
  const logout = () => {
    clearTokens();
    setUser(null);
    router.push('/login');
  };

  const value: AuthContextType = {
    user,
    loading,
    error,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access authentication context
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

