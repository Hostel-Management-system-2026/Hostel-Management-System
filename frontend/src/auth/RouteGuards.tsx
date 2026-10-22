import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from './AuthContext'
import type { Role } from './roles'

export function RequireAuth() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace state={{ from: location }} />
}

export function RequireRole({ allowed }: { allowed: Role[] }) {
  const { role } = useAuth()
  return role && allowed.includes(role) ? <Outlet /> : <Navigate to="/forbidden" replace />
}
