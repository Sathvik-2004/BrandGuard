import { useState, useEffect } from 'react'
import axios from 'axios'

interface Mention {
  id: number
  source: string
  source_id: string
  author: string
  text: string
  url: string
  published_at: string
  sentiment: string | null
  reach: number | null
  cluster_id: number | null
}

interface Alert {
  id: number
  alert_type: string
  message: string
  created_at: string
  resolved: boolean
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/mentions'

function App() {
  const [mentions, setMentions] = useState<Mention[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [wsConnected, setWsConnected] = useState(false)
  const [loading, setLoading] = useState(true)

  // Fetch initial mentions and alerts from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [mentionsResponse, alertsResponse] = await Promise.all([
          axios.get(`${API_BASE}/api/mentions`),
          axios.get(`${API_BASE}/api/alerts`)
        ])
        setMentions(mentionsResponse.data)
        setAlerts(alertsResponse.data)
      } catch (error) {
        console.error('Failed to fetch data:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  // WebSocket connection for live updates
  useEffect(() => {
    const ws = new WebSocket(WS_URL)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setWsConnected(true)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data?.type === 'mention' && data.mention) {
          // Add new mention to the top of the list
          setMentions(prev => [data.mention, ...prev])
        } else if (data?.type === 'alert' && data.alert) {
          // Add new alert to the top of the list
          setAlerts(prev => [data.alert, ...prev])
        }
      } catch (error) {
        console.log('Non-JSON message received:', event.data)
      }
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setWsConnected(false)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setWsConnected(false)
    }

    return () => {
      ws.close()
    }
  }, [])

  const getSentimentClass = (sentiment: string | null) => {
    if (!sentiment) return 'sentiment-neutral'
    switch (sentiment.toLowerCase()) {
      case 'positive': return 'sentiment-positive'
      case 'negative': return 'sentiment-negative'
      default: return 'sentiment-neutral'
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="App">
      <h1>🛡️ BrandGuard</h1>
      <p>Real-time Brand Mention & Reputation Tracker</p>
      
      <div className="dashboard">
        <div className="mentions-panel">
          <h2>Recent Mentions</h2>
          {loading ? (
            <p>Loading mentions...</p>
          ) : mentions.length === 0 ? (
            <p>No mentions found. Run the ingestion scripts to populate data.</p>
          ) : (
            <div className="mentions-list">
              {mentions.map((mention: Mention) => (
                <div key={mention.id} className="mention-card">
                  <div className="mention-header">
                    <span className="source">{mention.source}</span>
                    <span className={`sentiment-badge ${getSentimentClass(mention.sentiment)}`}>
                      {mention.sentiment || 'neutral'}
                    </span>
                  </div>
                  <p className="mention-text">{mention.text}</p>
                  <div className="mention-meta">
                    <small>By: {mention.author || 'Unknown'}</small>
                    {mention.published_at && (
                      <small> • {formatTimestamp(mention.published_at)}</small>
                    )}
                    {mention.reach && (
                      <small> • Reach: {Math.round(mention.reach)}</small>
                    )}
                    {mention.cluster_id !== null && (
                      <small> • Topic: {mention.cluster_id}</small>
                    )}
                  </div>
                  {mention.url && (
                    <a href={mention.url} target="_blank" rel="noopener noreferrer">
                      View Source
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="live-panel">
          <h2>
            <span className={`status-indicator ${wsConnected ? 'status-connected' : 'status-disconnected'}`}></span>
            Live Feed
          </h2>
          <p className="connection-status">
            {wsConnected ? 'Connected' : 'Disconnected'} • {mentions.length} total mentions
          </p>
          <div className="live-feed">
            {mentions.length === 0 ? (
              <p>No mentions yet. Create a mention via API to see real-time updates.</p>
            ) : (
              mentions.slice(0, 5).map((mention: Mention) => (
                <div key={mention.id} className="mention-card">
                  <p>{mention.text}</p>
                  <small>
                    {mention.sentiment && `${mention.sentiment} • `}
                    {mention.cluster_id !== null && `Topic: ${mention.cluster_id} • `}
                    {formatTimestamp(mention.published_at)}
                  </small>
                </div>
              ))
            )}
          </div>

          <h3 style={{ marginTop: '2rem' }}>🚨 Alerts</h3>
          <div className="alerts-feed">
            {alerts.length === 0 ? (
              <p>No alerts yet. Alerts will appear when spikes are detected.</p>
            ) : (
              alerts.slice(0, 5).map((alert: Alert) => (
                <div key={alert.id} className={`alert-card alert-${alert.alert_type}`}>
                  <div className="alert-header">
                    <strong>{alert.alert_type.replace('_', ' ').toUpperCase()}</strong>
                  </div>
                  <p>{alert.message}</p>
                  <small>{formatTimestamp(alert.created_at)}</small>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App