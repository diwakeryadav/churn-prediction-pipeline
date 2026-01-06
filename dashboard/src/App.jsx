import React, {useState} from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'


export default function App(){
  const [txCount, setTxCount] = useState(10)
  const [txSum, setTxSum] = useState(500)
  const [txMean, setTxMean] = useState(50)
  const [daysSinceLast, setDaysSinceLast] = useState(7)
  const [score, setScore] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

  const submit = async () => {
    setLoading(true)
    try {
      const payload = { features: [Number(txCount), Number(txSum), Number(txMean), Number(daysSinceLast)] }
      const res = await axios.post(`${apiBase}/predict/churn`, payload)
      const s = res.data.churn_score
      setScore(s)
      const t = new Date().toLocaleTimeString()
      setHistory(h => [...h.slice(-99), { time: t, score: +(s*100).toFixed(2) }])
    } catch (err) {
      console.error(err)
      alert('Error calling API: ' + (err.response?.data?.detail || err.message))
    } finally { setLoading(false) }
  }

  return (
    <div style={{padding:20, fontFamily: 'Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial'}}>
      <header style={{marginBottom:16}}>
        <h1 style={{fontSize:22, margin:0}}>Analytics — Churn Demo</h1>
        <p style={{color:'#666', marginTop:6}}>Submit a feature vector and view churn score history.</p>
      </header>

      <main style={{display:'grid', gridTemplateColumns:'300px 1fr', gap:16}}>
        <section style={{padding:12, background:'#fff', borderRadius:8, boxShadow:'0 1px 4px rgba(0,0,0,0.06)'}}>
          <h2 style={{marginTop:0}}>Input features</h2>
          <label style={{fontSize:12}}>tx_count</label>
          <input style={{width:'100%', marginBottom:8, padding:8}} value={txCount} onChange={e=>setTxCount(e.target.value)} />
          <label style={{fontSize:12}}>tx_sum</label>
          <input style={{width:'100%', marginBottom:8, padding:8}} value={txSum} onChange={e=>setTxSum(e.target.value)} />
          <label style={{fontSize:12}}>tx_mean</label>
          <input style={{width:'100%', marginBottom:8, padding:8}} value={txMean} onChange={e=>setTxMean(e.target.value)} />
          <label style={{fontSize:12}}>days_since_last</label>
          <input style={{width:'100%', marginBottom:12, padding:8}} value={daysSinceLast} onChange={e=>setDaysSinceLast(e.target.value)} />
          <button style={{width:'100%', padding:10, background:'#2563eb', color:'#fff', border:'none', borderRadius:6}} onClick={submit} disabled={loading}>{loading ? 'Predicting...' : 'Predict churn'}</button>
          {score !== null && (
            <div style={{marginTop:12, padding:10, background:'#f3f4f6', borderRadius:6}}>Churn score: <strong>{(score*100).toFixed(2)}%</strong></div>
          )}
        </section>

        <section style={{padding:12, background:'#fff', borderRadius:8, boxShadow:'0 1px 4px rgba(0,0,0,0.06)'}}>
          <h2 style={{marginTop:0}}>Churn score history</h2>
          <div style={{width:'100%', height:320}}>
            <ResponsiveContainer>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey ="time"/>
                <YAxis domain={[0,100]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#8884d8" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>
      </main>

      <footer style={{marginTop:12, fontSize:12, color:'#777'}}>Note: This demo posts to <code>{apiBase}/predict/churn</code></footer>
    </div>
  )
}
