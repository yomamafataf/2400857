# OWASP C7 Password Policy Lab

A concise Flask and PostgreSQL web application demonstrating the OWASP Top 10
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

## Test

```powershell
python -m unittest discover -s tests -v
docker compose ps
```
