
/**
 * API client for SSVproff backend.
 * 
 * This module provides typed API calls to the FastAPI backend,
 * including authentication and CRUD operations.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * Custom error class for API errors
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

/**
 * Make an authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Get token from localStorage if available
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  // Add authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  // Handle non-JSON responses
  const contentType = response.headers.get('content-type');
  const isJson = contentType?.includes('application/json');
  
  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`;
    let errorDetails;
    
    if (isJson) {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
      errorDetails = errorData;
    } else {
      errorMessage = await response.text();
    }
    
    throw new APIError(errorMessage, response.status, errorDetails);
  }
  
  // Handle 204 No Content
  if (response.status === 204) {
    return null as T;
  }
  
  return response.json();
}

// =============================================================================
// Types
// =============================================================================

export interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  is_completed?: boolean;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

// =============================================================================
// Authentication API
// =============================================================================

/**
 * Register a new user
 */
export async function register(data: RegisterData): Promise<User> {
  return apiRequest<User>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Login with email and password
 */
export async function login(data: LoginData): Promise<AuthTokens> {
  return apiRequest<AuthTokens>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Get current user information
 */
export async function getCurrentUser(): Promise<User> {
  return apiRequest<User>('/auth/me');
}

/**
 * Refresh access token
 */
export async function refreshToken(refreshToken: string): Promise<AuthTokens> {
  return apiRequest<AuthTokens>('/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
}

// =============================================================================
// Task API
// =============================================================================

/**
 * Get all tasks for the current user
 */
export async function getTasks(params?: {
  skip?: number;
  limit?: number;
  completed?: boolean;
}): Promise<Task[]> {
  const queryParams = new URLSearchParams();
  if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
  if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
  if (params?.completed !== undefined) queryParams.append('completed', params.completed.toString());
  
  const query = queryParams.toString();
  return apiRequest<Task[]>(`/tasks${query ? `?${query}` : ''}`);
}

/**
 * Get a specific task by ID
 */
export async function getTask(taskId: string): Promise<Task> {
  return apiRequest<Task>(`/tasks/${taskId}`);
}

/**
 * Create a new task
 */
export async function createTask(data: TaskCreate): Promise<Task> {
  return apiRequest<Task>('/tasks/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Update a task
 */
export async function updateTask(taskId: string, data: TaskUpdate): Promise<Task> {
  return apiRequest<Task>(`/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: string): Promise<void> {
  return apiRequest<void>(`/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

