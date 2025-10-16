
/**
 * Dashboard page with task management (protected)
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { ProtectedRoute } from '../components/ProtectedRoute';
import Link from 'next/link';
import { getTasks, createTask, updateTask, deleteTask, Task, TaskCreate, TaskUpdate } from '../lib/api';
import styles from '../styles/Dashboard.module.css';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    loadTasks();
  }, [filter]);

  const loadTasks = async () => {
    setLoading(true);
    setError('');

    try {
      const completed = filter === 'all' ? undefined : filter === 'completed';
      const tasksData = await getTasks({ completed });
      setTasks(tasksData);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const newTask = await createTask({
        title: newTaskTitle,
        description: newTaskDescription || undefined,
      });
      setTasks([newTask, ...tasks]);
      setNewTaskTitle('');
      setNewTaskDescription('');
      setShowCreateForm(false);
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    }
  };

  const handleToggleTask = async (task: Task) => {
    try {
      const updated = await updateTask(task.id, {
        is_completed: !task.is_completed,
      });
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await deleteTask(taskId);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    }
  };

  return (
    <ProtectedRoute>
      <div className={styles.container}>
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Dashboard</h1>
            <p className={styles.welcome}>Welcome, {user?.username}!</p>
          </div>
          <nav className={styles.nav}>
            <Link href="/profile" className={styles.navLink}>
              Profile
            </Link>
            <button onClick={logout} className={styles.logoutButton}>
              Logout
            </button>
          </nav>
        </div>

        {error && (
          <div className={styles.error}>
            {error}
          </div>
        )}

        <div className={styles.content}>
          <div className={styles.toolbar}>
            <div className={styles.filters}>
              <button
                className={`${styles.filterButton} ${filter === 'all' ? styles.active : ''}`}
                onClick={() => setFilter('all')}
              >
                All
              </button>
              <button
                className={`${styles.filterButton} ${filter === 'active' ? styles.active : ''}`}
                onClick={() => setFilter('active')}
              >
                Active
              </button>
              <button
                className={`${styles.filterButton} ${filter === 'completed' ? styles.active : ''}`}
                onClick={() => setFilter('completed')}
              >
                Completed
              </button>
            </div>
            <button
              className={styles.createButton}
              onClick={() => setShowCreateForm(!showCreateForm)}
            >
              {showCreateForm ? 'Cancel' : 'New Task'}
            </button>
          </div>

          {showCreateForm && (
            <div className={styles.createForm}>
              <h3 className={styles.formTitle}>Create New Task</h3>
              <form onSubmit={handleCreateTask}>
                <div className={styles.field}>
                  <label htmlFor="title" className={styles.label}>
                    Title
                  </label>
                  <input
                    id="title"
                    type="text"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="Task title"
                    required
                    className={styles.input}
                  />
                </div>
                <div className={styles.field}>
                  <label htmlFor="description" className={styles.label}>
                    Description (optional)
                  </label>
                  <textarea
                    id="description"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    placeholder="Task description"
                    rows={3}
                    className={styles.textarea}
                  />
                </div>
                <button type="submit" className={styles.submitButton}>
                  Create Task
                </button>
              </form>
            </div>
          )}

          <div className={styles.taskList}>
            {loading ? (
              <p className={styles.loading}>Loading tasks...</p>
            ) : tasks.length === 0 ? (
              <p className={styles.empty}>No tasks found. Create your first task!</p>
            ) : (
              tasks.map((task) => (
                <div key={task.id} className={styles.taskCard}>
                  <div className={styles.taskContent}>
                    <input
                      type="checkbox"
                      checked={task.is_completed}
                      onChange={() => handleToggleTask(task)}
                      className={styles.checkbox}
                    />
                    <div className={styles.taskInfo}>
                      <h4 className={`${styles.taskTitle} ${task.is_completed ? styles.completed : ''}`}>
                        {task.title}
                      </h4>
                      {task.description && (
                        <p className={styles.taskDescription}>{task.description}</p>
                      )}
                      <p className={styles.taskDate}>
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className={styles.deleteButton}
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}

