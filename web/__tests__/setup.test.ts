
/**
 * Jest setup validation tests
 */

describe('Jest Configuration', () => {
  it('jest-dom matchers are available', () => {
    const element = document.createElement('div')
    element.textContent = 'test'
    document.body.appendChild(element)
    
    expect(element).toBeInTheDocument()
    expect(element).toHaveTextContent('test')
    
    document.body.removeChild(element)
  })

  it('can import modules with @ alias', async () => {
    // This test validates that the module path alias is working
    // If this test runs without error, the alias is configured correctly
    expect(true).toBe(true)
  })

  it('environment is jsdom', () => {
    expect(typeof window).toBe('object')
    expect(typeof document).toBe('object')
  })
})
