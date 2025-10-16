
/**
 * User profile page (protected)
 */
import { useAuth } from '../contexts/AuthContext';
import { ProtectedRoute } from '../components/ProtectedRoute';
import Link from 'next/link';
import styles from '../styles/Profile.module.css';

export default function ProfilePage() {
  const { user, logout } = useAuth();

  return (
    <ProtectedRoute>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>Profile</h1>
          <nav className={styles.nav}>
            <Link href="/dashboard" className={styles.navLink}>
              Dashboard
            </Link>
            <button onClick={logout} className={styles.logoutButton}>
              Logout
            </button>
          </nav>
        </div>

        <div className={styles.card}>
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>User Information</h2>
            
            <div className={styles.field}>
              <label className={styles.label}>User ID</label>
              <p className={styles.value}>{user?.id}</p>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Email</label>
              <p className={styles.value}>{user?.email}</p>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Username</label>
              <p className={styles.value}>{user?.username}</p>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Status</label>
              <p className={styles.value}>
                {user?.is_active ? (
                  <span className={styles.badge + ' ' + styles.active}>Active</span>
                ) : (
                  <span className={styles.badge + ' ' + styles.inactive}>Inactive</span>
                )}
              </p>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Role</label>
              <p className={styles.value}>
                {user?.is_superuser ? (
                  <span className={styles.badge + ' ' + styles.superuser}>Superuser</span>
                ) : (
                  <span className={styles.badge}>User</span>
                )}
              </p>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Member Since</label>
              <p className={styles.value}>
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </p>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Last Updated</label>
              <p className={styles.value}>
                {user?.updated_at ? new Date(user.updated_at).toLocaleDateString() : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}

