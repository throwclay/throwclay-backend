# Setup env

> python3 -m venv .venv
> source .venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt

# Run app

> uvicorn app.main:app --reload --port 8000

# Generate token for protected routes

1. Generate default token

   > make token

2. Convenice targets

   > make token-admin # role=admin, roles=[admin, authenticated]
   > make token-auth # role=authenticated, roles=[authenticated]

3. Override claims at call time

   > make token TOKEN_ROLE=owner TOKEN_ROLES="owner,authenticated" TOKEN_EMAIL="alice@studio.com" TOKEN_SUB="user-123" TOKEN_EXP_SECONDS=7200
   > make token-auth PYTHON=.venv/bin/python

4. Use the token
   > curl -H "Authorization: Bearer <PASTE_JWT_HERE>" http://localhost:8000/protected/route

# For protected routes, used token (example)

TOKEN=$(make -s token)
curl -s -X POST http://127.0.0.1:8000/api/studios \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"name":"Demo Studio","subdomain":"demo","timezone":"America/Los_Angeles"}' | jq

# Get studios

> curl http://localhost:8000/api/studios/demo
