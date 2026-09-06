You are acting as a senior technical reviewer fact-checking DP-700 (Fabric Data Engineer Associate) exam prep content in `DP700/` against **live** Microsoft Learn documentation. This is NOT a code review — it's a factual accuracy pass. Microsoft Fabric changes fast; anything asserted confidently in these files may already be stale. Do not answer from training data — verify every claim you correct against a fetched page from this session.

**No rushing.** This is a thorough, multi-hour task by nature (14 files, dozens of WebFetch/WebSearch calls). Prioritize correctness over speed. If the user has said "don't rush" or similar before, that still applies here by default.

---

## Step 1 — Establish the source of truth

Fetch the current official skills outline before touching any file:

1. `https://learn.microsoft.com/credentials/certifications/resources/study-guides/dp-700` — get the full "Skills measured as of {date}" outline (all sections, sub-bullets, weights) and the "Skills at a glance" percentages.
2. Note that date. Compare it against the date recorded in any "✅ Fact-checked / Re-verified" banner already present in the DP700 files — if a file's banner is already dated *after* the outline's date and nothing else has changed, you can skip deep re-verification of that file and just spot-check it.
3. If the change log renders (it may only show one row due to a rendering quirk — that's a known issue, not a bug in your fetch), note whatever it shows; don't over-invest trying to force it to render fully.

---

## Step 2 — Enumerate targets

```bash
find /Users/home/Documents/GitHub/DevLearnings/DP700 -type f \( -name "*.html" -o -name "*.md" \)
```

Expected: `DP700_Study_Plan.md`, `Day1_Implement_Manage.md`, `dp700_notes.html`, `dp700_official_notes.html`, `dp700_pb_notes.html`, `dp700_pdf_notes.html`, `dp700_kql.html`, `dp700_labs.html`, `dp700_scenarios.html`, `dp700_exam.html`, `dp700_mock2.html` through `dp700_mock6.html`. If the file list has grown or shrunk since this was written, adjust — don't skip new files.

Read every file in full (some are 500–1100+ lines; use `offset`/`limit` to page through, don't stop at the first page).

---

## Step 3 — Prioritize what to verify

You cannot re-verify every sentence with a fresh fetch — that's not proportionate. Spend your verification budget on claims that are: (a) stated with high confidence / flagged as "critical" or "heavily tested", (b) in areas Fabric changes often, or (c) contradicted by another file in this same folder (a strong signal something is wrong, since files share sources). Grep across files first to catch repeated claims cheaply, e.g.:

```bash
grep -rn -i "onelake data access\|oldar" DP700/
grep -rn -i "cls.*fallback\|column-level security.*directquery\|falls back to directquery" DP700/
grep -rn -i "native execution engine" DP700/
```

High-volatility topics worth checking every run (this list will drift out of date itself — treat it as a starting point, not gospel):

- **OneLake security** — current name/GA status for what used to be called "OneLake data access roles"; what granularity it supports (folder/table/row/column)
- **Direct Lake fallback behavior** — does RLS behave the same as CLS/OLS? (as of this writing: no — RLS falls back to DirectQuery, CLS/OLS errors instead; "Direct Lake on OneLake" doesn't fall back at all). Re-verify this doesn't drift further.
- **OneLake shortcuts** — which source types are read-only vs support write-through; which are cached; the full current list of internal/external shortcut types (this list keeps growing)
- **Native Execution Engine** — current UDF/complex-type support status (this reversed once already — don't assume the old answer or the new one without checking)
- **Git integration & deployment pipeline "supported items"** — these lists grow almost every release; don't trust a short list in any file without checking the current one
- **Database projects** — SDK-style requirement, DAC/dacpac's actual role, exact VS Code workflow/menu names
- **Capacity Metrics app** — current page/tab list (do not trust "exactly N tabs" claims)
- **queryinsights views** — exact list of view names
- **Spark runtime versions** — Spark/Delta version per Fabric Runtime number
- **Eventhouse / Real-Time Intelligence terminology** — "Query acceleration" vs "accelerated shortcut", OneLake availability sync behavior (existing vs new data, format, latency)
- **V-Order default status** — note the workspace-creation-date nuance (pre/post the cutoff where the default flipped), don't just say "on" or "off"
- Lab links in `dp700_labs.html` — quick `curl -s -o /dev/null -w "%{http_code}"` check that all still return 200

---

## Step 4 — Apply corrections

For each confirmed error:
- Edit the file in place. Don't rewrite unrelated content or restructure the page.
- Where a wrong claim is presented as a confident "gotcha" or gives an incorrect "correct answer" to a quiz question, fix the marked answer (`ans:`/`correct:`) too, not just the explanation text — a corrected explanation next to an unchanged wrong answer key is worse than doing nothing.
- If the same error appears in multiple files (expected, since they share sources), fix it everywhere — don't stop at the first occurrence. `sed -i ''` is fine for exact, unambiguous string/terminology swaps (e.g., a renamed feature) across a file; use targeted `Edit` for anything context-dependent.
- Add or refresh a short verification banner near the top of each file you touched: what was checked, the date, and a one-line summary of what changed. Keep it terse — this is a marker for next time, not documentation.

## Step 5 — Flag, don't fabricate

If a question's explanation is internally inconsistent (argues toward one answer, then reverses to a different "correct" answer via an assumption invented mid-explanation), or you cannot find a live source to confirm or deny a specific claim, do NOT guess a fix. Mark it clearly as unreliable/unverified with a note explaining why, and say so in your final summary to the user. This happened with 3 questions in `dp700_mock6.html` last run — check whether they're still marked, and don't silently "fix" them without new evidence.

---

## Step 6 — Git workflow

Follow the user's standard git rules: never commit to `main`, always a feature branch, never push without being told.

```bash
git fetch origin main
git checkout -b feature/dp700-accuracy-audit-<YYYY-MM-DD> origin/main
git add DP700/
git commit -m "Fact-check DP700 exam content against live Microsoft Learn docs (<date>)

<bullet summary of what changed this run>

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

Stop there. Wait for the user to say "push" or "pr" before pushing or opening a pull request, same as any other change.

---

## Hard rules

1. Never assert a correction without a live fetch from this session backing it — no "I recall Fabric does X."
2. Never silently trust that a claim is right just because multiple files agree — they likely share one source and one mistake.
3. Prefer flagging uncertainty over inventing a plausible-sounding fix.
4. Don't touch content outside DP700/ unless the user asks.
5. Don't add scope beyond fact-checking — this is not the place to redesign pages, add new practice questions, or restructure navigation.
