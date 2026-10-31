import { ApiError, api } from '../../api/client'

export type Payment = {
  id: number
  amount: string
  payment_mode: string
  created_at: string
}

export type FeeRecord = {
  id: number
  total_amount: string
  amount_paid: string
  balance_due: string
  fee_status: 'UNPAID' | 'PARTIAL' | 'PAID'
  payments?: Payment[]
}

export type StaffFeeRecord = Omit<FeeRecord, 'payments'> & {
  student: number
  student_username: string
}

export type StudentProfile = {
  user_id: string
  student_number: string
  full_name: string
}

export async function getMyFeeRecord(): Promise<FeeRecord | null> {
  try { return await api.get<FeeRecord>('/fees/my') }
  catch (error) {
    if (error instanceof ApiError && error.status === 404) return null
    throw error
  }
}

export const feesApi = {
  mine: getMyFeeRecord,
  pay: (amount: string, payment_mode: string) =>
    api.post<FeeRecord>('/fees/pay', { amount, payment_mode }),
  records: () => api.get<StaffFeeRecord[]>('/fees/records'),
  students: () => api.get<StudentProfile[]>('/profiles'),
  createRecord: (student: number, total_amount: string) =>
    api.post<StaffFeeRecord>('/fees/records', { student, total_amount }),
  updateTotal: (id: number, total_amount: string) =>
    api.patch<StaffFeeRecord>(`/fees/records/${id}`, { total_amount }),
}
