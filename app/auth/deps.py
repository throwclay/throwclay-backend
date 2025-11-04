# apps/api/app/auth/deps.py
from fastapi import Depends, Header, HTTPException
import jwt
from datetime import datetime, timezone
from ..settings import settings

class AuthUser(dict):
    @property
    def id(self): return self.get("sub")
    @property
    def email(self): return self.get("email")
    @property
    def roles(self) -> set[str]:
        # Try app_metadata.roles (array)
        roles = []
        app_meta = self.get("app_metadata") or {}
        if isinstance(app_meta.get("roles"), list):
            roles.extend([str(r).lower() for r in app_meta["roles"]])

        # Fallback to single 'role' claim
        if "role" in self:
            roles.append(str(self["role"]).lower())

        return set(r for r in roles if r)

def get_current_user(authorization: str | None = Header(None, alias="Authorization")) -> AuthUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1]

    if not settings.supabase_jwt_secret:
        raise HTTPException(status_code=500, detail="Auth not configured")

    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"require": ["exp", "iat"]},
        )
        now = datetime.now(timezone.utc).timestamp()
        if payload.get("exp") and now > payload["exp"]:
            raise HTTPException(status_code=401, detail="Token expired")
        return AuthUser(payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
