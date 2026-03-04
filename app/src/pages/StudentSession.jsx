import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './StudentSession.css'

const STRUGGLE_LABELS = {
  0: { text: 'Normal', class: 'label-normal' },
  1: { text: 'Phonics issue', class: 'label-phonics' },
  2: { text: 'Spelling issue', class: 'label-spelling' },
  3: { text: 'Visual issue', class: 'label-visual' },
}

const DIFFICULTY_OPTIONS = ['Easy', 'Medium', 'Hard']
const MODE_OPTIONS = ['Visual', 'Audio']

function StudentSession() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [session, setSession] = useState({
    step: 1,
    gamesPlayed: 0,
    accuracy: 0,
    avgTime: 0,
    retryCount: 0,
    struggleClass: 0,
    predictedAccuracy: null,
    riskLevel: null,
    difficulty: 'Medium',
    mode: 'Visual',
  })
  const [gameResult, setGameResult] = useState(null)

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

  const simulatePlayGame = () => {
    setGameResult(null)
    // Simulate: play game → collect metrics → AI runs
    const newGamesPlayed = session.gamesPlayed + 1
    const mockAccuracy = 50 + Math.floor(Math.random() * 45)
    const mockTime = 3 + Math.floor(Math.random() * 8)
    const mockRetry = Math.floor(Math.random() * 4)
    const mockStruggle = Math.floor(Math.random() * 4)
    const mockPredicted = Math.min(95, mockAccuracy + 5 + Math.floor(Math.random() * 15))
    const risk = mockPredicted < 60 ? 'High' : mockPredicted < 75 ? 'Moderate' : 'Low'

    setSession((s) => ({
      ...s,
      step: Math.max(s.step, 2),
      gamesPlayed: newGamesPlayed,
      accuracy: mockAccuracy,
      avgTime: mockTime,
      retryCount: mockRetry,
      struggleClass: mockStruggle,
      predictedAccuracy: mockPredicted,
      riskLevel: risk,
      difficulty: DIFFICULTY_OPTIONS[Math.floor(Math.random() * 3)],
      mode: MODE_OPTIONS[Math.floor(Math.random() * 2)],
    }))
    setGameResult({ accuracy: mockAccuracy, time: mockTime, retries: mockRetry })
  }

  if (!user) return null

  const struggle = STRUGGLE_LABELS[session.struggleClass] || STRUGGLE_LABELS[0]

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Learning Session — {user.name}</h1>
        <button type="button" className="btn-secondary header-btn" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <main className="app-main">
        <div className="session-flow">
          <div className="card session-card">
            <h2>Step {session.step}: {session.step === 1 ? 'Initial assessment' : 'Adapted learning'}</h2>
            <p className="session-desc">
              {session.step === 1
                ? 'Play 3–5 starter games. System will collect accuracy, time, errors & retries, then run the AI layer.'
                : 'Play → Analyze → Predict → Decide → Adapt. Your content is personalized in real time.'}
            </p>
          </div>

          <div className="two-col">
            <div className="card game-engine-card">
              <h3>Game area</h3>
              <div className="current-params">
                <span className="param difficulty">Difficulty: <strong>{session.difficulty}</strong></span>
                <span className="param mode">Mode: <strong>{session.mode}</strong></span>
              </div>
              <p className="game-placeholder">
                Game content is updated here based on DQN action (difficulty + sensory mode).
              </p>
              <button type="button" className="btn-primary play-btn" onClick={simulatePlayGame}>
                {session.gamesPlayed === 0 ? 'Start first game' : 'Play next round'}
              </button>
              {gameResult && (
                <div className="game-result">
                  <p>Last round: Accuracy {gameResult.accuracy}% · Time {gameResult.time}s · Retries {gameResult.retries}</p>
                </div>
              )}
            </div>

            <div className="card ai-panel">
              <h3>AI layer (real-time)</h3>
              <div className="ai-row">
                <span className="ai-label">XGBoost → Struggle type</span>
                <span className={`label-tag ${struggle.class}`}>{struggle.text}</span>
              </div>
              <div className="ai-row">
                <span className="ai-label">MLP → Predicted next accuracy</span>
                <span className="ai-value">{session.predictedAccuracy != null ? `${session.predictedAccuracy}%` : '—'}</span>
              </div>
              <div className="ai-row">
                <span className="ai-label">Risk level</span>
                <span className={`risk-badge risk-${(session.riskLevel || '').toLowerCase()}`}>{session.riskLevel || '—'}</span>
              </div>
              <div className="ai-row">
                <span className="ai-label">DQN → Current action</span>
                <span className="ai-value">{session.difficulty} + {session.mode}</span>
              </div>
              <div className="session-stats">
                <h4>Session stats</h4>
                <p>Accuracy: {session.accuracy}% · Avg time: {session.avgTime}s · Retries: {session.retryCount}</p>
                <p>Rounds played: {session.gamesPlayed}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default StudentSession
