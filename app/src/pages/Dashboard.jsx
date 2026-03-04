import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Dashboard.css'

const STRUGGLE_LABELS = {
  0: { text: 'Normal', class: 'label-normal' },
  1: { text: 'Phonics issue', class: 'label-phonics' },
  2: { text: 'Spelling issue', class: 'label-spelling' },
  3: { text: 'Visual issue', class: 'label-visual' },
}

// Mock session trend for demo (replace with real data from API)
const MOCK_TREND = [42, 48, 55, 52, 58, 65, 62, 68, 72]

function Dashboard() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [demoData, setDemoData] = useState({
    currentDifficulty: 'Medium',
    struggleClass: 1,
    predictedImprovement: 12,
    riskScore: 'Moderate',
    sessionTrend: MOCK_TREND,
    lastUpdated: new Date().toLocaleTimeString(),
  })

  useEffect(() => {
    const raw = localStorage.getItem('learning_platform_user')
    if (!raw) {
      navigate('/', { replace: true })
      return
    }
    try {
      setUser(JSON.parse(raw))
    } catch {
      navigate('/', { replace: true })
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('learning_platform_user')
    navigate('/')
  }

  if (!user) return null

  const struggle = STRUGGLE_LABELS[demoData.struggleClass] || STRUGGLE_LABELS[0]
  const maxVal = Math.max(...demoData.sessionTrend)
  const minVal = Math.min(...demoData.sessionTrend)

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Progress Dashboard — {user.name}</h1>
        <button type="button" className="btn-secondary header-btn" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <main className="app-main">
        <p className="dashboard-intro">
          Live view while the student is in a session. Data updates as the AI layer runs (XGBoost, MLP, DQN).
        </p>

        <div className="dashboard-grid">
          <div className="card metric-card">
            <h3>Current difficulty level</h3>
            <p className="metric-value difficulty-value">{demoData.currentDifficulty}</p>
          </div>

          <div className="card metric-card">
            <h3>Struggle classification</h3>
            <span className={`label-tag ${struggle.class} metric-tag`}>{struggle.text}</span>
          </div>

          <div className="card metric-card">
            <h3>Predicted improvement %</h3>
            <p className="metric-value improvement-value">+{demoData.predictedImprovement}%</p>
          </div>

          <div className="card metric-card">
            <h3>Risk score</h3>
            <p className={`metric-value risk-value risk-${demoData.riskScore.toLowerCase()}`}>{demoData.riskScore}</p>
          </div>
        </div>

        <div className="card trend-card">
          <h3>Session trend (accuracy over rounds)</h3>
          <p className="trend-sub">Last 9 rounds — updates in real time</p>
          <div className="trend-chart">
            {demoData.sessionTrend.map((val, i) => (
              <div
                key={i}
                className="trend-bar-wrap"
                title={`Round ${i + 1}: ${val}%`}
              >
                <div
                  className="trend-bar"
                  style={{
                    height: maxVal > minVal ? `${((val - minVal) / (maxVal - minVal)) * 100}%` : '50%',
                  }}
                />
                <span className="trend-label">{val}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card model-summary">
          <h3>Model functionality summary</h3>
          <table className="summary-table">
            <thead>
              <tr>
                <th>Model</th>
                <th>Role</th>
                <th>When it runs</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>XGBoost</strong></td>
                <td>Identify struggle type</td>
                <td>After each mini-session</td>
              </tr>
              <tr>
                <td><strong>MLP</strong></td>
                <td>Predict future performance</td>
                <td>After session</td>
              </tr>
              <tr>
                <td><strong>DQN</strong></td>
                <td>Decide next difficulty + mode</td>
                <td>After every game round</td>
              </tr>
            </tbody>
          </table>
          <p className="last-updated">Last updated: {demoData.lastUpdated}</p>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
