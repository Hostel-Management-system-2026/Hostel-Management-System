import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { roleLabel } from '../auth/roles'

const workspaces = {
  STUDENT: [
    ['My profile', 'View your hostel information', '/profiles/me'],
    ['Complaints', 'Raise and follow up on an issue', '/complaints'],
    ['Notices', 'Read updates from your hostel', '/notices'],
    ['Mess menu', 'See this week’s meals', '/mess'],
    ['Leave request', 'Request an outpass', '/leave'],
  ],
  WARDEN: [
    ['Visitors', 'Log arrivals and departures', '/visitors'],
    ['Leave requests', 'Review student outpasses', '/leave'],
    ['Complaints', 'Review and update reports', '/complaints'],
  ],
  ADMIN: [
    ['Student profiles', 'Maintain student records', '/profiles'],
    ['Room allocations', 'View and assign rooms', '/allocations'],
    ['Notices', 'Publish hostel announcements', '/notices'],
    ['Mess menu', 'Publish the weekly menu', '/mess'],
  ],
} as const

export default function DashboardPage() {
  const { role } = useAuth()
  if (!role) return null
  const date = new Intl.DateTimeFormat('en', { weekday: 'long', month: 'long', day: 'numeric' }).format(new Date())
  return (
    <div className="dashboard-page">
      <div className="page-heading">
        <div><div className="eyebrow">YOUR HMS WORKSPACE</div><h2>Good to see you.</h2>
          <p>Your {roleLabel(role).toLowerCase()} workspace is ready.</p></div>
        <div className="date-pill"><span className="date-dot" />{date}</div>
      </div>
      <section className="welcome-card">
        <div className="welcome-orb" />
        <div className="welcome-content"><span className="welcome-tag">HOSTEL LIFE, MADE SIMPLER</span>
          <h3>One place for the things<br />that keep life moving.</h3>
          <p>Choose a workspace below to get started.</p></div>
        <div className="welcome-number">H<span>MS</span></div>
      </section>
      <section className="workspace-section">
        <div className="section-heading"><div><div className="eyebrow">QUICK ACCESS</div><h3>Your workspaces</h3></div>
          <span className="section-count">0{workspaces[role].length} AREAS</span></div>
        <div className="workspace-grid">
          {workspaces[role].map(([title, description, path], index) => (
            <Link className="workspace-card" to={path} key={path}>
              <span className={`workspace-icon icon-${index + 1}`} aria-hidden="true">{['↗', '▦', '◷', '＋'][index % 4]}</span>
              <span className="workspace-card-copy"><strong>{title}</strong><small>{description}</small></span>
              <span className="workspace-arrow" aria-hidden="true">↗</span>
            </Link>
          ))}
        </div>
      </section>
      <div className="dashboard-footnote"><span className="status-pulse" />Your account access is managed by your hostel role.</div>
    </div>
  )
}
