# Admin Role: Env Var Bootstrap + DB Fallback Pattern

**Learned:** 2026-05-28 | **Project:** TravelPlannerV2

---

## What it is
A two-layer admin check that survives server restarts and lets you add admins dynamically via UI — without ever locking yourself out.

- **Layer 1 (env var):** `ADMIN_EMAILS=you@example.com` in Railway/Vercel env — always wins, can't be revoked via UI. Bootstrap safety net.
- **Layer 2 (DB flag):** `users.is_admin = True` — set via admin panel, survives after env var check fails.

---

## How it works

### Backend — FastAPI `_require_admin()`

```python
_ADMIN_EMAILS = set(
    e.strip().lower()
    for e in os.getenv("ADMIN_EMAILS", "you@example.com").split(",")
    if e.strip()
)

def _require_admin(email: str, db: Session = None):
    if email.lower() in _ADMIN_EMAILS:   # fast path — no DB hit
        return
    if db is not None:
        user = db.get(User, email.lower())
        if user and user.is_admin:        # DB fallback
            return
    raise HTTPException(status_code=403, detail="Forbidden")
```

Always pass `db` when calling it so the fallback works:
```python
_require_admin(caller_email, db)   # ✅
_require_admin(caller_email)       # ❌ DB fallback never runs
```

### Frontend — Next.js `isAdminUser()`

```typescript
// app/lib/admin.ts
export async function isAdminUser(email: string | null | undefined): Promise<boolean> {
  if (!email) return false;
  if (isAdminEmail(email)) return true;   // env var fast path, no fetch
  try {
    const r = await fetch(`${BACKEND}/user/me?user_email=${encodeURIComponent(email)}`, { cache: "no-store" });
    if (!r.ok) return false;
    return (await r.json()).is_admin === true;
  } catch { return false; }
}
```

Use in every server page/layout instead of the sync `isAdminEmail()`:
```tsx
const isAdmin = await isAdminUser(userEmail);
```

### Auto-sync on first message (streaming endpoint)

When an env-var admin sends their first message, their DB row might still have `is_admin=False`. Auto-fix it:

```python
if not user.is_admin and user_email_lc in _ADMIN_EMAILS:
    user.is_admin = True
    db.commit()
```

---

## Gotchas

- **The modal bug:** Frontend showed "⚡ Admin" (env var check passed) but the streaming endpoint returned 402 (DB flag was `False`). The fix was the auto-sync above. Always make sure the streaming/budget endpoint also checks the env var, not just `user.is_admin`.
- **Stale backend process:** We restarted uvicorn and the endpoint magically worked — the old running process had code from before the DB fallback fix. Always restart after code changes (uvicorn without `--reload` serves the exact code from when it started).
- **Env var wins over DB revoke:** If email is in `ADMIN_EMAILS`, you can't demote them via the admin UI. That's intentional — it's your recovery path.

## Quick reference

```
Production setup:
1. Set ADMIN_EMAILS=youremail@gmail.com in Railway env vars
2. Deploy → you get admin immediately (env var path, no DB row needed)
3. Use admin panel to add more admins → they get is_admin=True in DB
4. Those DB admins work even after a backend restart

Test the DB fallback:
  patch("routers.admin_users._ADMIN_EMAILS", {"only@superadmin.com"})
  → other DB admins should still pass _require_admin()
```
