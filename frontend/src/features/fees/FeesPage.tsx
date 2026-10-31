import { useState, type FormEvent } from 'react'
import { useAuth } from '../../auth/AuthContext'
import { Field, LoadState, Page, dateLabel, message, useResource } from '../shared'
import { feesApi, type StaffFeeRecord } from './api'

const money = (value: string) => new Intl.NumberFormat('en-IN', {
  style: 'currency', currency: 'INR', minimumFractionDigits: 2,
}).format(Number(value))

function FeeStatus({ status }: { status: string }) {
  return <span className={`status-badge status-${status === 'PAID' ? 'resolved' : status === 'PARTIAL' ? 'pending' : 'open'}`}>{status}</span>
}

export default function FeesPage() {
  const { role } = useAuth()
  const isAdmin = role === 'ADMIN'
  const mine = useResource(() => isAdmin ? Promise.resolve(null) : feesApi.mine(), [isAdmin])
  const records = useResource(() => isAdmin ? feesApi.records() : Promise.resolve([] as StaffFeeRecord[]), [isAdmin])
  const students = useResource(() => isAdmin ? feesApi.students() : Promise.resolve([]), [isAdmin])
  const [amount, setAmount] = useState('')
  const [paymentMode, setPaymentMode] = useState('UPI')
  const [studentId, setStudentId] = useState('')
  const [totalAmount, setTotalAmount] = useState('')
  const [totals, setTotals] = useState<Record<number, string>>({})
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  async function recordPayment(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(''); setNotice('')
    try {
      const updated = await feesApi.pay(amount, paymentMode)
      mine.setData(updated); setAmount(''); setNotice('Payment recorded successfully.')
    } catch (err) { setError(message(err)) } finally { setBusy(false) }
  }

  async function createRecord(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(''); setNotice('')
    try {
      await feesApi.createRecord(Number(studentId), totalAmount)
      setStudentId(''); setTotalAmount(''); setNotice('Fee record created.')
      await records.reload()
    } catch (err) { setError(message(err)) } finally { setBusy(false) }
  }

  async function updateTotal(record: StaffFeeRecord) {
    const value = totals[record.id] ?? record.total_amount
    setBusy(true); setError(''); setNotice('')
    try {
      await feesApi.updateTotal(record.id, value)
      setNotice(`Fee record for ${record.student_username} updated.`)
      await records.reload()
    } catch (err) { setError(message(err)) } finally { setBusy(false) }
  }

  return <Page title="Fees" intro={isAdmin
    ? 'Create student fee records and maintain the amount due.'
    : 'Review your balance and record a payment.'}>
    {error && <div className="state-error" role="alert">{error}</div>}
    {notice && <div className="inline-success" role="status">{notice}</div>}

    {!isAdmin && <>
      <LoadState loading={mine.loading} error={mine.error} empty={!mine.loading && !mine.error && !mine.data} onRetry={mine.reload} />
      {mine.data && <>
        <section className="profile-card fee-summary">
          <div className="record-top"><div><div className="eyebrow">CURRENT STATEMENT</div><h3>Fee balance</h3></div><FeeStatus status={mine.data.fee_status} /></div>
          <dl><div><dt>Total fee</dt><dd>{money(mine.data.total_amount)}</dd></div><div><dt>Paid</dt><dd>{money(mine.data.amount_paid)}</dd></div><div><dt>Balance due</dt><dd>{money(mine.data.balance_due)}</dd></div></dl>
        </section>
        {Number(mine.data.balance_due) > 0 && <form className="feature-form compact-form" onSubmit={(event) => void recordPayment(event)}>
          <h3>Record a payment</h3>
          <Field label={`Amount (up to ${money(mine.data.balance_due)})`}><input required type="number" min="0.01" max={mine.data.balance_due} step="0.01" value={amount} onChange={(event) => setAmount(event.target.value)} /></Field>
          <Field label="Payment method"><select value={paymentMode} onChange={(event) => setPaymentMode(event.target.value)}><option value="UPI">UPI</option><option value="CARD">Card</option><option value="ONLINE_BANKING">Online banking</option><option value="CASH">Cash</option></select></Field>
          <button className="primary-button form-submit" disabled={busy}>{busy ? 'Recording…' : 'Record payment'}</button>
        </form>}
        {!!mine.data.payments?.length && <section className="profile-card"><h3>Payment history</h3><div className="table-wrap"><table><thead><tr><th>Amount</th><th>Method</th><th>Recorded</th></tr></thead><tbody>{mine.data.payments.map((payment) => <tr key={payment.id}><td>{money(payment.amount)}</td><td>{payment.payment_mode.replaceAll('_', ' ')}</td><td>{dateLabel(payment.created_at)}</td></tr>)}</tbody></table></div></section>}
      </>}
    </>}

    {isAdmin && <>
      <form className="feature-form compact-form" onSubmit={(event) => void createRecord(event)}>
        <h3>Create a fee record</h3>
        <Field label="Student"><select required value={studentId} onChange={(event) => setStudentId(event.target.value)}><option value="">Choose a student</option>{students.data?.map((student) => <option key={student.user_id} value={student.user_id}>{student.full_name} · {student.student_number} (account {student.user_id})</option>)}</select></Field>
        <Field label="Total fee (INR)"><input required type="number" min="0.01" step="0.01" value={totalAmount} onChange={(event) => setTotalAmount(event.target.value)} /></Field>
        <LoadState loading={students.loading} error={students.error} empty={!students.loading && !students.error && !students.data?.length} onRetry={students.reload} />
        <button className="primary-button form-submit" disabled={busy || students.loading || !students.data?.length}>{busy ? 'Saving…' : 'Create fee record'}</button>
      </form>
      <LoadState loading={records.loading} error={records.error} empty={!records.loading && !records.error && !records.data?.length} onRetry={records.reload} />
      {!!records.data?.length && <div className="table-wrap"><table><thead><tr><th>Student</th><th>Total fee</th><th>Paid</th><th>Balance</th><th>Status</th><th>Update total</th></tr></thead><tbody>{records.data.map((record) => <tr key={record.id}>
        <td>{record.student_username}<small>Account {record.student}</small></td><td>{money(record.total_amount)}</td><td>{money(record.amount_paid)}</td><td>{money(record.balance_due)}</td><td><FeeStatus status={record.fee_status} /></td>
        <td><div className="fee-update"><input aria-label={`New total for ${record.student_username}`} type="number" min={record.amount_paid} step="0.01" value={totals[record.id] ?? record.total_amount} onChange={(event) => setTotals({ ...totals, [record.id]: event.target.value })} /><button type="button" className="secondary-button" disabled={busy} onClick={() => void updateTotal(record)}>Save</button></div></td>
      </tr>)}</tbody></table></div>}
    </>}
  </Page>
}
