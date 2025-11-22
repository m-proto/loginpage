# LogPages API 設計書 (API Design Document)

## 概要 (Overview)

FastAPI ベースの認証システム。ログイン → OTP → トークン発行の完全なフローを提供し、REST API と WebSocket の両方をサポート。

**Base URL:** `http://localhost:8000`

---

## 認証フロー (Authentication Flow)

### 新しいフロー (Keycloak連携 - 推奨)

```
1. POST /auth/send-otp (email のみ)
   ↓
2. OTP生成・送信 (ok: true)
   ↓
3. POST /auth/verify-otp (email + OTP)
   ↓
4. Keycloakからトークン取得 (access_token + refresh_token + id_token)
   ↓
5. 認証済みエンドポイント・WebSocket接続
```

### レガシーフロー (既存)

```
1. POST /auth/login (email + password)
   ↓
2. OTP生成・送信 (need_otp: true)
   ↓
3. POST /auth/otp (email + OTP)
   ↓
4. トークン発行 (access_token + refresh_token)
   ↓
5. 認証済みエンドポイント・WebSocket接続
```

---

## エンドポイント一覧 (Endpoints)

### 新エンドポイント (Keycloak連携)

#### 1. OTP送信 (Send OTP)

**Endpoint:** `POST /auth/send-otp`

**説明:** メールアドレスのみでOTPを生成・送信。パスワード不要。

**Request:**
```json
{
  "email": "test@example.com"
}
```

**Response (Success - 200):**
```json
{
  "ok": true,
  "message": "OTP sent"
}
```

**Response (Error - 400):**
```json
{
  "detail": "Invalid email address"
}
```

**認証:** 不要

**備考:**
- OTPは5分間有効
- 開発環境ではコンソールにOTPを出力
- 本番環境ではメールまたはSMSでOTPを送信

---

#### 2. OTP検証 + Keycloakトークン取得 (Verify OTP with Keycloak)

**Endpoint:** `POST /auth/verify-otp`

**説明:** OTPを検証し、Keycloakから直接トークンを取得。

**Request:**
```json
{
  "email": "test@example.com",
  "code": "123456"
}
```

**Response (Success - 200):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI...",
  "token_type": "Bearer",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "scope": "openid email profile"
}
```

**Response (Error - 400):**
```json
{
  "detail": "Invalid or expired OTP"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Failed to obtain token from Keycloak"
}
```

**認証:** 不要

**備考:**
- OTPは1回のみ使用可能
- Keycloakへのパスワード認証には固定のダミーパスワードを使用
- Keycloak側の設定が必要:
  - Realm: myrealm
  - Client: app-backend (confidential)
  - Direct Access Grants: ON
  - Email as username: ON

---

### レガシーエンドポイント (既存の認証フロー)

### 1. ログイン (Login)

**Endpoint:** `POST /auth/login`

**説明:** ユーザー認証の第1ステップ。メールアドレスとパスワードで認証し、OTPを生成。

**Request:**
```json
{
  "email": "test@example.com",
  "password": "secret"
}
```

**Response (Success - 200):**
```json
{
  "need_otp": true,
  "message": "OTP sent to test@example.com. For development: OTP is 123456"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Incorrect email or password"
}
```

**認証:** 不要

**備考:**
- OTPは5分間有効
- 開発環境ではレスポンスにOTPを含む
- 本番環境ではメールまたはSMSでOTPを送信

---

### 2. OTP検証 (Verify OTP)

**Endpoint:** `POST /auth/otp`

**説明:** OTPを検証し、アクセストークンとリフレッシュトークンを発行。

**Request:**
```json
{
  "email": "test@example.com",
  "otp": "123456"
}
```

**Response (Success - 200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Invalid or expired OTP"
}
```

**認証:** 不要

**備考:**
- OTPは1回のみ使用可能
- トークンの有効期限:
  - access_token: 30分
  - refresh_token: 7日間

---

### 3. トークンリフレッシュ (Refresh Token)

**Endpoint:** `POST /auth/refresh`

**説明:** リフレッシュトークンを使用して新しいアクセストークンを取得。

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Success - 200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (Error - 401):**
```json
{
  "detail": "Invalid refresh token"
}
```

**認証:** 不要 (refresh_tokenのみ必要)

---

### 4. ログアウト (Logout)

**Endpoint:** `POST /auth/logout`

**説明:** ログアウト処理。クライアント側でトークンを削除。

**Request:** なし (Bearer Token必要)

**Response (Success - 200):**
```json
{
  "message": "Successfully logged out"
}
```

**認証:** Bearer Token (必須)

**Headers:**
```
Authorization: Bearer {access_token}
```

---

### 5. ユーザー情報取得 (Get Current User)

**Endpoint:** `GET /auth/me`

**説明:** 現在ログインしているユーザーの情報を取得。

**Request:** なし (Bearer Token必要)

**Response (Success - 200):**
```json
{
  "id": "user_001",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2025-01-15T10:30:00"
}
```

**認証:** Bearer Token (必須)

**Headers:**
```
Authorization: Bearer {access_token}
```

---

### 6. ヘルスチェック (Health Check)

**Endpoint:** `GET /health`

**説明:** APIの稼働状況を確認。

**Request:** なし

**Response (Success - 200):**
```json
{
  "status": "healthy"
}
```

**認証:** 不要

---

### 7. 開発用OTP取得 (Development Only)

**Endpoint:** `GET /auth/dev/otp/{email}`

**説明:** 開発環境のみ。指定したメールアドレスのOTPを取得。

**Request:** なし

**Response (Success - 200):**
```json
{
  "email": "test@example.com",
  "otp": "123456"
}
```

**認証:** 不要

**備考:** DEBUG=Trueの場合のみ有効。本番環境では無効化される。

---

## WebSocket エンドポイント

### 1. 認証済みWebSocket接続 (Authenticated WebSocket)

**Endpoint:** `ws://localhost:8000/ws/auth?token={access_token}`

**説明:** 認証済みユーザー専用のWebSocket接続。リアルタイム通信が可能。

**接続方法:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/auth?token=YOUR_ACCESS_TOKEN')
```

**接続時メッセージ (Server → Client):**
```json
{
  "type": "connection_established",
  "message": "Welcome Test User!",
  "user_id": "user_001",
  "timestamp": "2025-01-15T10:30:00"
}
```

**送信可能なメッセージ (Client → Server):**

#### Ping/Pong
```json
{
  "type": "ping"
}
```

**Response:**
```json
{
  "type": "pong",
  "timestamp": "2025-01-15T10:30:00"
}
```

#### OTPリクエスト
```json
{
  "type": "request_otp"
}
```

**Response:**
```json
{
  "type": "otp_generated",
  "message": "OTP generated: 123456",
  "otp": "123456",
  "timestamp": "2025-01-15T10:30:00"
}
```

#### OTP検証
```json
{
  "type": "verify_otp",
  "otp": "123456"
}
```

**Response:**
```json
{
  "type": "otp_verification_result",
  "valid": true,
  "message": "OTP verified successfully",
  "timestamp": "2025-01-15T10:30:00"
}
```

**認証:** Query Parameter に access_token が必須

**エラー処理:**
- トークン未提供: Close code 1008, "Missing token"
- トークン無効: Close code 1008, "Invalid or expired token"
- ユーザー不明: Close code 1008, "User not found"

---

### 2. 公開WebSocket接続 (Public WebSocket)

**Endpoint:** `ws://localhost:8000/ws/public`

**説明:** 認証不要のWebSocket接続。接続後にトークンで認証可能。

**接続方法:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/public')
```

**認証メッセージ (Client → Server):**
```json
{
  "type": "authenticate",
  "token": "YOUR_ACCESS_TOKEN"
}
```

**Response (Success):**
```json
{
  "type": "auth_success",
  "message": "Authentication successful",
  "user": {
    "id": "user_001",
    "email": "test@example.com",
    "full_name": "Test User"
  }
}
```

**Response (Error):**
```json
{
  "type": "auth_error",
  "message": "Invalid token"
}
```

**認証:** 不要 (接続後に認証可能)

---

## セキュリティ (Security)

### JWT トークン

- **Algorithm:** HS256
- **Access Token有効期限:** 30分
- **Refresh Token有効期限:** 7日間
- **Secret Key:** 環境変数で管理 (SECRET_KEY)

### パスワード

- **ハッシュアルゴリズム:** bcrypt
- **ソルト:** 自動生成

### OTP

- **長さ:** 6桁の数字
- **有効期限:** 5分
- **ストレージ:** In-Memory または Redis
- **使用回数:** 1回のみ

### CORS

- **許可オリジン:** 環境変数で設定可能 (ALLOWED_ORIGINS)
- **デフォルト:** http://localhost:3000, http://localhost:5173

---

## エラーレスポンス形式

すべてのエラーレスポンスは以下の形式:

```json
{
  "detail": "エラーメッセージ"
}
```

**主なステータスコード:**
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

---

## テストアカウント

**Email:** test@example.com
**Password:** secret
**Full Name:** Test User
**User ID:** user_001

---

## 環境変数

```bash
# Application
APP_NAME=LogPages API
DEBUG=True

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OTP
OTP_EXPIRE_MINUTES=5
OTP_LENGTH=6

# Redis (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
USE_REDIS=False

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Keycloak
KEYCLOAK_REALM=myrealm
KEYCLOAK_BASE_URL=http://localhost:8080
KEYCLOAK_CLIENT_ID=app-backend
KEYCLOAK_CLIENT_SECRET=change-me
KEYCLOAK_DUMMY_PASSWORD=dummy-password
```

---

## Keycloak設定 (Keycloak Configuration)

新しい認証フロー (POST /auth/send-otp → /auth/verify-otp) を使用する場合、以下のKeycloak設定が必要:

### 前提条件

1. **Realm作成:** `myrealm` という名前のRealmを作成
2. **Client作成:** `app-backend` という名前のClientを作成
   - Access Type: `confidential`
   - Standard Flow Enabled: OFF (オプション)
   - Direct Access Grants Enabled: **ON** (必須)
   - Client Authentication: ON
3. **Client Secret:** Client の Credentials タブから Secret をコピーし、環境変数 `KEYCLOAK_CLIENT_SECRET` に設定
4. **ユーザー作成:**
   - Email を Username として使用 (Email as username を有効化)
   - 各ユーザーにパスワードを設定: 環境変数 `KEYCLOAK_DUMMY_PASSWORD` と同じ値
   - このパスワードはユーザーには知らせず、FastAPI が代理で使用

### 動作の仕組み

1. ユーザーはメールアドレスのみでOTPを要求
2. OTP検証が成功したら、FastAPI が Keycloak に対して **Resource Owner Password Credentials Grant** (Direct Access Grant) を実行
3. Keycloak からトークンを取得し、フロントエンドに返す

### セキュリティ上の注意

- `KEYCLOAK_CLIENT_SECRET` と `KEYCLOAK_DUMMY_PASSWORD` は秘密に保つこと
- 本番環境では環境変数または secrets manager を使用すること
- ダミーパスワードはランダムで強力なものを使用すること

---

## 変更履歴

| Date | Version | Changes |
|------|---------|---------|
| 2025-01-15 | 1.0.0 | 初版リリース - 全エンドポイント実装 |
| 2025-01-22 | 1.1.0 | Keycloak連携エンドポイント追加 (POST /auth/send-otp, POST /auth/verify-otp) |
