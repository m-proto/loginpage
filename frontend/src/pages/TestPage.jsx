import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'

function TestPage() {
  const navigate = useNavigate()
  const [userInfo, setUserInfo] = useState(null)

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token')
    if (!token) {
      navigate('/login')
      return
    }

    // You can decode the JWT token to show user info
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      setUserInfo(payload)
    } catch (err) {
      console.error('Failed to decode token:', err)
    }
  }, [navigate])

  const handleLogout = () => {
    // Clear tokens
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')

    // Navigate to login page
    navigate('/login')
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      {/* Header with logout button */}
      <header style={{
        backgroundColor: 'white',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        padding: '16px 24px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: '24px', color: '#333' }}>
          テストページ
        </h1>

        <button
          onClick={handleLogout}
          style={{
            padding: '10px 20px',
            backgroundColor: '#e74c3c',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'background-color 0.3s'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#c0392b'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#e74c3c'}
        >
          ログアウト
        </button>
      </header>

      {/* Main content */}
      <main style={{
        maxWidth: '1200px',
        margin: '40px auto',
        padding: '0 24px'
      }}>
        <div style={{
          backgroundColor: 'white',
          borderRadius: '8px',
          padding: '32px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginTop: 0, color: '#2c3e50' }}>
            ログイン成功！
          </h2>

          <p style={{ color: '#666', fontSize: '16px', lineHeight: '1.6' }}>
            Keycloak認証を使用したOTPログインに成功しました。
          </p>

          {userInfo && (
            <div style={{
              marginTop: '24px',
              padding: '20px',
              backgroundColor: '#f8f9fa',
              borderRadius: '6px',
              border: '1px solid #dee2e6'
            }}>
              <h3 style={{ marginTop: 0, color: '#495057' }}>トークン情報:</h3>
              <pre style={{
                backgroundColor: '#fff',
                padding: '16px',
                borderRadius: '4px',
                overflow: 'auto',
                fontSize: '13px',
                border: '1px solid #e9ecef'
              }}>
                {JSON.stringify(userInfo, null, 2)}
              </pre>
            </div>
          )}

          <div style={{
            marginTop: '32px',
            padding: '20px',
            backgroundColor: '#e8f4f8',
            borderRadius: '6px',
            border: '1px solid #b8dae6'
          }}>
            <h3 style={{ marginTop: 0, color: '#0c5460' }}>認証フロー:</h3>
            <ol style={{ color: '#0c5460', lineHeight: '1.8' }}>
              <li>メールアドレスを入力</li>
              <li>OTPコードがサーバーで生成される（開発環境ではコンソールに表示）</li>
              <li>OTPコードを入力</li>
              <li>Keycloakからトークンを取得</li>
              <li>このテストページにリダイレクト</li>
            </ol>
          </div>

          <div style={{ marginTop: '24px', textAlign: 'center' }}>
            <p style={{ color: '#999', fontSize: '14px' }}>
              右上の「ログアウト」ボタンを押すとログイン画面に戻ります。
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default TestPage
