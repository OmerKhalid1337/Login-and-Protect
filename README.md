# Auth Login & Protect API

A secure, production-ready backend authentication API built with **FastAPI** and integrated with **Supabase Auth** as the Identity Provider (IdP). This project implements robust user registration, credential authentication, session termination, token verification, and reusable route guards protected by JSON Web Tokens (JWTs).

---

## 📑 Table of Contents

- [Overview & Architecture](#-overview--architecture)
- [Technologies Used](#-technologies-used)
- [The Authentication Trust Triangle](#-the-authentication-trust-triangle)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone and Install](#1-clone-and-install)
  - [2. Configure Environment](#2-configure-environment)
  - [3. Supabase Auth Configuration](#3-supabase-auth-configuration)
  - [4. Run the Server](#4-run-the-server)
- [API Reference](#-api-reference)
- [Interactive API Docs (Swagger UI)](#-interactive-api-docs-swagger-ui)
- [Manual Testing with cURL](#-manual-testing-with-curl)
- [Security & Best Practices](#-security--best-practices)
- [HTTP Status Codes & Error Handling](#-http-status-codes--error-handling)

---

## 🎯 Overview & Architecture

Modern web security follows a fundamental rule: **Never roll your own authentication or store raw passwords**. This backend relies on **Supabase Auth** as a secure Identity Provider (IdP) to hash credentials, manage user records, and issue cryptographically signed JWT access tokens.

### Key Features
- **User Registration (`POST /auth/signup`)**: Validates input and registers users with Supabase Auth (`201 Created`).
- **User Authentication (`POST /auth/login`)**: Authenticates users and returns signed JWT access tokens and refresh tokens (`200 OK`).
- **Session Logout (`POST /auth/logout`)**: Protected endpoint terminating sessions (`204 No Content`).
- **Token Verification (`GET /protected/profile`)**: Live cryptographic JWT verification via Supabase GoTrue Auth.
- **Reusable Auth Guard (`GET /protected/dashboard`)**: FastAPI dependency injection (`Depends(get_current_user)`) safeguarding multiple endpoints.
- **Public Gate (`GET /public/info`)**: Unprotected endpoint accessible without headers.
- **Interactive Swagger Documentation (`/docs`)**: OpenAPI documentation with configured `HTTPBearer` security lock.

---

## 🛠️ Technologies Used

- **Language:** Python 3.10+
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Web Server:** [Uvicorn](https://www.uvicorn.org/)
- **Identity Provider (IdP):** [Supabase Auth (GoTrue)](https://supabase.com/docs/guides/auth)
- **SDK:** `supabase-py` (v2.x)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Environment Management:** `python-dotenv`
- **Documentation:** OpenAPI & Swagger UI

---

## 📐 The Authentication Trust Triangle

Authentication operates as a secure trust triangle between three parties:

```
                      +-----------------------------+
                      |   Identity Provider (IdP)   |
                      |        (Supabase Auth)      |
                      +-----------------------------+
                        ^                         ^
      1. Credentials    |                         |  4. Live Token
         (Email/Pass)   |                         |     Verification
                        v                         |     (get_user)
                +---------------+                 |
                |    Client     |                 |
                | (Browser/cURL)|                 |
                +---------------+                 v
                        |                 +-----------------+
        3. Request with |                 |  Backend Server |
           Bearer JWT   +---------------->|    (FastAPI)    |
                                          +-----------------+
```

1. **Sign Up / Log In:** The client submits credentials (`email` + `password`) to the backend, which forwards them to Supabase.
2. **Token Issuance:** Supabase verifies credentials and returns a signed JWT **access token**.
3. **Protected Request:** The client includes the token in the `Authorization` header: `Authorization: Bearer <token>`.
4. **Token Verification:** The FastAPI backend extracts the Bearer token and calls Supabase (`supabase.auth.get_user(token)`) to verify its validity before executing route logic.

---

## 📂 Project Structure

```
Login-&-Protect/
├── app/
│   ├── __init__.py           # Application package marker
│   ├── config.py             # Environment loader & Supabase client initialization
│   ├── dependencies.py       # Reusable get_current_user auth guard & HTTPBearer scheme
│   ├── main.py               # FastAPI entrypoint, error handlers & router mounts
│   ├── schemas.py            # Pydantic validation schemas
│   └── routers/
│       ├── __init__.py       # Routers package marker
│       ├── auth.py           # /auth/signup, /auth/login, /auth/logout
│       ├── protected.py      # /protected/profile, /protected/dashboard
│       └── public.py         # /public/info
├── .env.example              # Template with placeholder credentials (committed)
├── .gitignore                # Excludes .env, virtual environments & cache
├── requirements.txt          # Python dependencies
└── README.md                 # Complete project documentation
```

---

## 🚀 Getting Started

Follow these steps to run the API locally in under 3 minutes.

### Prerequisites
- Python 3.10 or higher
- Git
- A free account at [Supabase](https://supabase.com)

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd Login-and-Protect

# Create and activate a virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory by copying `.env.example`:

```bash
cp .env.example .env
```

Populate your `.env` with your Supabase project credentials (found under **Supabase Dashboard -> Project Settings -> API**):

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-supabase-anon-key
PORT=8000
HOST=127.0.0.1
```

> [!WARNING]
> **Never commit your `.env` file or leak your `SUPABASE_KEY` / `service_role` key.** `.gitignore` is already configured to protect your secrets.

### 3. Supabase Auth Configuration

In your **Supabase Dashboard**:
1. Navigate to **Authentication -> Providers -> Email**.
2. Toggle **"Confirm email" OFF** for development testing (this allows newly registered users to log in immediately without waiting for an email verification link).

### 4. Run the Server

Start the FastAPI application with a single command:

```bash
uvicorn app.main:app --reload --port 8000
```

The server will be running at `http://127.0.0.1:8000`.

---

## 📡 API Reference

| Method | Endpoint | Description | Auth Required | Success Status |
| :--- | :--- | :--- | :---: | :---: |
| `GET` | `/` | API status & health check | None | `200 OK` |
| `GET` | `/public/info` | Public open data endpoint | None | `200 OK` |
| `POST` | `/auth/signup` | Create a new user account | None | `201 Created` |
| `POST` | `/auth/login` | Authenticate user & receive JWT | None | `200 OK` |
| `POST` | `/auth/logout` | End active user session | `Bearer <token>` | `204 No Content` |
| `GET` | `/protected/profile` | Read authenticated user profile | `Bearer <token>` | `200 OK` |
| `GET` | `/protected/dashboard` | User dashboard (guard demo) | `Bearer <token>` | `200 OK` |

---

## 📖 Interactive API Docs (Swagger UI)

FastAPI automatically generates interactive OpenAPI documentation at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### How to use Swagger with Bearer Authentication:
1. Open `http://127.0.0.1:8000/docs`.
2. Expand `POST /auth/login`, click **Try it out**, enter your credentials, and click **Execute**.
3. Copy the `access_token` from the JSON response.
4. Scroll to the top right and click the green **Authorize 🔓** button.
5. Paste your token into the **Value** box and click **Authorize**.
6. All protected routes (`/protected/profile`, `/protected/dashboard`, `/auth/logout`) will now automatically include the token when you click **Try it out** -> **Execute**.

---

## 🧪 Manual Testing with cURL

### 1. Register a User (`POST /auth/signup`)
```bash
curl -i -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"developer@example.com","password":"SecurePassword123!"}'
```
*Expected Status:* `201 Created`

### 2. Log In (`POST /auth/login`)
```bash
curl -i -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"developer@example.com","password":"SecurePassword123!"}'
```
*Expected Status:* `200 OK` (returns `access_token` and `refresh_token`).

### 3. Access Public Info (`GET /public/info`)
```bash
curl -i http://127.0.0.1:8000/public/info
```
*Expected Status:* `200 OK`

### 4. Access Protected Profile with Valid Token (`GET /protected/profile`)
```bash
curl -i http://127.0.0.1:8000/protected/profile \
  -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN>"
```
*Expected Status:* `200 OK`

### 5. Access Protected Profile with Tampered / Bad Token
```bash
curl -i http://127.0.0.1:8000/protected/profile \
  -H "Authorization: Bearer invalid.tampered.token"
```
*Expected Status:* `401 Unauthorized` (`{"error": "Invalid or expired token"}`)

### 6. Access Protected Dashboard (`GET /protected/dashboard`)
```bash
curl -i http://127.0.0.1:8000/protected/dashboard \
  -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN>"
```
*Expected Status:* `200 OK`

### 7. Log Out (`POST /auth/logout`)
```bash
curl -i -X POST http://127.0.0.1:8000/auth/logout \
  -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN>"
```
*Expected Status:* `204 No Content`

---

## 🛡️ Security & Best Practices

1. **Zero Secret Leakage:** Supabase `anon` keys and Project URLs are managed through `.env`. The `service_role` secret is never exposed to the client.
2. **Input Validation:** Pydantic models reject missing or empty strings with `400 Bad Request`.
3. **Stateless JWT Verification:** Backend cryptographically checks tokens against Supabase without managing database password tables.
4. **Reusable Guard:** Single source of truth for authentication (`get_current_user`) avoids duplicated code and prevents unguarded endpoints.

### 401 Unauthorized vs. 403 Forbidden
- **401 Unauthorized:** *"I don't know who you are."* The request is missing a token, or the provided token is malformed, expired, or tampered with.
- **403 Forbidden:** *"I know who you are, but you do not have permission to access this resource."* (e.g. standard user attempting to reach an admin-only endpoint).

---

## 📜 Commit History Checklist

This repository contains clean, incremental commits representing each stage of the assignment:

1. `Stage 0: setup server and supabase client`
2. `Stage 1: signup and login routes working`
3. `Stage 2: public route and unverified protected route`
4. `Stage 3: profile route token verification`
5. `Stage 4: auth middleware and logout endpoint`
6. `Stage 5: Swagger UI documentation with bearer auth`
7. `Stage 6: publish to GitHub and write README`
