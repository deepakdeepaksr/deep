import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Login.css'

const ROLES = [
  { id: 'student', label: 'Student', desc: 'Play learning games', path: '/session' },
  { id: 'parent', label: 'Parent / Teacher', desc: 'View progress dashboard', path: '/dashboard' },
]

function Login() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [role, setRole] = useState('student')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    const trimmed = name.trim()
    if (!trimmed) {
      setError('Please enter your name.')
      return
    }
    const user = { role, name: trimmed, id: `user-${Date.now()}` }
    localStorage.setItem('learning_platform_user', JSON.stringify(user))
    const config = ROLES.find((r) => r.id === role)
    navigate(config.path, { state: { user } })
  }

  return (
    <div className="login-page">
      <div className="login-card card">
        <div className="login-header">
          <h1>Adaptive Learning Platform</h1>
          <p className="login-subtitle">For Dyslexic Children — Real-time AI-Powered Personalization</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <label htmlFor="name">Your name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter name"
            autoComplete="name"
            autoFocus
          />

          <label>I am a</label>
          <div className="role-tabs">
            {ROLES.map((r) => (
              <button
                key={r.id}
                type="button"
                className={`role-tab ${role === r.id ? 'active' : ''}`}
                onClick={() => setRole(r.id)}
              >
                <span className="role-label">{r.label}</span>
                <span className="role-desc">{r.desc}</span>
              </button>
            ))}
          </div>

          {error && <p className="login-error">{error}</p>}

          <button type="submit" className="btn-primary login-btn">
            Continue
          </button>
        </form>
      </div>
    </div>
  )
}

export default Login
