import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [otp, setOtp] = useState('')
  const [step, setStep] = useState('email') // 'email' or 'otp'
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleEmailSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setLoading(true)

    try {
      const response = await api.post('/auth/send-otp', {
        email,
      })

      if (response.data.ok) {
        setMessage('OTPコードをメールで送信しました。コンソールを確認してください。')
        setStep('otp')
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 'OTP送信に失敗しました。もう一度お試しください。'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleOtpSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await api.post('/auth/verify-otp', {
        email,
        code: otp,
      })

      // Keycloak tokens received
      const { access_token, refresh_token } = response.data
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)

      // Navigate to test page
      navigate('/test')
    } catch (err) {
      setError(
        err.response?.data?.detail || 'OTP検証に失敗しました。もう一度お試しください。'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleBackToEmail = () => {
    setStep('email')
    setOtp('')
    setError('')
    setMessage('')
  }

  return (
    <div className="container">
      <div className="auth-card">
        <h1>ログイン</h1>
        <p>{step === 'email' ? 'メールアドレスを入力してください' : 'OTPコードを入力してください'}</p>

        {error && <div className="error-message">{error}</div>}
        {message && <div className="success-message" style={{
          padding: '12px',
          backgroundColor: '#d4edda',
          color: '#155724',
          borderRadius: '4px',
          marginBottom: '16px',
          border: '1px solid #c3e6cb'
        }}>{message}</div>}

        {step === 'email' ? (
          <form onSubmit={handleEmailSubmit}>
            <div className="form-group">
              <label htmlFor="email">メールアドレス</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
                autoFocus
              />
            </div>

            <button type="submit" className="btn" disabled={loading}>
              {loading ? '送信中...' : 'OTPを送信'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleOtpSubmit}>
            <div className="form-group">
              <label htmlFor="otp">OTPコード (6桁)</label>
              <input
                type="text"
                id="otp"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="123456"
                maxLength="6"
                pattern="[0-9]{6}"
                required
                autoFocus
              />
            </div>

            <button type="submit" className="btn" disabled={loading}>
              {loading ? '検証中...' : 'ログイン'}
            </button>

            <button
              type="button"
              onClick={handleBackToEmail}
              style={{
                marginTop: '10px',
                background: 'transparent',
                color: '#4a90e2',
                border: 'none',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}
            >
              メールアドレスを変更
            </button>
          </form>
        )}

        <div className="back-link">
          <p style={{ marginTop: '20px', fontSize: '13px', color: '#666' }}>
            テストアカウント: test@example.com
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
