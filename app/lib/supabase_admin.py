# apps/api/app/lib/supabase_admin.py
import os, httpx

PROJECT_REF = os.getenv("SUPABASE_PROJECT_REF")  # e.g. ullbvuwrfliosmwtavlp
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
BASE = f"https://{PROJECT_REF}.supabase.co"

HEADERS = {
    "apikey": SERVICE_KEY or "",
    "Authorization": f"Bearer {SERVICE_KEY}" if SERVICE_KEY else "",
    "Content-Type": "application/json",
}

async def admin_create_user(email: str) -> dict:
    """
    Creates a user (no password). You can also send invites via /admin/invite if enabled.
    Returns JSON including 'id'.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE}/auth/v1/admin/users", headers=HEADERS, json={"email": email})
        # If user exists, may return 422/409; TODO: decide how to handle in service.
        r.raise_for_status()
        return r.json()

async def admin_invite_user(email: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE}/auth/v1/admin/invite", headers=HEADERS, json={"email": email})
        r.raise_for_status()
        return r.json()
