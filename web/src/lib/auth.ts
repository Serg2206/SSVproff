
/**
 * Authentication utilities.
 * 
 * This module provides token storage and management utilities
 * for client-side authentication.
 */

const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

/**
 * Store authentication tokens in localStorage
 */
export function storeTokens(accessToken: string, refreshToken?: string): void {
  if (typeof window === 'undefined') return;
  
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
}

/**
 * Get access token from localStorage
 */
export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

/**
 * Get refresh token from localStorage
 */
export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

/**
 * Clear all authentication tokens
 */
export function clearTokens(): void {
  if (typeof window === 'undefined') return;
  
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

/**
 * Check if user is authenticated (has access token)
 */
export function isAuthenticated(): boolean {
  return getAccessToken() !== null;
}

