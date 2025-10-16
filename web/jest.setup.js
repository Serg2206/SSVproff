
/**
 * Jest setup file
 * Runs before each test file
 */

// Add custom jest matchers from jest-dom
import '@testing-library/jest-dom'

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
    back: jest.fn(),
    pathname: '/',
    query: {},
    asPath: '/',
  })),
}))

// Mock Next.js navigation (App Router)
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
    back: jest.fn(),
  })),
  usePathname: jest.fn(() => '/'),
  useSearchParams: jest.fn(() => new URLSearchParams()),
}))

// Global test utilities
global.fetch = jest.fn()

// Reset mocks after each test
afterEach(() => {
  jest.clearAllMocks()
})
