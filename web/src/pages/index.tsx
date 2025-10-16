/**
 * Home page component for SSVproff Web.
 * 
 * This is the main landing page of the application.
 */
import React from 'react';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';

export default function Home() {
  const { user } = useAuth();
  const router = useRouter();

  // Redirect to dashboard if already logged in
  React.useEffect(() => {
    if (user) {
      router.push('/dashboard');
    }
  }, [user, router]);

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: '100vh',
      padding: '20px',
      textAlign: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white'
    }}>
      <h1 style={{ fontSize: '48px', marginBottom: '16px', fontWeight: 'bold' }}>
        Welcome to SSVproff
      </h1>
      <p style={{ fontSize: '20px', marginBottom: '40px', maxWidth: '600px', lineHeight: '1.6' }}>
        A modern monorepo with FastAPI backend and Next.js frontend,
        featuring authentication, task management, and comprehensive documentation.
      </p>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '40px' }}>
        <Link 
          href="/login"
          style={{
            padding: '12px 32px',
            background: 'white',
            color: '#667eea',
            borderRadius: '8px',
            fontWeight: '600',
            fontSize: '16px',
            textDecoration: 'none'
          }}
        >
          Login
        </Link>
        <Link 
          href="/register"
          style={{
            padding: '12px 32px',
            background: 'rgba(255, 255, 255, 0.2)',
            color: 'white',
            borderRadius: '8px',
            fontWeight: '600',
            fontSize: '16px',
            border: '2px solid white',
            textDecoration: 'none'
          }}
        >
          Register
        </Link>
      </div>
      <div style={{ marginTop: '20px', fontSize: '14px', opacity: 0.9 }}>
        <p style={{ marginBottom: '8px' }}>Quick Links:</p>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', justifyContent: 'center' }}>
          <a href="https://github.com/Serg2206/SSVproff" style={{ color: 'white' }}>GitHub Repository</a>
          <a href="/docs/" style={{ color: 'white' }}>Documentation</a>
          <a href="http://localhost:8000/docs" style={{ color: 'white' }}>API Docs</a>
        </div>
      </div>
    </div>
  );
}
