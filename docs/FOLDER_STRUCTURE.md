# Folder Structure

Complete overview of the LogPages API project structure.

```
logpagesandapi/
│
├── app/                                 # Backend application
│   ├── __init__.py
│   ├── config.py                        # Configuration and settings
│   │
│   ├── api/                             # API routes
│   │   ├── __init__.py
│   │   ├── auth.py                      # Authentication endpoints
│   │   ├── websocket.py                 # WebSocket endpoints
│   │   └── dependencies.py              # Route dependencies (auth)
│   │
│   ├── models/                          # Data models
│   │   ├── __init__.py
│   │   ├── user.py                      # User models and fake DB
│   │   └── auth.py                      # Auth request/response models
│   │
│   ├── services/                        # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py              # Authentication service
│   │   └── otp_service.py               # OTP generation/verification
│   │
│   └── utils/                           # Utilities
│       ├── __init__.py
│       └── security.py                  # JWT & password utilities
│
├── frontend/                            # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js                 # API client with interceptors
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx          # Auth state management
│   │   ├── pages/
│   │   │   ├── Login.jsx                # Login page
│   │   │   ├── OTP.jsx                  # OTP verification page
│   │   │   └── Dashboard.jsx            # Authenticated dashboard
│   │   ├── App.jsx                      # Main app component
│   │   ├── main.jsx                     # Entry point
│   │   └── index.css                    # Global styles
│   │
│   ├── index.html
│   ├── package.json                     # Frontend dependencies
│   └── vite.config.js                   # Vite configuration
│
├── docs/                                # Documentation
│   ├── API_DESIGN.md                    # Complete API specification
│   └── FOLDER_STRUCTURE.md              # This file
│
├── main.py                              # FastAPI application entry
├── requirements.txt                     # Python dependencies
├── postman_collection.json              # Postman API collection
│
├── .env.example                         # Environment variables template
├── .gitignore                           # Git ignore rules
└── README.md                            # Project documentation

```

---

## Directory Descriptions

### `/app` - Backend Application

Main FastAPI application directory.

#### `/app/api` - API Routes
- `auth.py` - REST endpoints for authentication (login, OTP, refresh, logout)
- `websocket.py` - WebSocket endpoints for real-time communication
- `dependencies.py` - FastAPI dependencies for authentication

#### `/app/models` - Data Models
- `user.py` - User models (UserBase, UserCreate, UserInDB, User)
- `auth.py` - Authentication models (Token, LoginRequest, OTPRequest, etc.)

#### `/app/services` - Business Logic
- `auth_service.py` - User authentication, token creation/verification
- `otp_service.py` - OTP generation, storage, and verification

#### `/app/utils` - Utilities
- `security.py` - Password hashing (bcrypt) and JWT token utilities

#### `/app/config.py`
- Application configuration using Pydantic Settings
- Loads from environment variables

---

### `/frontend` - React Frontend

React application built with Vite.

#### `/frontend/src/api`
- `axios.js` - Axios instance with request/response interceptors for token management

#### `/frontend/src/contexts`
- `AuthContext.jsx` - React Context for global authentication state

#### `/frontend/src/pages`
- `Login.jsx` - Email/password login form
- `OTP.jsx` - 6-digit OTP verification form
- `Dashboard.jsx` - Protected dashboard with WebSocket demo

---

### `/docs` - Documentation

Complete project documentation.

- `API_DESIGN.md` - Full API specification in Japanese
- `FOLDER_STRUCTURE.md` - This file

---

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization and route registration |
| `requirements.txt` | Python backend dependencies |
| `frontend/package.json` | Node.js frontend dependencies |
| `.env.example` | Template for environment variables |
| `postman_collection.json` | Postman collection for API testing |
| `README.md` | Complete project setup and usage guide |

---

## Adding New Features

### Adding a New API Endpoint

1. Create route function in appropriate file in `/app/api/`
2. Define request/response models in `/app/models/`
3. Implement business logic in `/app/services/`
4. Register route in `main.py` if needed

### Adding a New Frontend Page

1. Create new component in `/frontend/src/pages/`
2. Add route in `/frontend/src/App.jsx`
3. Update navigation if needed

### Adding a New Service

1. Create new service file in `/app/services/`
2. Export service instance
3. Import in routes that need it

---

## Import Conventions

### Backend (Python)

```python
# From config
from app.config import settings

# From models
from app.models.user import User, UserInDB
from app.models.auth import Token, LoginRequest

# From services
from app.services.auth_service import auth_service
from app.services.otp_service import otp_service

# From utils
from app.utils.security import create_access_token, verify_password

# From dependencies
from app.api.dependencies import get_current_user
```

### Frontend (JavaScript)

```javascript
// From contexts
import { useAuth } from '../contexts/AuthContext'

// From API
import api from '../api/axios'

// From React Router
import { useNavigate, useLocation } from 'react-router-dom'
```

---

## Development Workflow

1. **Backend changes:** Edit files in `/app`, server auto-reloads
2. **Frontend changes:** Edit files in `/frontend/src`, Vite auto-reloads
3. **API changes:** Update `/docs/API_DESIGN.md`
4. **New dependencies:**
   - Backend: Add to `requirements.txt`, run `pip install -r requirements.txt`
   - Frontend: Run `npm install package-name`

---

## Environment Files

### Backend `.env`

Located at project root. Copy from `.env.example`.

```
APP_NAME=LogPages API
DEBUG=True
SECRET_KEY=your-secret-key
...
```

### Frontend `.env` (optional)

Located at `/frontend/.env` if needed.

```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## Build Outputs

### Backend

No build step required. Run directly with:
```bash
python main.py
```

### Frontend

Build for production:
```bash
cd frontend
npm run build
```

Output: `/frontend/dist/`
