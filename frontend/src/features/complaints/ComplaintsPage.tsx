
import { useCallback, useEffect, useState } from 'react';
import { ApiError } from '../../api/client';
import { useAuth } from '../../auth/AuthContext';
import {
    complaintsApi,
    type Complaint,
    type ComplaintStatus,
} from './api';

function getErrorMessage(error: unknown): string {
    if (error instanceof ApiError) {
        return error.message;
    }

    return error instanceof Error
        ? error.message
        : 'Something went wrong. Please try again.';
}

function formatDate(value: string): string {
    const date = new Date(value);

    return Number.isNaN(date.getTime())
        ? value
        : date.toLocaleString();
}

function statusLabel(status: ComplaintStatus): string {
    return status.replace('_', ' ');
}

export default function ComplaintsPage() {
    const { role } = useAuth();
    const isWarden = role === 'WARDEN';

    const [complaints, setComplaints] = useState<Complaint[]>([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [updatingId, setUpdatingId] = useState<number | null>(null);
    const [error, setError] = useState('');
    const [notice, setNotice] = useState('');

    const loadComplaints = useCallback(async () => {
        setLoading(true);
        setError('');

        try {
            const result = await complaintsApi.getAll();
            setComplaints(result);
        } catch (err) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        void loadComplaints();
    }, [loadComplaints]);

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setSubmitting(true);
        setError('');
        setNotice('');

        try {
            await complaintsApi.create({
                title: title.trim(),
                description: description.trim(),
            });

            setTitle('');
            setDescription('');
            setNotice('Complaint submitted successfully.');
            await loadComplaints();
        } catch (err) {
            setError(getErrorMessage(err));
        } finally {
            setSubmitting(false);
        }
    }

    async function handleStatusUpdate(
        complaint: Complaint,
        nextStatus: ComplaintStatus,
    ) {
        setUpdatingId(complaint.id);
        setError('');
        setNotice('');

        try {
            await complaintsApi.updateStatus(complaint.id, nextStatus);
            setNotice(`Complaint #${complaint.id} updated successfully.`);
            await loadComplaints();
        } catch (err) {
            setError(getErrorMessage(err));
        } finally {
            setUpdatingId(null);
        }
    }

    return (
        <section className="feature-page">
            <header className="feature-header">
                <div>
                    <p className="eyebrow">HOSTEL MANAGEMENT</p>
                    <h1>Complaints</h1>
                    <p>
                        {isWarden
                            ? 'Review student complaints and move them through the resolution process.'
                            : 'Submit an issue and track its progress.'}
                    </p>
                </div>

                <button
                    type="button"
                    className="secondary-button"
                    onClick={() => void loadComplaints()}
                    disabled={loading}
                >
                    Refresh
                </button>
            </header>

            {error && (
                <div className="feedback error-feedback" role="alert">
                    {error}
                </div>
            )}

            {notice && (
                <div className="feedback success-feedback" role="status">
                    {notice}
                </div>
            )}

            {!isWarden && (
                <section className="feature-card">
                    <h2>Submit a complaint</h2>

                    <form className="profile-form" onSubmit={handleSubmit}>
                        <label>
                            Complaint title
                            <input
                                value={title}
                                onChange={(event) => setTitle(event.target.value)}
                                maxLength={160}
                                required
                                placeholder="Briefly describe the issue"
                            />
                        </label>

                        <label>
                            Description
                            <textarea
                                value={description}
                                onChange={(event) => setDescription(event.target.value)}
                                maxLength={4000}
                                rows={5}
                                required
                                placeholder="Provide details so the hostel team can help."
                            />
                        </label>

                        <div className="profile-form-actions">
                            <button
                                type="submit"
                                disabled={
                                    submitting ||
                                    !title.trim() ||
                                    !description.trim()
                                }
                            >
                                {submitting ? 'Submitting...' : 'Submit complaint'}
                            </button>
                        </div>
                    </form>
                </section>
            )}

            <section className="feature-card">
                <h2>{isWarden ? 'Student complaints' : 'My complaints'}</h2>

                {loading ? (
                    <p role="status">Loading complaints...</p>
                ) : complaints.length === 0 ? (
                    <p>No complaints were returned by the server.</p>
                ) : (
                    <div className="complaint-list">
                        {complaints.map((complaint) => {
                            const nextStatus: ComplaintStatus | null =
                                complaint.status === 'OPEN'
                                    ? 'IN_PROGRESS'
                                    : complaint.status === 'IN_PROGRESS'
                                        ? 'RESOLVED'
                                        : null;

                            return (
                                <article
                                    className="complaint-item"
                                    key={complaint.id}
                                >
                                    <div className="complaint-item-header">
                                        <div>
                                            <p className="eyebrow">
                                                Complaint #{complaint.id}
                                            </p>
                                            <h3>{complaint.title}</h3>
                                        </div>

                                        <span
                                            className={`complaint-status status-${complaint.status.toLowerCase()}`}
                                        >
                                            {statusLabel(complaint.status)}
                                        </span>
                                    </div>

                                    <p className="complaint-description">
                                        {complaint.description}
                                    </p>

                                    <div className="complaint-meta">
                                        <span>
                                            Submitted: {formatDate(complaint.created_at)}
                                        </span>

                                        {isWarden && (
                                            <span>Student ID: {complaint.student_id}</span>
                                        )}
                                    </div>

                                    {isWarden && nextStatus && (
                                        <div className="profile-form-actions">
                                            <button
                                                type="button"
                                                disabled={updatingId === complaint.id}
                                                onClick={() =>
                                                    void handleStatusUpdate(
                                                        complaint,
                                                        nextStatus,
                                                    )
                                                }
                                            >
                                                {updatingId === complaint.id
                                                    ? 'Updating...'
                                                    : nextStatus === 'IN_PROGRESS'
                                                        ? 'Start progress'
                                                        : 'Mark resolved'}
                                            </button>
                                        </div>
                                    )}
                                </article>
                            );
                        })}
                    </div>
                )}
            </section>
        </section>
    );
}
