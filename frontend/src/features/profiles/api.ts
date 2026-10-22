
import { api } from '../../api/client';

export interface StudentProfile {
    id: number;
    user_id: string;
    student_number: string;
    full_name: string;
    email: string;
    phone: string;
    room_number: string;
    course: string;
    year_of_study: number;
    created_at: string;
    updated_at: string;
}

export interface CreateStudentProfile {
    user_id: string;
    student_number: string;
    full_name: string;
    email: string;
    phone: string;
    room_number: string;
    course: string;
    year_of_study: number;
}

export const profilesApi = {
    getMyProfile: () =>
        api.get<StudentProfile>('/profiles/me'),

    getAll: () =>
        api.get<StudentProfile[]>('/profiles'),

    create: (profile: CreateStudentProfile) =>
        api.post<StudentProfile>('/profiles', profile),

    update: (id: number, profile: Partial<CreateStudentProfile>) =>
        api.patch<StudentProfile>(`/profiles/${id}`, profile),
};
