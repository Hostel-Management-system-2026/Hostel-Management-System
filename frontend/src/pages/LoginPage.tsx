import { useState, type FormEvent } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { useAuth } from '../auth/AuthContext'

export default function LoginPage() {
  const { isAuthenticated, signIn } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  if (isAuthenticated) return <Navigate to="/dashboard" replace />

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setBusy(true)
    try {
      await signIn({ username: username.trim(), password })
      const destination = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname
      navigate(destination || '/dashboard', { replace: true })
    } catch (cause) {
      setError(cause instanceof ApiError && cause.status === 401
        ? 'That username and password did not match.'
        : cause instanceof Error ? cause.message : 'Sign in failed. Please try again.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="login-screen">
      <section className="login-art" aria-label="Hostel Management System">
        <div className="brand brand-light"><span className="brand-mark">H</span><span>HMS</span></div>
        <div className="art-copy">
          <div className="eyebrow eyebrow-light">A BETTER WAY TO LIVE ON CAMPUS</div>
          <h1>Everything hostel life needs, in one place.</h1>
          <p>Simple, connected tools for students and the people who support them.</p>
        </div>
        <div className="art-footer"><span>HOSTEL MANAGEMENT SYSTEM</span><span>01 — 03</span></div>
        <div className="art-orbit orbit-one" /><div className="art-orbit orbit-two" />
      </section>
      <section className="login-panel">
        <div className="login-panel-inner">
          <div className="brand brand-dark"><span className="brand-mark">H</span><span>HMS</span></div>
          <div className="login-heading">
            <div className="eyebrow">YOUR CAMPUS, CONNECTED</div>
            <h2>Welcome back</h2>
            <p>Sign in with your hostel account to continue.</p>
          </div>
          <form className="login-form" onSubmit={submit}>
            <label htmlFor="username">Username</label>
            <input id="username" name="username" autoComplete="username" required value={username}
              onChange={(event) => setUsername(event.target.value)} placeholder="Enter your username" />
            <label htmlFor="password">Password</label>
            <input id="password" name="password" type="password" autoComplete="current-password"
              required value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Enter your password" />
            {error && <div className="form-error" role="alert">{error}</div>}
            <button className="primary-button login-button" type="submit" disabled={busy}>
              {busy ? 'Signing in…' : 'Sign in'} <span aria-hidden="true">→</span>
            </button>
          </form>
          <div className="login-help">Need access? Contact your hostel administrator.</div>
        </div>
      </section>
    </main>
  )
}
