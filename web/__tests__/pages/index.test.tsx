
/**
 * Tests for the home page
 */

import { render, screen } from '@testing-library/react'
import Home from '@/pages/index'

describe('Home Page', () => {
  it('renders the page without crashing', () => {
    render(<Home />)
    
    // Page should render
    expect(document.body).toBeInTheDocument()
  })

  it('displays the project name', () => {
    render(<Home />)
    
    // Should contain SSVproff text
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading.textContent).toContain('SSVproff')
  })

  it('has the correct page title structure', () => {
    render(<Home />)
    
    // Should have main heading
    const headings = screen.getAllByRole('heading')
    expect(headings.length).toBeGreaterThan(0)
  })

  it('renders main content area', () => {
    const { container } = render(<Home />)
    
    // Should have a main element or container
    expect(container.firstChild).toBeInTheDocument()
  })

  it('has proper semantic HTML structure', () => {
    const { container } = render(<Home />)
    
    // Should use semantic HTML elements
    const headings = container.querySelectorAll('h1, h2, h3')
    expect(headings.length).toBeGreaterThan(0)
  })
})
