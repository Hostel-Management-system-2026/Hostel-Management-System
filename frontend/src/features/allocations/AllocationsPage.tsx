import { useState, type FormEvent } from 'react'
import { api } from '../../api/client'
import { Field, LoadState, Page, dateLabel, message, useResource } from '../shared'

type Allocation = { id: number; student_id: number; room_id: number; student_username: string; room_number: string; allocated_at: string; released_at: string | null }
type Room = { id: number; room_number: string; capacity: number; is_available: boolean; occupied: number; available_beds: number }
type StudentProfile = { user_id: string; student_number: string; full_name: string }
export default function AllocationsPage() {
  const resource = useResource(() => api.get<Allocation[]>('/allocations/'), [])
  const rooms = useResource(() => api.get<Room[]>('/rooms/'), [])
  const students = useResource(() => api.get<StudentProfile[]>('/profiles'), [])
  const [student, setStudent] = useState(''); const [room, setRoom] = useState(''); const [busy, setBusy] = useState(false); const [error, setError] = useState('')
  async function submit(e: FormEvent) { e.preventDefault(); setBusy(true); setError(''); try { await api.post('/allocations/', { student_id: Number(student), room_id: Number(room) }); setStudent(''); setRoom(''); await Promise.all([resource.reload(), rooms.reload()]) } catch (err) { setError(message(err)) } finally { setBusy(false) } }
  async function release(item: Allocation) { setError(''); try { await api.patch(`/allocations/${item.id}/release`, {}); await Promise.all([resource.reload(), rooms.reload()]) } catch (err) { setError(message(err)) } }
  return <Page title="Room allocations" intro="Assign students to rooms with available capacity and release rooms when they move out.">
    <form className="feature-form compact-form" onSubmit={submit}><h3>Create allocation</h3><Field label="Student account ID"><input required type="number" min="1" step="1" list="student-account-options" value={student} onChange={e => setStudent(e.target.value)} /><datalist id="student-account-options">{students.data?.map(profile => <option key={profile.user_id} value={profile.user_id}>{profile.full_name} · {profile.student_number}</option>)}</datalist></Field><Field label="Available room"><select required value={room} onChange={e => setRoom(e.target.value)}><option value="">Choose a room</option>{rooms.data?.filter(r => r.is_available && r.available_beds > 0).map(r => <option key={r.id} value={r.id}>{r.room_number} · {r.available_beds} bed{r.available_beds === 1 ? '' : 's'} free (ID {r.id})</option>)}</select></Field><LoadState loading={rooms.loading} error={rooms.error} empty={!rooms.loading && !rooms.error && !rooms.data?.some(r => r.is_available && r.available_beds > 0)} onRetry={rooms.reload} /><button className="primary-button form-submit" disabled={busy || rooms.loading || !rooms.data?.some(r => r.is_available && r.available_beds > 0)}>{busy ? 'Assigning…' : 'Assign room'}</button></form>
    {error && <div className="state-error" role="alert">{error}</div>}<LoadState loading={resource.loading} error={resource.error} empty={!resource.loading && !resource.error && !resource.data?.length} onRetry={resource.reload} />
    {!!resource.data?.length && <div className="table-wrap"><table><thead><tr><th>Student</th><th>Room</th><th>Assigned</th><th>Status</th><th>Action</th></tr></thead><tbody>{resource.data.map(item => <tr key={item.id}><td>{item.student_username} <small>Account {item.student_id}</small></td><td>{item.room_number} <small>Room ID {item.room_id}</small></td><td>{dateLabel(item.allocated_at)}</td><td><span className={`status-badge ${item.released_at ? 'status-open' : 'status-resolved'}`}>{item.released_at ? 'RELEASED' : 'ACTIVE'}</span></td><td>{!item.released_at && <button className="secondary-button danger-button" onClick={() => void release(item)}>Release</button>}</td></tr>)}</tbody></table></div>}
  </Page>
}
