# claude-code-action Setup (Pro Subscription, No API Key)

**Learned:** 2026-05-25

---

## What it is

`anthropics/claude-code-action@beta` — a GitHub Action that runs Claude Code inside CI.
Can use your Claude Pro/Max subscription instead of billing per token.

## One-time setup (per repo)

### 1. Get your OAuth token
Run in terminal:
```bash
# Full path if `claude` isn't in your PATH
"/Users/home/Library/Application Support/Claude/claude-code/2.1.149/claude.app/Contents/MacOS/claude" setup-token
```
Copy the token it prints.

### 2. Add it as a GitHub secret
Repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `CLAUDE_CODE_OAUTH_TOKEN`
- Value: the token from step 1

Same token works for all your repos — just add it as a secret in each one.

### 3. Install the Claude Code GitHub App
Go to: **https://github.com/apps/claude**
Click Install → select the repo.

This is separate from the token. Both are required.

### 4. Add permissions to the workflow
```yaml
permissions:
  contents: write       # so Claude can commit files
  pull-requests: write  # so Claude can comment on PRs
  id-token: write       # required for OIDC token exchange
```

## Workflow usage

```yaml
- uses: anthropics/claude-code-action@beta
  with:
    direct_prompt: /qa main HEAD      # runs a slash command
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

**Note:** The input is `direct_prompt` on the `@beta` tag (not `prompt`).
The `@main` tag uses `prompt`. Check which tag you're on.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `id-token: write` missing | Permission not set | Add to workflow `permissions:` block |
| `Claude Code is not installed on this repository` | GitHub App not installed | Install at https://github.com/apps/claude |
| `claude: command not found` | claude not in PATH | Use full path (see step 1 above) |
| `Invalid action input 'prompt'` | Wrong input name for beta tag | Use `direct_prompt` instead |
