# LogPages API - Authentification OTP + Keycloak

Système d'authentification moderne : **Email OTP → Keycloak → JWT**

---

## 🚀 Installation rapide

### 1. Keycloak (Docker)

```bash
docker run -d --name keycloak -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
```

**Accès** : http://localhost:8080 (admin/admin)

**Configuration** :
1. Crée Realm : `myrealm`
2. Crée Client : `app-backend` (Client auth: ON, Direct grants: ON)
3. Note le Client Secret
4. Crée un user avec email = username, password = `dummy-password`

---

### 2. Backend (FastAPI)

```bash
# Installe les dépendances
pip install -r requirements.txt

# Configure .env
cp .env.example .env
```

**Édite `.env` :**
- `SMTP_EMAIL` : Ton Gmail
- `SMTP_PASSWORD` : [App Password Gmail](https://myaccount.google.com/apppasswords)
- `KEYCLOAK_CLIENT_SECRET` : Client secret de Keycloak

**Lance :**
```bash
python main.py
```

Backend : http://localhost:8000

---

### 3. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Frontend : http://localhost:5173

---

### 4. Test

1. Ajoute ton email dans `app/data/invited_users.json`
2. Va sur http://localhost:5173
3. Entre ton email → Reçois OTP par Gmail
4. Entre le code OTP → Connecté !

---

## 🔧 Commandes utiles

**Keycloak :**
```bash
docker stop keycloak        # Arrêter
docker start keycloak       # Redémarrer
docker logs keycloak -f     # Voir logs
```

**Backend :**
```bash
python main.py              # Lancer
```

**Frontend :**
```bash
cd frontend && npm run dev  # Lancer
```

---

## 📚 Documentation

- **API** : `docs/API_DESIGN.md`
- **Gmail Setup** : `docs/GMAIL_SETUP.md`
- **Structure** : `STRUCTURE_CLEAN.md`

---

## 🛠️ Stack

- **Backend** : FastAPI + httpx
- **Frontend** : React + Vite
- **Auth** : Keycloak + Gmail SMTP
