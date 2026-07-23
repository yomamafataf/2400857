# OWASP C7 Password Policy Lab

A concise Nginx, Flask, and PostgreSQL web application demonstrating the OWASP Top 10
Proactive Controls 2024 C7 password requirements without MFA.

## Password policy

- Minimum 10 characters because MFA is not enabled.
- Printable ASCII characters, including spaces, are accepted.
- No arbitrary uppercase, number, or symbol composition rule.
- Passwords found in the SecLists NCSC common-password file are rejected.
- The browser checks first, and the server repeats every check before accepting
  an account.

## Run

```powershell
docker compose up -d --build
```

Open <https://127.0.0.1>. The browser will warn about the local self-signed
certificate.

The PostgreSQL table `"2400857"` stores only the username and creation time.
Submitted passwords are not persisted.

## Continuous integration

`.github/workflows/ci.yml` runs an ESLint security scan, a Python dependency
audit, HTTP integration checks, and Playwright UI tests. CI uses
`docker-compose.ci.yml` to expose only the internal Flask service at
`http://127.0.0.1:8000`; the normal local stack continues to use Nginx and
HTTPS.
