import { useMemo, useState, type FormEvent } from 'react'
import { useAuth } from '../../auth/AuthContext'
import { Field, LoadState, Page, message, useResource } from '../shared'
import { facilitiesApi, type Facility, type FacilityDraft } from './api'

const today = () => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 10)
}

const blankFacility: FacilityDraft = {
  name: '', description: '', location: '', capacity: 1, is_active: true,
}

export default function FacilitiesPage() {
  const { role } = useAuth()
  const isStudent = role === 'STUDENT'
  const isStaff = role === 'WARDEN' || role === 'ADMIN'
  const resource = useResource(
    () => isStudent ? facilitiesApi.listForStudents() : facilitiesApi.listForStaff(),
    [isStudent],
  )
  const [selectedId, setSelectedId] = useState('')
  const [bookingDate, setBookingDate] = useState(today)
  const availability = useResource(
    () => selectedId
      ? facilitiesApi.availability(Number(selectedId), bookingDate)
      : Promise.resolve(null),
    [selectedId, bookingDate],
  )
  const [startTime, setStartTime] = useState('')
  const [endTime, setEndTime] = useState('')
  const [facilityDraft, setFacilityDraft] = useState<FacilityDraft>(blankFacility)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const selectedFacility = useMemo(
    () => resource.data?.find((facility) => String(facility.id) === selectedId),
    [resource.data, selectedId],
  )

  async function bookSlot(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setBusy(true); setError(''); setNotice('')
    try {
      await facilitiesApi.book({
        facility: Number(selectedId), booking_date: bookingDate,
        start_time: `${startTime}:00`, end_time: `${endTime}:00`,
      })
      setNotice('Facility slot booked.')
      setStartTime(''); setEndTime('')
      await availability.reload()
    } catch (err) { setError(message(err)) } finally { setBusy(false) }
  }

  async function saveFacility(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setBusy(true); setError(''); setNotice('')
    try {
      if (editingId === null) await facilitiesApi.create(facilityDraft)
      else await facilitiesApi.update(editingId, facilityDraft)
      setFacilityDraft(blankFacility); setEditingId(null)
      setNotice(editingId === null ? 'Facility created.' : 'Facility updated.')
      await resource.reload()
    } catch (err) { setError(message(err)) } finally { setBusy(false) }
  }

  function editFacility(facility: Facility) {
    setEditingId(facility.id)
    setFacilityDraft({
      name: facility.name, description: facility.description, location: facility.location,
      capacity: facility.capacity, is_active: facility.is_active,
    })
    setError(''); setNotice('')
  }

  return <Page title="Facilities" intro={isStudent
    ? 'Check facility availability and reserve a time slot.'
    : 'Maintain facilities and review their availability.'}>
    {isStaff && <form className="feature-form compact-form" onSubmit={(event) => void saveFacility(event)}>
      <h3>{editingId === null ? 'Add a facility' : 'Edit facility'}</h3>
      <Field label="Name"><input required maxLength={100} value={facilityDraft.name} onChange={(event) => setFacilityDraft({ ...facilityDraft, name: event.target.value })} /></Field>
      <Field label="Location"><input required maxLength={150} value={facilityDraft.location} onChange={(event) => setFacilityDraft({ ...facilityDraft, location: event.target.value })} /></Field>
      <Field label="Description"><textarea rows={3} value={facilityDraft.description} onChange={(event) => setFacilityDraft({ ...facilityDraft, description: event.target.value })} /></Field>
      <Field label="Capacity"><input required type="number" min="1" step="1" value={facilityDraft.capacity} onChange={(event) => setFacilityDraft({ ...facilityDraft, capacity: Number(event.target.value) })} /></Field>
      <label className="check-field"><input type="checkbox" checked={facilityDraft.is_active} onChange={(event) => setFacilityDraft({ ...facilityDraft, is_active: event.target.checked })} /> Available for booking</label>
      <div className="action-row"><button className="primary-button form-submit" disabled={busy}>{busy ? 'Saving…' : editingId === null ? 'Add facility' : 'Save changes'}</button>
        {editingId !== null && <button type="button" className="secondary-button" onClick={() => { setEditingId(null); setFacilityDraft(blankFacility) }}>Cancel edit</button>}</div>
    </form>}

    {error && <div className="state-error" role="alert">{error}</div>}
    {notice && <div className="inline-success" role="status">{notice}</div>}
    {isStudent && <form className="feature-form" onSubmit={(event) => void bookSlot(event)}>
      <h3>Find and book a slot</h3>
      <div className="form-grid">
        <Field label="Facility"><select required value={selectedId} onChange={(event) => setSelectedId(event.target.value)}><option value="">Choose a facility</option>{resource.data?.map((facility) => <option key={facility.id} value={facility.id}>{facility.name} — {facility.location}</option>)}</select></Field>
        <Field label="Date"><input required type="date" min={today()} value={bookingDate} onChange={(event) => setBookingDate(event.target.value)} /></Field>
        <Field label="Start time"><input required type="time" value={startTime} onChange={(event) => setStartTime(event.target.value)} /></Field>
        <Field label="End time"><input required type="time" min={startTime || undefined} value={endTime} onChange={(event) => setEndTime(event.target.value)} /></Field>
      </div>
      {selectedFacility && <p className="field-hint">{selectedFacility.description || 'No description provided.'} Capacity: {selectedFacility.capacity}.</p>}
      <LoadState loading={resource.loading} error={resource.error} empty={!resource.loading && !resource.error && !resource.data?.length} onRetry={resource.reload} />
      <button className="primary-button form-submit" disabled={busy || resource.loading || !selectedId}>{busy ? 'Booking…' : 'Book this slot'}</button>
    </form>}

    {isStudent && selectedId && <section className="profile-card">
      <h3>Booked slots on {bookingDate}</h3>
      <LoadState loading={availability.loading} error={availability.error} empty={!availability.loading && !availability.error && !availability.data?.booked_slots.length} onRetry={availability.reload} />
      {!!availability.data?.booked_slots.length && <div className="table-wrap"><table><thead><tr><th>Time</th><th>Facility</th><th>Status</th></tr></thead><tbody>{availability.data.booked_slots.map((booking) => <tr key={booking.id}><td>{booking.start_time.slice(0, 5)}–{booking.end_time.slice(0, 5)}</td><td>{booking.facility_name}</td><td><span className="status-badge status-resolved">{booking.status}</span></td></tr>)}</tbody></table></div>}
    </section>}

    {isStaff && <section className="workspace-section">
      <div className="section-heading"><div><div className="eyebrow">FACILITY CATALOG</div><h3>Current facilities</h3></div></div>
      <LoadState loading={resource.loading} error={resource.error} empty={!resource.loading && !resource.error && !resource.data?.length} onRetry={resource.reload} />
      {!!resource.data?.length && <div className="table-wrap"><table><thead><tr><th>Facility</th><th>Location</th><th>Capacity</th><th>Status</th><th>Action</th></tr></thead><tbody>{resource.data.map((facility) => <tr key={facility.id}><td>{facility.name}<small>{facility.description}</small></td><td>{facility.location}</td><td>{facility.capacity}</td><td><span className={`status-badge ${facility.is_active ? 'status-resolved' : 'status-open'}`}>{facility.is_active ? 'ACTIVE' : 'INACTIVE'}</span></td><td><button type="button" className="secondary-button" onClick={() => editFacility(facility)}>Edit</button></td></tr>)}</tbody></table></div>}
    </section>}
  </Page>
}
