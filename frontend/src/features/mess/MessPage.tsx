import { useState, type FormEvent } from 'react'
import { ApiError, api } from '../../api/client'
import { useAuth } from '../../auth/AuthContext'
import { Field, LoadState, Page, message, useResource } from '../shared'

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] as const
const meals = ['breakfast', 'lunch', 'dinner'] as const
type Menu = { id: number; week_start: string; menu: { days: Record<string, Record<string, string[]>> } }
type Draft = Record<string, Record<string, string>>
function emptyDraft(): Draft { return Object.fromEntries(days.map(day => [day, Object.fromEntries(meals.map(meal => [meal, '']))])) }
function draftFrom(menu: Menu | null) { const draft = emptyDraft(); if (menu) for (const day of days) for (const meal of meals) draft[day][meal] = menu.menu.days[day][meal].join('\n'); return draft }
export default function MessPage() {
  const { role } = useAuth(); const admin = role === 'ADMIN'
  const resource = useResource(async () => { try { return await api.get<Menu>('/mess/menu') } catch (err) { if (err instanceof ApiError && err.status === 404) return null; throw err } }, [])
  const [week, setWeek] = useState(new Date().toISOString().slice(0, 10)); const [draft, setDraft] = useState(emptyDraft); const [busy, setBusy] = useState(false); const [error, setError] = useState(''); const [success, setSuccess] = useState('')
  function beginEdit() { if (resource.data) { setDraft(draftFrom(resource.data)); setWeek(resource.data.week_start) } }
  async function submit(e: FormEvent) { e.preventDefault(); setBusy(true); setError(''); setSuccess(''); const menu = { days: Object.fromEntries(days.map(day => [day, Object.fromEntries(meals.map(meal => [meal, draft[day][meal].split('\n').map(item => item.trim()).filter(Boolean)]))])) }; try { await api.post('/mess/menu', { week_start: week, menu }); setSuccess('Weekly menu published.'); await resource.reload() } catch (err) { setError(message(err)) } finally { setBusy(false) } }
  return <Page title="Mess menu" intro={admin ? 'Publish the seven day menu. Enter one dish per line; publishing replaces the menu for that week.' : 'The latest published weekly menu.'}>
    {admin && <form className="feature-form menu-form" onSubmit={submit}><h3>{resource.data ? 'Publish or update a week' : 'Publish weekly menu'}</h3><Field label="Week start"><input type="date" required value={week} onChange={e => setWeek(e.target.value)} /></Field><div className="menu-grid">{days.map(day => <fieldset className="menu-day" key={day}><legend>{day}</legend>{meals.map(meal => <Field key={meal} label={meal[0].toUpperCase() + meal.slice(1)}><textarea required rows={2} placeholder="One dish per line" value={draft[day][meal]} onChange={e => setDraft(prev => ({ ...prev, [day]: { ...prev[day], [meal]: e.target.value } }))} /></Field>)}</fieldset>)}</div><button className="primary-button form-submit" disabled={busy}>{busy ? 'Publishing…' : 'Publish menu'}</button></form>}
    {error && <div className="state-error" role="alert">{error}</div>}{success && <div className="inline-success" role="status">{success}</div>}<LoadState loading={resource.loading} error={resource.error} empty={!resource.loading && !resource.error && !resource.data} onRetry={resource.reload} />
    {resource.data && <section className="published-menu"><div className="record-top"><div><span className="status-badge status-resolved">CURRENT MENU</span><h3>Week starting {resource.data.week_start}</h3></div>{admin && <button className="secondary-button" onClick={beginEdit}>Load this menu into editor</button>}</div><div className="menu-grid published-grid">{days.map(day => <article className="menu-day" key={day}><h4>{day}</h4>{meals.map(meal => <p key={meal}><strong>{meal}</strong><br />{resource.data!.menu.days[day][meal].join(', ')}</p>)}</article>)}</div></section>}
  </Page>
}
