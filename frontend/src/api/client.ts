import { tokenStore } from './tokenStore'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/, '')

type RequestOptions = RequestInit & { authenticated?: boolean; retryOn401?: boolean }
type TokenRefreshResponse = { access: string; refresh?: string }

export class ApiError extends Error {
  status: number
  details: unknown

  constructor(status: number, message: string, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

let refreshInFlight: Promise<boolean> | null = null

function errorMessage(payload: unknown, fallback: string): string {
  if (typeof payload === 'string') return payload
  if (payload && typeof payload === 'object') {
    const record = payload as Record<string, unknown>
    if (typeof record.detail === 'string') return record.detail
    const first = Object.values(record).flat()[0]
    if (typeof first === 'string') return first
  }
  return fallback
}

async function refreshAccessToken(): Promise<boolean> {
  const refresh = tokenStore.getRefresh()
  if (!refresh) return false
  if (refreshInFlight) return refreshInFlight

  refreshInFlight = (async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      })
      if (!response.ok) return false
      const tokens = (await response.json()) as TokenRefreshResponse
      if (!tokens.access) return false
      tokenStore.setAccess(tokens.access)
      if (tokens.refresh) tokenStore.set({ access: tokens.access, refresh: tokens.refresh })
      return true
    } catch {
      return false
    } finally {
      refreshInFlight = null
    }
  })()

  return refreshInFlight
}

async function request<T>(path: string, options: RequestOptions = {}, didRetry = false): Promise<T> {
  const { authenticated = true, retryOn401 = true, ...init } = options
  const headers = new Headers(init.headers)
  if (!(init.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  if (authenticated) {
    const access = tokenStore.getAccess()
    if (access) headers.set('Authorization', `Bearer ${access}`)
  }

  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`, {
      ...init,
      headers,
    })
  } catch {
    throw new ApiError(0, 'Could not reach the server. Check that the backend is running.')
  }

  if (response.status === 401 && authenticated && retryOn401 && !didRetry) {
    if (await refreshAccessToken()) return request<T>(path, options, true)
    tokenStore.clear()
    window.dispatchEvent(new Event('hms:auth-expired'))
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new ApiError(response.status, errorMessage(payload, `Request failed (${response.status}).`), payload)
  }
  if (response.status === 204) return undefined as T
  return (await response.json()) as T
}

export const api = {
  get: <T>(path: string) => request<T>(path, { method: 'GET' }),
  post: <T>(path: string, body: unknown, options?: RequestOptions) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(body), ...options }),
  patch: <T>(path: string, body: unknown) => request<T>(path, { method: 'PATCH', body: JSON.stringify(body) }),
  put: <T>(path: string, body: unknown) => request<T>(path, { method: 'PUT', body: JSON.stringify(body) }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
}

export type { RequestOptions }
