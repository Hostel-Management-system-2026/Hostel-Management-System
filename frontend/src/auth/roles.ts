export const ROLES = ['STUDENT', 'WARDEN', 'ADMIN'] as const
export type Role = (typeof ROLES)[number]

export function roleFromAccessToken(access: string): Role | null {
  try {
    const payloadPart = access.split('.')[1]
    if (!payloadPart) return null
    const base64 = payloadPart.replace(/-/g, '+').replace(/_/g, '/')
      .padEnd(Math.ceil(payloadPart.length / 4) * 4, '=')
    const payload = JSON.parse(atob(base64)) as { role?: unknown }
    return typeof payload.role === 'string' && ROLES.includes(payload.role as Role)
      ? (payload.role as Role)
      : null
  } catch {
    return null
  }
}

export function roleLabel(role: Role): string {
  return role.charAt(0) + role.slice(1).toLowerCase()
}
