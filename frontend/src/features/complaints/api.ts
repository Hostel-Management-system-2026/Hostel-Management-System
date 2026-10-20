
import { api } from '../../api/client';

export type ComplaintStatus = 'OPEN' | 'IN_PROGRESS' | 'RESOLVED';

export interface Complaint {
    id: number;
    student_id: string;
    title: string;
    description: string;
    status: ComplaintStatus;
    created_at: string;
    updated_at: string;
}

export interface CreateComplaint {
    title: string;
    description: string;
}

export interface UpdateComplaintStatus {
    status: ComplaintStatus;
}

export const complaintsApi = {
    getAll: () => api.get<Complaint[]>('/complaints'),

    create: (complaint: CreateComplaint) =>
        api.post<Complaint>('/complaints', complaint),

    updateStatus: (id: number, status: ComplaintStatus) =>
        api.patch<Complaint>(`/complaints/${id}`, { status }),
};

