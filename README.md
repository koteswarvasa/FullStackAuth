# FullStackAuth

A full-stack authentication application built with **React, FastAPI, and Microsoft SQL Server**. The project is designed to implement secure user registration, login, session management, and password recovery.

## Project Overview

FullStackAuth provides a foundation for a secure authentication system with a React frontend, Python FastAPI backend, and SQL Server database.

### Key Features

- User registration
- User login and authentication
- Password hashing using bcrypt
- JWT access token generation and validation
- Refresh token management
- HTTP-only cookie for refresh token storage
- Role-based access control foundation
- User session tracking
- Protected dashboard and profile endpoint
- SQL Server database integration
- Environment-based configuration

**Planned enhancements**
- Registration confirmation emails
- Successful login notification emails
- Forgot-password and reset-password workflow
- Password reset email delivery

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| API Documentation | Swagger UI, OpenAPI |
| Database | Microsoft SQL Server |
| ORM | SQLAlchemy |
| Database Driver | pyodbc |
| Authentication | JWT access tokens, refresh tokens |
| Password Security | bcrypt |
| Configuration | python-dotenv |
| Version Control | Git, GitHub |

## Project Structure


FullStackAuth/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── routes/
│   │   ├── security/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── .env
│   ├── .gitignore
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   ├── routes/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env
│   └── package.json
├── database/
│   └── FullStackAuthDB.txt
├── .gitignore
└── README.md

The structure above is illustrative. Keep the actual filenames and folders in your repository consistent with your implementation.

## Prerequisites

Install the following before running the application:

- Python 3.10 or a compatible version for the installed dependencies
- Node.js and npm
- Microsoft SQL Server
- Microsoft ODBC Driver for SQL Server
- Git

## Database Setup

1. Open SQL Server Management Studio (SSMS).
2. Connect to your SQL Server instance.
3. Open `database/FullStackAuthDB.txt`.
4. Review the SQL scripts and execute them in the correct order.
5. Verify that the database, schemas, tables, constraints, indexes, and required seed data have been created.

Do not execute database creation scripts repeatedly against an existing database unless they are designed to be rerun safely.

## Backend Setup

Open a terminal in the `backend` directory.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can activate it from Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `backend` directory using your own local configuration.

Example:

```env
DB_SERVER=YOUR_SQL_SERVER_INSTANCE
DB_NAME=FullStackAuthDB
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_TRUSTED_CONNECTION=yes

JWT_SECRET_KEY=YOUR_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Replace the example values with your actual configuration. Do not commit your real `.env` file or secret keys to GitHub.

### 5. Start the backend

From the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

Backend base URL:

```text
http://127.0.0.1:8000
```

### 6. Open API documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Alternative API documentation:

```text
http://127.0.0.1:8000/redoc
```

## Frontend Setup

Open another terminal in the `frontend` directory.

### 1. Install dependencies

```bash
npm install
```

### 2. Configure the API URL

Create a `.env` file inside the `frontend` directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

This variable contains the backend API base URL, not a database password or JWT secret.

### 3. Start the React application

```bash
npm run dev
```

Open the local URL printed by Vite in your terminal, typically:

```text
http://localhost:5173
```

## Authentication Flow

### Registration

1. The user submits registration details.
2. FastAPI validates the request.
3. The password is hashed before storage.
4. The user and assigned role are saved in SQL Server.

### Login

1. The user submits their username and password.
2. The backend verifies the credentials.
3. A user session is created.
4. An access token is generated.
5. A refresh token is issued through an HTTP-only cookie.
6. The frontend navigates to the protected dashboard.

### Protected API Requests

1. The frontend sends the access token in the `Authorization` header.
2. FastAPI validates the token.
3. The backend checks the user and associated session.
4. The request is accepted only if the authentication checks pass.

## Database Design

The database uses separate schemas to organize application and audit-related data.

### APP Schema

- `APP.USER` — user account details
- `APP.ROLE` — application roles
- `APP.USER_ROLE` — user-to-role relationships
- `APP.USER_SESSION` — login sessions and refresh-token metadata

### AUDIT Schema

Contains audit-related tables for recording application and authentication events, as implemented in the database scripts.

Refer to `database/FullStackAuthDB.txt` for the actual database definition.

## Security Considerations

- Never store plaintext passwords.
- Never commit `.env` files or credentials.
- Use a strong, randomly generated JWT secret.
- Keep refresh tokens in HTTP-only cookies.
- Validate tokens and session status on protected endpoints.
- Use HTTPS in production.
- Configure CORS for trusted frontend origins.
- Avoid exposing sensitive authentication errors.
- Use a secure email provider when implementing email notifications and password reset.
- Do not log passwords, access tokens, refresh tokens, or password-reset tokens.

## Git Workflow

The project uses separate branches to keep stable code apart from ongoing development.

- `main` — stable, tested code
- `develop` — integration and testing
- `feature/*` — individual features and enhancements
- `fix/*` — bug fixes

Recommended workflow:

1. Create a feature branch from `develop`.
2. Implement and test your changes.
3. Commit and push the feature branch.
4. Open a Pull Request into `develop`.
5. Merge tested changes into `main` through a Pull Request when ready for release.

Use meaningful commit messages to make project history easier to understand.

## Future Enhancements

- Registration confirmation emails
- Login notification emails
- Secure forgot-password and reset-password flow
- Email verification
- Automated testing
- Improved audit logging
- Production deployment and monitoring

## Author

FullStackAuth — a full-stack authentication project developed for learning and applying industry-oriented application architecture.
