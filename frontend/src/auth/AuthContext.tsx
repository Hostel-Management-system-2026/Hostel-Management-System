import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { api } from '../api/client'
import { tokenStore, type TokenPair } from '../api/tokenStore'
import { roleFromAccessToken, type Role } from './roles'

type Credentials = { username: string; password: string }
type AuthContextValue = {
  role: Role | null
  isAuthenticated: boolean
  signIn: (credentials: Credentials) => Promise<void>
  signOut: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

function currentRole(): Role | null {
  const access = tokenStore.getAccess()
  return access ? roleFromAccessToken(access) : null
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<Role | null>(currentRole)

  useEffect(() => {
    const expireSession = () => setRole(null)
    window.addEventListener('hms:auth-expired', expireSession)
    return () => window.removeEventListener('hms:auth-expired', expireSession)
  }, [])

  async function signIn(credentials: Credentials) {
    const tokens = await api.post<TokenPair>('/auth/login/', credentials, {
      authenticated: false,
      retryOn401: false,
    })
    const tokenRole = roleFromAccessToken(tokens.access)
    if (!tokenRole || !tokens.refresh) {
      tokenStore.clear()
      throw new Error('The server returned an invalid session. Please contact the project team.')
    }
    tokenStore.set(tokens)
    setRole(tokenRole)
  }

  function signOut() {
    tokenStore.clear()
    setRole(null)
  }

  const value = useMemo(
    () => ({ role, isAuthenticated: role !== null, signIn, signOut }),
    [role],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used inside AuthProvider')
  return value
}
