import { useCallback, useEffect, useState, type ReactNode } from 'react'
import { ApiError } from '../api/client'

export function useResource<T>(load: () => Promise<T>, dependencies: unknown[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const reload = useCallback(async () => {
    setLoading(true); setError('')
    try { setData(await load()) } catch (e) { setError(message(e)) } finally { setLoading(false) }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencies)
  useEffect(() => { void reload() }, [reload])
  return { data, setData, loading, error, reload }
}

export function message(error: unknown) {
  if (error instanceof ApiError) return error.message
  return error instanceof Error ? error.message : 'Something went wrong. Please try again.'
}

export function Page({ title, intro, children }: { title: string; intro?: string; children: ReactNode }) {
  return <section className="feature-page"><div className="eyebrow">HMS WORKSPACE</div><h2>{title}</h2>{intro && <p className="feature-intro">{intro}</p>}{children}</section>
}

export function LoadState({ loading, error, empty, onRetry }: { loading: boolean; error: string; empty?: boolean; onRetry?: () => void }) {
  if (loading) return <p className="state-message" role="status">Loading…</p>
  if (error) return <div className="state-error" role="alert"><span>{error}</span>{onRetry && <button className="secondary-button" onClick={onRetry}>Try again</button>}</div>
  if (empty) return <p className="state-message">Nothing here yet.</p>
  return null
}

export function Notice({ children }: { children: ReactNode }) { return <div className="inline-success" role="status">{children}</div> }
export function Field({ label, children }: { label: string; children: ReactNode }) { return <label className="form-field"><span>{label}</span>{children}</label> }
export function dateLabel(value?: string | null) { return value ? new Date(value).toLocaleString() : '—' }
