import { useState, type FormEvent } from 'react'
import { api } from '../../api/client'
import { useAuth } from '../../auth/AuthContext'
import { Field, LoadState, Page, dateLabel, message, useResource } from '../shared'

type LeaveRequest = { id: number; student_id: string; start_date: string; end_date: string; reason: string; status: 'PENDING' | 'APPROVED' | 'REJECTED'; submitted_at: string }
export default function LeavePage() {
  const { role } = useAuth(); const resource = useResource(() => api.get<LeaveRequest[]>('/leave'), [])
  const [start, setStart] = useState(''); const [end, setEnd] = useState(''); const [reason, setReason] = useState(''); const [busy, setBusy] = useState(false); const [error, setError] = useState('')
  async function submit(e: FormEvent) { e.preventDefault(); setBusy(true); setError(''); try { await api.post('/leave', { start_date: start, end_date: end, reason }); setStart(''); setEnd(''); setReason(''); await resource.reload() } catch (err) { setError(message(err)) } finally { setBusy(false) } }
  async function decide(item: LeaveRequest, decision: 'approve' | 'reject') { setError(''); try { const updated = await api.patch<LeaveRequest>(`/leave/${item.id}/decision`, { decision }); resource.setData(rows => rows?.map(row => row.id === updated.id ? updated : row) ?? null) } catch (err) { setError(message(err)) } }
  return <Page title="Leave requests" intro={role === 'STUDENT' ? 'Request an outpass and track its decision.' : 'Review student outpass requests and record a decision.'}>
    {role === 'STUDENT' && <form className="feature-form" onSubmit={submit}><h3>New leave request</h3><div className="form-grid"><Field label="Start date"><input type="date" required value={start} onChange={e => setStart(e.target.value)} /></Field><Field label="End date"><input type="date" required min={start || undefined} value={end} onChange={e => setEnd(e.target.value)} /></Field></div><Field label="Reason"><textarea required rows={4} maxLength={2000} value={reason} onChange={e => setReason(e.target.value)} /></Field><button className="primary-button form-submit" disabled={busy}>{busy ? 'Submitting…' : 'Submit request'}</button></form>}
    {error && <div className="state-error" role="alert">{error}</div>}<LoadState loading={resource.loading} error={resource.error} empty={!resource.loading && !resource.error && !resource.data?.length} onRetry={resource.reload} />
    <div className="record-list">{resource.data?.map(item => <article className="record-card" key={item.id}><div className="record-top"><div><span className={`status-badge status-${item.status.toLowerCase()}`}>{item.status}</span><h3>{item.start_date} → {item.end_date}</h3></div><time>Submitted {dateLabel(item.submitted_at)}</time></div><p>{item.reason}</p>{role === 'WARDEN' && item.status === 'PENDING' && <div className="action-row"><button className="primary-button small-button" onClick={() => void decide(item, 'approve')}>Approve</button><button className="secondary-button danger-button" onClick={() => void decide(item, 'reject')}>Reject</button></div>}</article>)}</div>
  </Page>
}
