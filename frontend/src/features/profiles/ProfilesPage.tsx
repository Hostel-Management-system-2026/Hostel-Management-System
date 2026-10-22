
import { useCallback, useEffect, useState } from 'react';
import { ApiError } from '../../api/client';
import { useAuth } from '../../auth/AuthContext';
import {
    profilesApi,
    type CreateStudentProfile,
    type StudentProfile,
} from './api';

const emptyProfile: CreateStudentProfile = {
    user_id: '',
    student_number: '',
    full_name: '',
    email: '',
    phone: '',
    room_number: '',
    course: '',
    year_of_study: 1,
};

function errorMessage(error: unknown): string {
    if (error instanceof ApiError) {
        return error.message;
    }

    return error instanceof Error
        ? error.message
        : 'Something went wrong. Please try again.';
}

export default function ProfilesPage() {
    const { role } = useAuth();
    const isAdmin = role === 'ADMIN';

    const [profiles, setProfiles] = useState<StudentProfile[]>([]);
    const [myProfile, setMyProfile] = useState<StudentProfile | null>(null);
    const [form, setForm] = useState<CreateStudentProfile>(emptyProfile);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [notice, setNotice] = useState('');

    const loadProfiles = useCallback(async () => {
        setLoading(true);
        setError('');

        try {
            if (isAdmin) {
                const result = await profilesApi.getAll();
                setProfiles(result);
            } else {
                const result = await profilesApi.getMyProfile();
                setMyProfile(result);
            }
        } catch (err) {
            setError(errorMessage(err));
        } finally {
            setLoading(false);
        }
    }, [isAdmin]);

    useEffect(() => {
        void loadProfiles();
    }, [loadProfiles]);

    function updateField(
        field: keyof CreateStudentProfile,
        value: string,
    ) {
        setForm((current) => ({
            ...current,
            [field]: field === 'year_of_study' ? Number(value) : value,
        }));
    }

    function startEditing(profile: StudentProfile) {
        setEditingId(profile.id);
        setForm({
            user_id: profile.user_id,
            student_number: profile.student_number,
            full_name: profile.full_name,
            email: profile.email,
            phone: profile.phone,
            room_number: profile.room_number,
            course: profile.course,
            year_of_study: profile.year_of_study,
        });
        setError('');
        setNotice('');
    }

    function cancelEditing() {
        setEditingId(null);
        setForm({ ...emptyProfile });
        setError('');
    }

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setSaving(true);
        setError('');
        setNotice('');

        try {
            if (editingId !== null) {
                await profilesApi.update(editingId, form);
                setNotice('Profile updated successfully.');
            } else {
                await profilesApi.create(form);
                setNotice('Student profile created successfully.');
            }

            cancelEditing();
            await loadProfiles();
        } catch (err) {
            setError(errorMessage(err));
        } finally {
            setSaving(false);
        }
    }

    if (loading) {
        return (
            <section className="feature-page">
                <p role="status">Loading profiles...</p>
            </section>
        );
    }

    return (
        <section className="feature-page">
            <header className="feature-header">
                <div>
                    <p className="eyebrow">HOSTEL MANAGEMENT</p>
                    <h1>{isAdmin ? 'Student profiles' : 'My profile'}</h1>
                    <p>
                        {isAdmin
                            ? 'View and maintain student records.'
                            : 'View your registered student information.'}
                    </p>
                </div>
                <button className="secondary-button" onClick={() => void loadProfiles()}>
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

            {isAdmin ? (
                <>
                    <section className="feature-card">
                        <h2>{editingId === null ? 'Add a student' : 'Edit student'}</h2>
                        <form className="profile-form" onSubmit={handleSubmit}>
                            <label>
                                User ID
                                <input
                                    required
                                    value={form.user_id}
                                    onChange={(e) => updateField('user_id', e.target.value)}
                                />
                            </label>
                            <label>
                                Student number
                                <input
                                    required
                                    value={form.student_number}
                                    onChange={(e) => updateField('student_number', e.target.value)}
                                />
                            </label>
                            <label>
                                Full name
                                <input
                                    required
                                    value={form.full_name}
                                    onChange={(e) => updateField('full_name', e.target.value)}
                                />
                            </label>
                            <label>
                                Email
                                <input
                                    type="email"
                                    value={form.email}
                                    onChange={(e) => updateField('email', e.target.value)}
                                />
                            </label>
                            <label>
                                Phone
                                <input
                                    value={form.phone}
                                    onChange={(e) => updateField('phone', e.target.value)}
                                />
                            </label>
                            <label>
                                Room number
                                <input
                                    value={form.room_number}
                                    onChange={(e) => updateField('room_number', e.target.value)}
                                />
                            </label>
                            <label>
                                Course
                                <input
                                    value={form.course}
                                    onChange={(e) => updateField('course', e.target.value)}
                                />
                            </label>
                            <label>
                                Year of study
                                <input
                                    type="number"
                                    min="1"
                                    value={form.year_of_study}
                                    onChange={(e) => updateField('year_of_study', e.target.value)}
                                />
                            </label>

                            <div className="profile-form-actions">
                                <button type="submit" disabled={saving}>
                                    {saving
                                        ? 'Saving...'
                                        : editingId === null
                                            ? 'Create profile'
                                            : 'Save changes'}
                                </button>
                                {editingId !== null && (
                                    <button
                                        type="button"
                                        className="secondary-button"
                                        onClick={cancelEditing}
                                    >
                                        Cancel
                                    </button>
                                )}
                            </div>
                        </form>
                    </section>

                    <section className="feature-card">
                        <h2>All students</h2>
                        {profiles.length === 0 ? (
                            <p>No student profiles were returned by the server.</p>
                        ) : (
                            <div className="profile-table-wrap">
                                <table className="profile-table">
                                    <thead>
                                        <tr>
                                            <th>Student number</th>
                                            <th>Name</th>
                                            <th>Email</th>
                                            <th>Room</th>
                                            <th>Course</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {profiles.map((profile) => (
                                            <tr key={profile.id}>
                                                <td>{profile.student_number}</td>
                                                <td>{profile.full_name}</td>
                                                <td>{profile.email || '—'}</td>
                                                <td>{profile.room_number || '—'}</td>
                                                <td>{profile.course || '—'}</td>
                                                <td>
                                                    <button
                                                        type="button"
                                                        className="secondary-button"
                                                        onClick={() => startEditing(profile)}
                                                    >
                                                        Edit
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </section>
                </>
            ) : myProfile ? (
                <section className="feature-card">
                    <h2>{myProfile.full_name}</h2>
                    <dl className="profile-details">
                        <div><dt>Student number</dt><dd>{myProfile.student_number}</dd></div>
                        <div><dt>Email</dt><dd>{myProfile.email || '—'}</dd></div>
                        <div><dt>Phone</dt><dd>{myProfile.phone || '—'}</dd></div>
                        <div><dt>Room number</dt><dd>{myProfile.room_number || '—'}</dd></div>
                        <div><dt>Course</dt><dd>{myProfile.course || '—'}</dd></div>
                        <div><dt>Year of study</dt><dd>{myProfile.year_of_study}</dd></div>
                    </dl>
                </section>
            ) : (
                <section className="feature-card">
                    <p>No profile data was returned by the server.</p>
                </section>
            )}
        </section>
    );
}
