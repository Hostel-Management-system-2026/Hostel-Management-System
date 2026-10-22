
import { api } from '../../api/client';

export interface Notice {
    id: number;
    title: string;
    body: string;
    audience: string;
    is_published: boolean;
    published_by: string;
    created_at: string;
    updated_at: string;
}

export interface CreateNotice {
    title: string;
    body: string;
    audience: string;
    is_published: boolean;
}

export type UpdateNotice = Partial<CreateNotice>;

export const noticesApi = {
    getAll: () => api.get<Notice[]>('/notices'),

    create: (notice: CreateNotice) =>
        api.post<Notice>('/notices', notice),

    update: (id: number, notice: UpdateNotice) =>
        api.patch<Notice>(`/notices/${id}`, notice),

    delete: (id: number) =>
        api.delete<void>(`/notices/${id}`),
};
