# LogPages API - Complete Authentication System

A complete **Login → OTP → Token** authentication system built with **FastAPI** (Python) and **React**, featuring REST API and WebSocket support.

## Features

- **Complete Authentication Flow:** Login with email/password → OTP verification → JWT tokens
- **OTP System:** 6-digit OTP with 5-minute expiration
- **JWT Tokens:** Access tokens (30 min) and refresh tokens (7 days)
- **WebSocket Support:** Real-time authenticated connections
- **React Frontend:** Beautiful login and OTP verification pages
- **Password Security:** Bcrypt hashing
- **Flexible Storage:** In-memory or Redis for OTP storage
- **API Documentation:** Interactive Swagger UI and Postman collection

---

## Project Structure

```
logpagesandapi/
├── app/
│   ├── api/
│   │   ├── auth.py              # Authentication REST endpoints
│   │   ├── websocket.py         # WebSocket endpoints
│   │   └── dependencies.py      # Auth dependencies
│   ├── models/
│   │   ├── user.py              # User models
│   │   └── auth.py              # Auth models
│   ├── services/
│   │   ├── auth_service.py      # Authentication service
│   │   └── otp_service.py       # OTP generation & verification
│   ├── utils/
│   │   └── security.py          # JWT & password utilities
│   └── config.py                # Application configuration
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx        # Login page
│   │   │   ├── OTP.jsx          # OTP verification page
│   │   │   └── Dashboard.jsx   # Authenticated dashboard
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx # Auth state management
│   │   ├── api/
│   │   │   └── axios.js         # API client
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── docs/
│   └── API_DESIGN.md            # Complete API documentation
├── main.py                      # FastAPI application
├── requirements.txt             # Python dependencies
├── postman_collection.json      # Postman collection
└── README.md
```

---

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **(Optional) Redis** for production OTP storage

### 1. Backend Setup (FastAPI)

```bash
# Navigate to project directory
cd logpagesandapi

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env and set your SECRET_KEY (optional)
# The default values work for development

# Run the backend server
python main.py
```

Backend will be available at: **http://localhost:8000**

API Documentation (Swagger): **http://localhost:8000/docs**

### 2. Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## Usage

### Testing the Authentication Flow

#### 1. Using the React Frontend

1. Open **http://localhost:3000** in your browser
2. Use the test account:
   - **Email:** `test@example.com`
   - **Password:** `secret`
3. Click "Sign In"
4. You'll see an OTP displayed in the message (development mode)
5. Enter the 6-digit OTP
6. You'll be redirected to the Dashboard
7. Test WebSocket connection from the Dashboard

#### 2. Using the API Directly

**Step 1: Login**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secret"}'
```

**Response:**
```json
{
  "need_otp": true,
  "message": "OTP sent to test@example.com. For development: OTP is 123456"
}
```

**Step 2: Get OTP (Development Only)**
```bash
curl http://localhost:8000/auth/dev/otp/test@example.com
```

**Step 3: Verify OTP**
```bash
curl -X POST http://localhost:8000/auth/otp \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "otp": "123456"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Step 4: Access Protected Endpoints**
```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 3. Using Postman

1. Import `postman_collection.json` into Postman
2. The collection includes all endpoints with automatic token management
3. Run requests in order:
   1. Login
   2. Get OTP (Dev Only)
   3. Verify OTP (automatically saves tokens)
   4. Get Current User
   5. Refresh Token
   6. Logout

---

## WebSocket Usage

### Authenticated WebSocket Connection

```javascript
// Connect with access token
const ws = new WebSocket('ws://localhost:8000/ws/auth?token=YOUR_ACCESS_TOKEN')

// Listen for messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('Received:', data)
}

// Send ping
ws.send(JSON.stringify({ type: 'ping' }))

// Request OTP via WebSocket
ws.send(JSON.stringify({ type: 'request_otp' }))

// Verify OTP via WebSocket
ws.send(JSON.stringify({ type: 'verify_otp', otp: '123456' }))
```

### Public WebSocket Connection

```javascript
// Connect without authentication
const ws = new WebSocket('ws://localhost:8000/ws/public')

// Authenticate after connection
ws.send(JSON.stringify({
  type: 'authenticate',
  token: 'YOUR_ACCESS_TOKEN'
}))
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Login with email/password | No |
| POST | `/auth/otp` | Verify OTP and get tokens | No |
| POST | `/auth/refresh` | Refresh access token | No (refresh_token) |
| POST | `/auth/logout` | Logout user | Yes |
| GET | `/auth/me` | Get current user info | Yes |
| GET | `/auth/dev/otp/{email}` | Get OTP (dev only) | No |

### WebSocket

| Endpoint | Description | Auth Required |
|----------|-------------|---------------|
| `/ws/auth?token=TOKEN` | Authenticated WebSocket | Yes (query param) |
| `/ws/public` | Public WebSocket | No |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | API info |

---

## Configuration

Edit `.env` file to configure the application:

```bash
# Application
APP_NAME=LogPages API
DEBUG=True

# Security - CHANGE THIS IN PRODUCTION!
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OTP Settings
OTP_EXPIRE_MINUTES=5
OTP_LENGTH=6

# Redis (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
USE_REDIS=False

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## Security Considerations

### For Production Deployment

1. **Change SECRET_KEY:**
   ```bash
   # Generate a secure secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Enable Redis:**
   - Set `USE_REDIS=True` in `.env`
   - Install and configure Redis server
   - OTP storage in Redis is more secure and scalable

3. **Disable DEBUG mode:**
   - Set `DEBUG=False` in `.env`
   - This will hide OTP in responses

4. **Configure OTP Delivery:**
   - Implement email/SMS delivery in `app/api/auth.py`
   - Replace console logging with actual delivery service

5. **HTTPS Only:**
   - Use HTTPS in production
   - Update WebSocket to use WSS (secure WebSocket)

6. **Database:**
   - Replace in-memory user storage with a real database
   - Update `app/models/user.py` with actual database models

7. **Rate Limiting:**
   - Add rate limiting to prevent brute force attacks
   - Limit OTP generation and verification attempts

---

## Test Account

**Email:** test@example.com
**Password:** secret
**User ID:** user_001

---

## Development

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the built-in runner
python main.py
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Build for Production

```bash
cd frontend
npm run build
```

---

## Documentation

- **API Documentation:** See `docs/API_DESIGN.md` for complete API specification
- **Swagger UI:** http://localhost:8000/docs (when backend is running)
- **Postman Collection:** Import `postman_collection.json`

---

## Architecture

### Authentication Flow

```
┌─────────┐         ┌─────────┐         ┌─────────┐
│ Client  │         │  API    │         │   OTP   │
└────┬────┘         └────┬────┘         └────┬────┘
     │                   │                    │
     │ POST /auth/login  │                    │
     │──────────────────>│                    │
     │                   │  Generate OTP      │
     │                   │───────────────────>│
     │                   │                    │
     │  need_otp=true    │                    │
     │<──────────────────│                    │
     │                   │                    │
     │ POST /auth/otp    │                    │
     │──────────────────>│                    │
     │                   │  Verify OTP        │
     │                   │───────────────────>│
     │                   │  Valid ✓           │
     │                   │<───────────────────│
     │  Tokens           │                    │
     │<──────────────────│                    │
     │                   │                    │
     │ Authenticated     │                    │
     │ Requests          │                    │
     │──────────────────>│                    │
     │                   │                    │
```

### Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- Pydantic - Data validation
- Python-JOSE - JWT implementation
- Passlib + Bcrypt - Password hashing
- Uvicorn - ASGI server
- WebSockets - Real-time communication

**Frontend:**
- React 18 - UI library
- React Router - Routing
- Axios - HTTP client
- Vite - Build tool
- Context API - State management

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in main.py or run on different port
uvicorn main:app --port 8001
```

**Redis connection error:**
```bash
# Disable Redis in .env
USE_REDIS=False
```

### Frontend Issues

**API connection failed:**
- Check if backend is running on port 8000
- Check CORS settings in `.env`
- Verify `VITE_API_URL` in frontend

**WebSocket connection failed:**
- Ensure access_token is valid
- Check WebSocket URL (ws:// not wss:// for local)
- Verify backend WebSocket endpoint is accessible

---

## License

This project is provided as-is for educational and development purposes.

---

## Contributing

Feel free to submit issues and enhancement requests!

---

## Author

Built with FastAPI + React for complete authentication solution.

---

## Next Steps

To extend this project:

1. **Add real database** (PostgreSQL, MongoDB)
2. **Implement email/SMS OTP delivery** (SendGrid, Twilio)
3. **Add user registration endpoint**
4. **Implement password reset flow**
5. **Add social login** (Google, GitHub)
6. **Implement token blacklist** for logout
7. **Add 2FA support** (TOTP, hardware keys)
8. **Create admin panel**
9. **Add rate limiting** (SlowAPI)
10. **Implement logging** and monitoring
