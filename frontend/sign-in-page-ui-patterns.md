# Sign-In Page UI Patterns — Immersive Lanes, Marquee, Photo Carousel

**Learned:** 2026-05-26 | **Project:** TravelPlannerV2

---

## What it is
Techniques for building an immersive sign-in page with full-bleed animated photo lanes, a frosted-glass auth overlay, per-card photo carousels, and a slide-up hover panel — plus the event-propagation gotchas that come with layered click targets.

---

## How it works / Key steps

### Full-bleed scrolling lanes (marquee)
- Three vertical lanes of cards scroll upward indefinitely with `@keyframes marqueeUp`
- GPU-accelerate with `transform: translate3d(0, 0, 0)` and `will-change: transform` — this moves work off the main thread and eliminates jank
- Pause on hover: toggle `animationPlayState: 'paused'` via React state on `onMouseEnter` / `onMouseLeave`

### Frosted glass auth overlay — desktop vs mobile
- **Desktop:** fixed right panel (e.g. 300px wide) with `backdrop-filter: blur(12px)` and `background: rgba(..., 0.7)` — sits over the lanes
- **Mobile:** bottom sheet with drag handle, same glass styling
- Use theme CSS vars everywhere (`--t-primary`, `--t-ai-bubble`, etc.) — hardcoded colors break non-default themes

### Per-card photo carousel
- Store `photoIdx` in state; cycle through an array of image URLs (picsum.photos is auth-free and no CORS issues — Unsplash CDN can block with ORB errors)
- **Don't use a `loadedIdx` gate** — it resets on back-navigation and breaks images. Instead render all images stacked, toggle visibility with `opacity: i === photoIdx ? 1 : 0`. Use a dark base div as the loading placeholder.
- Photo dot indicators: map over array, apply active style when index matches `photoIdx`

### Slide-up hover panel
- Absolute-position a panel at `bottom: 0`, default `transform: translateY(100%)`, on hover `translateY(0)` with `cubic-bezier` easing
- Panel contains emoji, title, 2-line clamped description, and a CTA pill button
- Default title/description fades out simultaneously so the card doesn't feel cluttered

---

## Gotchas

### Arrow clicks triggering sign-in (event bubbling)
- Card has `onClick` → triggers Google sign-in. Arrow buttons sit inside the card.
- Fix: call `e.stopPropagation()` inside the arrow button's `onClick`. Add `e.currentTarget.closest('button')` guard on the card's onClick for belt-and-suspenders.
- **Rule:** any interactive child inside a click-triggered parent needs explicit `stopPropagation`.

### Persona sheet flash on auto-send
- When navigating from sign-in with `autoSend=true`, ChatClient was fetching the persona sheet and briefly showing it before auto-sending the destination prompt.
- Fix: skip persona sheet fetch in the `!initialConvId` branch when `autoSend=true`.

### Image reset on back navigation
- `loadedIdx` state tracking which image had loaded would reset to `0` when the user navigated back (React unmounts/remounts the component).
- Fix: drop `loadedIdx` entirely — keep all images in the DOM, control visibility with `opacity`. The browser cache handles repeated loads instantly.

### Unsplash CDN CORS / ORB blocks
- Unsplash CDN URLs can fail with "ORB (Opaque Response Blocking)" errors in some browsers.
- Swap to `https://picsum.photos/{w}/{h}?random={seed}` — no API key, no auth, consistent CORS headers.

---

## Quick reference

```tsx
// GPU-promoted marquee
<div style={{
  animation: `marqueeUp ${duration}s linear infinite`,
  transform: 'translate3d(0,0,0)',
  willChange: 'transform',
  animationPlayState: hovered ? 'paused' : 'running',
}} />

// Photo carousel — opacity swap, no loadedIdx
{photos.map((src, i) => (
  <img key={src} src={src} style={{ opacity: i === photoIdx ? 1 : 0, transition: 'opacity 0.4s' }} />
))}

// Arrow button inside clickable card
<button onClick={e => { e.stopPropagation(); setPhotoIdx(prev => (prev + 1) % photos.length); }}>
  →
</button>

// Card click guard
<div onClick={e => { if ((e.target as Element).closest('button')) return; onSignIn(); }}>

// Slide-up panel
<div style={{
  position: 'absolute', bottom: 0, width: '100%',
  transform: hovered ? 'translateY(0)' : 'translateY(100%)',
  transition: 'transform 0.35s cubic-bezier(0.4,0,0.2,1)',
}} />
```
