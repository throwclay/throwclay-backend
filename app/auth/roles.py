# apps/api/app/auth/roles.py
from fastapi import Depends, HTTPException
from .deps import get_current_user, AuthUser

def require_roles_all(*expected: str):
    expected = {r.lower() for r in expected}
    async def dep(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if not expected.issubset(user.roles):
            raise HTTPException(status_code=403, detail="Forbidden (missing required role)")
        return user
    return dep

def require_roles_any(*expected: str):
    expected = {r.lower() for r in expected}
    async def dep(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.roles.isdisjoint(expected):
            raise HTTPException(status_code=403, detail="Forbidden (insufficient role)")
        return user
    return dep
