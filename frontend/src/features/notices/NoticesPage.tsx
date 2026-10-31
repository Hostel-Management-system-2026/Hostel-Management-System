
import { useCallback, useEffect, useState } from 'react';
import { ApiError } from '../../api/client';
import { useAuth } from '../../auth/AuthContext';
import {
    noticesApi,
    type Notice,
    type CreateNotice,
} from './api';

export default function NoticesPage() {
    const { role } = useAuth();
    const isAdmin = role === 'ADMIN';

    const [notices, setNotices] = useState<Notice[]>([]);
    const [title, setTitle] = useState('');
    const [body, setBody] = useState('');
    const [audience, setAudience] = useState('ALL_STUDENTS');
    const [isPublished, setIsPublished] = useState(true);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const loadNotices = useCallback(async () => {
        setLoading(true);
        setError('');

        try {
            const result = await noticesApi.getAll();
            setNotices(result);
        } catch (err) {
            setError(
                err instanceof ApiError
                    ? err.message
                    : 'Could not load notices. Please try again.',
            );
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        void loadNotices();
    }, [loadNotices]);

    function resetForm() {
        setTitle('');
        setBody('');
        setAudience('ALL_STUDENTS');
        setIsPublished(true);
        setEditingId(null);
    }

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setError('');
        setMessage('');

        const payload: CreateNotice = {
            title: title.trim(),
            body: body.trim(),
            audience,
            is_published: isPublished,
        };

        if (!payload.title || !payload.body) {
            setError('Please enter both a title and notice body.');
            return;
        }

        setSaving(true);

        try {
            if (editingId !== null) {
                await noticesApi.update(editingId, payload);
                setMessage('Notice updated successfully.');
            } else {
                await noticesApi.create(payload);
                setMessage('Notice created successfully.');
            }

            resetForm();
            await loadNotices();
        } catch (err) {
            setError(
                err instanceof ApiError
                    ? err.message
                    : 'Could not save the notice. Please try again.',
            );
        } finally {
            setSaving(false);
        }
    }

    function startEditing(notice: Notice) {
        setEditingId(notice.id);
        setTitle(notice.title);
        setBody(notice.body);
        setAudience(notice.audience);
        setIsPublished(notice.is_published);
        setError('');
        setMessage('');
    }

    async function handleDelete(id: number) {
        const confirmed = window.confirm(
            'Are you sure you want to delete this notice?',
        );

        if (!confirmed) return;

        setError('');
        setMessage('');

        try {
            await noticesApi.delete(id);
            setMessage('Notice deleted successfully.');

            if (editingId === id) {
                resetForm();
            }

            await loadNotices();
        } catch (err) {
            setError(
                err instanceof ApiError
                    ? err.message
                    : 'Could not delete the notice. Please try again.',
            );
        }
    }

    return (
        <section className="feature-page">
            <header className="feature-header">
                <div>
                    <p className="eyebrow">HOSTEL MANAGEMENT</p>
                    <h1>Notices</h1>
                    <p>View important hostel announcements and updates.</p>
                </div>
            </header>

            {error && <div className="feedback error-feedback" role="alert">{error}</div>}
            {message && <div className="feedback success-feedback" role="status">{message}</div>}

            {isAdmin && (
                <section className="feature-card">
                    <h2>{editingId !== null ? 'Edit Notice' : 'Create Notice'}</h2>

                    <form className="profile-form" onSubmit={handleSubmit}>
                        <label>
                            <span>Title</span>
                            <input
                                id="notice-title"
                                value={title}
                                onChange={(event) => setTitle(event.target.value)}
                                maxLength={180}
                                required
                            />
                        </label>

                        <label className="notice-body-field">
                            <span>Notice body</span>
                            <textarea
                                id="notice-body"
                                value={body}
                                onChange={(event) => setBody(event.target.value)}
                                maxLength={10000}
                                rows={6}
                                required
                            />
                        </label>

                        <label>
                            <span>Audience</span>
                            <select
                                id="notice-audience"
                                value={audience}
                                onChange={(event) => setAudience(event.target.value)}
                            >
                                <option value="ALL_STUDENTS">All students</option>
                                <option value="STUDENTS">Students</option>
                            </select>
                        </label>

                        <label className="notice-publish-toggle">
                            <input
                                id="notice-published"
                                type="checkbox"
                                checked={isPublished}
                                onChange={(event) => setIsPublished(event.target.checked)}
                            />
                            <span>Publish this notice</span>
                        </label>

                        <div className="profile-form-actions">
                            <button type="submit" disabled={saving}>
                                {saving
                                    ? 'Saving...'
                                    : editingId !== null
                                        ? 'Update notice'
                                        : 'Create notice'}
                            </button>
                            {editingId !== null && (
                                <button type="button" className="secondary-button" onClick={resetForm} disabled={saving}>
                                    Cancel edit
                                </button>
                            )}
                        </div>
                    </form>
                </section>
            )}

            <section className="feature-card">
                <h2>Available Notices</h2>

                {loading ? (
                    <p>Loading notices...</p>
                ) : notices.length === 0 ? (
                    <p>No notices available.</p>
                ) : (
                    <ul className="notice-list">
                        {notices.map((notice) => (
                            <li className="notice-entry" key={notice.id}>
                                <article className="notice-card">
                                    <header className="notice-card-header">
                                        <div>
                                            <p className="eyebrow">{notice.audience.replaceAll('_', ' ')}</p>
                                            <h3>{notice.title}</h3>
                                        </div>
                                        <span className={`status-badge ${notice.is_published ? 'status-resolved' : 'status-open'}`}>
                                            {notice.is_published ? 'Published' : 'Draft'}
                                        </span>
                                    </header>
                                    <p className="notice-body">{notice.body}</p>
                                    <div className="notice-metadata">
                                        <span>Created {new Date(notice.created_at).toLocaleString()}</span>
                                    </div>

                                    {isAdmin && (
                                        <div className="action-row">
                                            <button
                                                type="button"
                                                className="secondary-button"
                                                onClick={() => startEditing(notice)}
                                            >
                                                Edit
                                            </button>
                                            <button
                                                type="button"
                                                className="secondary-button danger-button"
                                                onClick={() => void handleDelete(notice.id)}
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    )}
                                </article>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </section>
    );
}
