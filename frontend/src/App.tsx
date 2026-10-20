
import {
  Link,
  NavLink,
  Navigate,
  Outlet,
  Route,
  Routes,
  useLocation,
} from 'react-router-dom';

import { useAuth } from './auth/AuthContext';
import { RequireAuth, RequireRole } from './auth/RouteGuards';
import { roleLabel, type Role } from './auth/roles';
import FeaturePlaceholder from './components/FeaturePlaceholder';
import ProfilesPage from './features/profiles/ProfilesPage';
import ComplaintsPage from './features/complaints/ComplaintsPage';
import NoticesPage from './features/notices/NoticesPage';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';

type NavItem = {
  label: string;
  to: string;
  icon: string;
  roles: Role[];
  endpoint: string;
  description: string;
};

const navItems: NavItem[] = [
  {
    label: 'My profile',
    to: '/profiles/me',
    icon: '◉',
    roles: ['STUDENT'],
    endpoint: 'GET /api/v1/profiles/me',
    description: 'View your own profile information.',
  },
  {
    label: 'Student profiles',
    to: '/profiles',
    icon: '◉',
    roles: ['ADMIN'],
    endpoint: 'GET, POST /api/v1/profiles',
    description: 'Maintain student records.',
  },
  {
    label: 'Complaints',
    to: '/complaints',
    icon: '▤',
    roles: ['STUDENT', 'WARDEN'],
    endpoint: 'GET, POST /api/v1/complaints',
    description:
      'Students submit and track complaints; wardens review and update them.',
  },
  {
    label: 'Notices',
    to: '/notices',
    icon: '◫',
    roles: ['STUDENT', 'ADMIN'],
    endpoint: 'GET, POST /api/v1/notices',
    description: 'Read notices or publish hostel announcements.',
  },
  {
    label: 'Room allocations',
    to: '/allocations',
    icon: '▦',
    roles: ['ADMIN'],
    endpoint: 'GET, POST /api/v1/allocations/',
    description: 'View and create student room allocations.',
  },
  {
    label: 'Visitors',
    to: '/visitors',
    icon: '↔',
    roles: ['WARDEN'],
    endpoint: 'POST /api/v1/visitors · PATCH /api/v1/visitors/{id}/exit',
    description: 'Log visitor arrivals and departures.',
  },
  {
    label: 'Mess menu',
    to: '/mess',
    icon: '⌂',
    roles: ['STUDENT', 'ADMIN'],
    endpoint: 'GET, POST /api/v1/mess/menu',
    description: 'View or publish the weekly menu.',
  },
  {
    label: 'Leave requests',
    to: '/leave',
    icon: '◷',
    roles: ['STUDENT', 'WARDEN'],
    endpoint: 'GET, POST /api/v1/leave',
    description: 'Submit requests or review pending outpasses.',
  },
];

function AppShell() {
  const { role, signOut } = useAuth();
  const location = useLocation();

  if (!role) {
    return <Navigate to="/login" replace />;
  }

  const items = navItems.filter((item) => item.roles.includes(role));
  const active = navItems.find(
    (item) => location.pathname === item.to,
  );

  const title =
    active?.label ??
    (location.pathname === '/dashboard' ? 'Overview' : 'Workspace');

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link to="/dashboard" className="brand brand-sidebar">
          <span className="brand-mark">H</span>
          <span>
            HMS
            <small>HOSTEL MANAGEMENT</small>
          </span>
        </Link>

        <div className="sidebar-label">WORKSPACE</div>

        <nav className="side-nav" aria-label="Main navigation">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `nav-link${isActive ? ' active' : ''}`
            }
          >
            <span className="nav-icon">⌂</span>
            <span>Overview</span>
          </NavLink>

          <div className="nav-divider" />

          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `nav-link${isActive ? ' active' : ''}`
              }
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-status">
            <span className="status-pulse" />
            <span>HMS workspace</span>
            <small>Session active</small>
          </div>

          <div className="sidebar-version">
            HOSTEL MANAGEMENT SYSTEM <span>v0.1</span>
          </div>
        </div>
      </aside>

      <div className="main-column">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Workspace</span>
            <span className="crumb-separator">/</span>
            <strong>{title}</strong>
          </div>

          <div className="topbar-user">
            <div className="user-avatar">{role[0]}</div>
            <div className="user-meta">
              <strong>{roleLabel(role)} account</strong>
              <span>{roleLabel(role)}</span>
            </div>

            <button
              className="logout-button"
              onClick={signOut}
              aria-label="Sign out"
              title="Sign out"
            >
              ↪
            </button>
          </div>
        </header>

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

function FeatureRoute({ item }: { item: NavItem }) {
  if (item.to === '/profiles/me' || item.to === '/profiles') {
    return <ProfilesPage />;
  }


  if (item.to === '/complaints') {
    return <ComplaintsPage />;
  }

  if (item.to === '/notices') {
    return <NoticesPage />;
  }

  return (
    <FeaturePlaceholder
      title={item.label}
      description={item.description}
      endpoint={item.endpoint}
    />
  );

}

function ForbiddenPage() {
  return (
    <div className="message-page">
      <span className="message-mark">403</span>
      <h2>This area isn’t available for your role.</h2>
      <p>
        Your account does not have permission to open this workspace.
      </p>
      <NavLink
        className="primary-button compact-button"
        to="/dashboard"
      >
        Back to overview
      </NavLink>
    </div>
  );
}

function NotFoundPage() {
  return (
    <div className="message-page">
      <span className="message-mark">404</span>
      <h2>We couldn’t find that page.</h2>
      <p>It may have moved, or the address may be incorrect.</p>
      <NavLink
        className="primary-button compact-button"
        to="/dashboard"
      >
        Back to overview
      </NavLink>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<RequireAuth />}>
        <Route element={<AppShell />}>
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />

          <Route path="/dashboard" element={<DashboardPage />} />

          {navItems.map((item) => (
            <Route
              key={item.to}
              element={<RequireRole allowed={item.roles} />}
            >
              <Route
                path={item.to}
                element={<FeatureRoute item={item} />}
              />
            </Route>
          ))}

          <Route path="/forbidden" element={<ForbiddenPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Route>
    </Routes>
  );
}
