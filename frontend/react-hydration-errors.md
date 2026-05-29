# React Hydration Errors — Causes & Fixes

**Learned:** 2026-05-28 | **Project:** TravelPlannerV2

---

## What it is
Hydration errors happen when the HTML the server sends doesn't match what React renders on the client. React can't patch it up — it just warns and may show broken UI. Two separate causes bit us in the same session.

---

## Cause 1 — Locale-sensitive formatters

`toLocaleDateString()` and `toLocaleString()` use the **runtime's default locale**. Node.js server and the user's browser often have different defaults → server renders `"5/28/2026"`, browser renders `"28/05/2026"` → mismatch.

**Fix:** Always pass an explicit locale.

```tsx
// ❌ breaks hydration
{new Date(u.created_at).toLocaleDateString()}
{u.tokens_used.toLocaleString()}

// ✅ consistent server + client
{new Date(u.created_at).toLocaleDateString("en-US")}
{u.tokens_used.toLocaleString("en-US")}
```

---

## Cause 2 — Pre-hydration DOM mutations (theme scripts)

An inline `<script>` that runs before React hydrates (e.g. sets `data-theme` on `<html>` from `localStorage`) will modify the DOM. Server sent `<html lang="en">`, script added `data-theme="spring"` → client sees different attributes → hydration mismatch.

**Fix:** `suppressHydrationWarning` on the element the script touches.

```tsx
// app/layout.tsx
<html
  lang="en"
  className={`...`}
  suppressHydrationWarning   // ← tells React: "I know this will differ, it's intentional"
>
  <body>
    <script dangerouslySetInnerHTML={{ __html: themeScript }} />
    ...
  </body>
</html>
```

Also worth adding on any element that uses `Date.now()` or `Math.random()`:

```tsx
<footer suppressHydrationWarning>
  © {new Date().getFullYear()} MyApp
</footer>
```

---

## Gotchas

- The error message says "Date formatting in a user's locale" — this hints at Cause 1, but Cause 2 (pre-hydration scripts) triggers the exact same error message with a completely different stack trace. Read the component tree in the error, not just the header.
- `"use client"` components are still server-rendered for SSR. The `suppressHydrationWarning` fix applies to them too.
- The fix is element-scoped — only the element with the prop suppresses, not its children.

## Quick reference

```
Symptom: "A tree hydrated but some attributes of the server rendered HTML didn't match"
  → Check: are you using toLocaleDateString() / toLocaleString() without a locale arg?
  → Check: does an inline <script> modify the element before React hydrates?

Fix 1: add "en-US" to all toLocaleDateString() / toLocaleString() calls
Fix 2: suppressHydrationWarning on <html> (or whichever element the script touches)
```
