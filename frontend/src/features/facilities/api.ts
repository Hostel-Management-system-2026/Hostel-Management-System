import { api } from '../../api/client'

export type Facility = {
  id: number
  name: string
  description: string
  location: string
  capacity: number
  is_active: boolean
}

export type FacilityBooking = {
  id: number
  facility: number
  facility_name: string
  student: string
  booking_date: string
  start_time: string
  end_time: string
  status: 'CONFIRMED' | 'CANCELLED'
  created_at: string
}

export type FacilityAvailability = {
  facility: Facility
  date: string
  booked_slots: FacilityBooking[]
}

export type FacilityDraft = Omit<Facility, 'id'>

export const facilitiesApi = {
  listForStudents: () => api.get<Facility[]>('/facilities/'),
  listForStaff: () => api.get<Facility[]>('/staff/facilities/'),
  availability: (facilityId: number, date: string) =>
    api.get<FacilityAvailability>(`/facilities/${facilityId}/availability/?date=${encodeURIComponent(date)}`),
  create: (draft: FacilityDraft) => api.post<Facility>('/staff/facilities/', draft),
  update: (id: number, draft: FacilityDraft) => api.patch<Facility>(`/staff/facilities/${id}/`, draft),
  book: (draft: { facility: number; booking_date: string; start_time: string; end_time: string }) =>
    api.post<FacilityBooking>('/facility-bookings/', draft),
}
