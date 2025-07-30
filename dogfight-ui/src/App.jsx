import { useState } from 'react'
import './App.css'

function App() {
  const [gameState, setGameState] = useState('ready') // 'ready', 'fighting', 'finished'
  const [combatResults, setCombatResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const startDogfight = async () => {
    setLoading(true)
    setError(null)
    setGameState('fighting')
    
    try {
      const response = await fetch('http://localhost:8000/dogfight/exchange/500/5')
      
      if (!response.ok) {
        throw new Error('Failed to connect to game server')
      }
      
      const data = await response.json()
      setCombatResults(data)
      setGameState('finished')
    } catch (err) {
      setError(err.message)
      setGameState('ready')
    } finally {
      setLoading(false)
    }
  }

  const resetGame = () => {
    setGameState('ready')
    setCombatResults(null)
    setError(null)
  }

  const FighterCard = ({ fighter, fighterName, isWinner }) => (
    <div className={`fighter-card ${isWinner ? 'winner' : ''}`}>
      <div className="fighter-header">
        <h3>{fighterName}</h3>
        {isWinner && <div className="winner-badge">WINNER!</div>}
      </div>
      
      <div className="fighter-plane">✈️</div>
      
      <div className="stats">
        <div className="stat">
          <span className="stat-label">Ammo</span>
          <div className="stat-bar">
            <div 
              className="stat-fill ammo" 
              style={{ width: `${(fighter[0] / 500) * 100}%` }}
            ></div>
            <span className="stat-value">{fighter[0]}/500</span>
          </div>
        </div>
        
        <div className="stat">
          <span className="stat-label">Health</span>
          <div className="stat-bar">
            <div 
              className="stat-fill health" 
              style={{ width: `${(fighter[1] / 5) * 100}%` }}
            ></div>
            <span className="stat-value">{fighter[1]}/5</span>
          </div>
        </div>
        
        <div className="combat-info">
          <div className={`hit-indicator ${fighter[2] ? 'hit' : 'miss'}`}>
            {fighter[2] ? '🎯 HIT!' : '❌ MISS'}
          </div>
          <div className="damage">
            Damage: {fighter[3] || 0}
          </div>
        </div>
      </div>
    </div>
  )

  return (
    <div className="game-container">
      <div className="game-header">
        <h1 className="game-title">
          <span className="title-text">DOGFIGHT</span>
          <span className="title-subtitle">AERIAL COMBAT</span>
        </h1>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {gameState === 'ready' && (
        <div className="ready-screen">
          <div className="ready-content">
            <div className="planes-animation">
              <div className="plane plane-1">✈️</div>
              <div className="vs-text">VS</div>
              <div className="plane plane-2">✈️</div>
            </div>
            <p className="ready-text">Two pilots enter the arena. Only one will emerge victorious!</p>
            <button 
              className="start-button" 
              onClick={startDogfight}
              disabled={loading}
            >
              {loading ? 'ENGAGING...' : 'START DOGFIGHT'}
            </button>
          </div>
        </div>
      )}

      {gameState === 'fighting' && (
        <div className="fighting-screen">
          <div className="fighting-animation">
            <div className="explosion">💥</div>
            <div className="fighting-text">COMBAT IN PROGRESS...</div>
          </div>
        </div>
      )}

      {gameState === 'finished' && combatResults && (
        <div className="results-screen">
          <div className="results-header">
            <h2>COMBAT RESULTS</h2>
          </div>
          
          <div className="fighters-container">
            <FighterCard 
              fighter={combatResults.fighter1} 
              fighterName="PILOT ALPHA"
              isWinner={combatResults.fighter1[1] > combatResults.fighter2[1]}
            />
            
            <div className="vs-divider">VS</div>
            
            <FighterCard 
              fighter={combatResults.fighter2} 
              fighterName="PILOT BRAVO"
              isWinner={combatResults.fighter2[1] > combatResults.fighter1[1]}
            />
          </div>
          
          <button className="play-again-button" onClick={resetGame}>
            PLAY AGAIN
          </button>
        </div>
      )}
    </div>
  )
}

export default App