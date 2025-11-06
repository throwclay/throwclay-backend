# ---------- Makefile ----------
.PHONY: token token-admin token-auth token-print

PYTHON ?= python

# Defaults (override at call-time: make token TOKEN_ROLE=owner ...)
TOKEN_SUB          ?= local-user-123
TOKEN_EMAIL        ?= test@example.com
TOKEN_ROLE         ?= admin
TOKEN_ROLES        ?= $(TOKEN_ROLE),authenticated
TOKEN_EXP_SECONDS  ?= 86400  # 24h

token:
	@$(PYTHON) - <<'PY'
import os, time
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(usecwd=True))
except Exception:
    pass
try:
    import jwt
except Exception:
    raise SystemExit("PyJWT not installed. Run: pip install PyJWT python-dotenv")
secret = os.environ.get("SUPABASE_JWT_SECRET")
if not secret:
    raise SystemExit("SUPABASE_JWT_SECRET not set; put it in .env or export it")
now = int(time.time())
sub   = os.environ.get("TOKEN_SUB",          "$(TOKEN_SUB)")
email = os.environ.get("TOKEN_EMAIL",        "$(TOKEN_EMAIL)")
role  = os.environ.get("TOKEN_ROLE",         "$(TOKEN_ROLE)")
roles = [r.strip() for r in os.environ.get("TOKEN_ROLES","$(TOKEN_ROLES)").split(",") if r.strip()]
exp_s = int(os.environ.get("TOKEN_EXP_SECONDS","$(TOKEN_EXP_SECONDS)"))
claims = {
    "sub": sub,
    "email": email,
    "role": role,
    "app_metadata": {"roles": roles},
    "iat": now,
    "exp": now + exp_s,
}
print(jwt.encode(claims, secret, algorithm="HS256"))
PY

# Convenience variants
token-admin:
	@$(MAKE) -s token TOKEN_ROLE=admin

token-auth:
	@$(MAKE) -s token TOKEN_ROLE=authenticated TOKEN_ROLES=authenticated
# ---------- end ----------
