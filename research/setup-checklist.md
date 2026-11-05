# Setup checklist (before pressing Start)

Checked on this machine on 4 Nov 2026. ✅ = verified here, ⬜ = you need to do it, ❓ = unverified.

## Submission needs three links

The challenge asks for a GitHub repo, a **live prototype link** and a **Google Drive link** with
supporting files (strategy, thinking, AI chats). Every item below serves one of those three.

## GitHub

- ✅ `gh auth status`: logged in as the repo owner, with token scopes `repo` and `workflow`. You can
  create repos and push.
- ✅ This repo has an `origin` on GitHub and is **private**. The challenge allows a private repo
  ("I will give access if asked").
- ⬜ **Decide: reuse this repo or start a new one.** My recommendation is to reuse it and rename it
  at the end (`gh repo rename <name>`). The scaffold, the agent workflow and this research are your own
  preparation, the rules allow preparation, and the history shows how you work. Start a new repo only
  if you want a history that begins at Start.
- ⬜ Know how to grant access fast: `gh api -X PUT repos/<owner>/<repo>/collaborators/<user>`, or make
  the repo public with `gh repo edit --visibility public --accept-visibility-change-consequences` if
  the deploy needs it.

## Toolchain

| Tool | Status |
|---|---|
| uv | ✅ 0.11.31 |
| Python 3.12 | ✅ managed by uv (`~/.local/share/uv/python/cpython-3.12`). System `python3` is 3.9.6, so always use `uv run` |
| Node / npm | ✅ v26.7.0 / 11.19.0 (only needed if you choose a JS front end) |
| git / gh | ✅ 2.50.1 / 2.100.0 |
| Docker | ✅ 29.7.2 (not needed for this build) |
| ruff | ⬜ not on PATH. Add it as a dev dependency in wave 0 (`uv add --dev ruff pytest`) |
| Streamlit | ⬜ not installed. Add it in wave 0 (`uv add streamlit`); no global install |
| Machine | 8 GB RAM. Keep to at most 5-6 light sessions, one browser agent |

**Gotcha:** a bare `uv init` picks up miniforge Python 3.14 (`requires-python >=3.14`). Always run
`uv init --python 3.12`.

**Pre-warm the cache now (5 min, saves install time after Start):**

```sh
cd /tmp && uv init --python 3.12 warm && cd warm && uv add streamlit pandas anthropic pydantic pytest ruff && uv run streamlit --version
```

## Live prototype (deploy)

You'll choose between two options once you've read the task.

**Option 1: Streamlit Community Cloud with a public repo**
- ✅ Account exists (GitHub `dhruv-kapri`, email login). It currently has **public-repo access only**.
  Settings say "Streamlit does not have access to private repos on this GitHub account". Granting
  private access means OAuth with full `repo` scope (read and write on all private repos), and we
  **decided not to grant it**. Plan: make the submission repo public at the end, then deploy.
- ✅ A throwaway repo `Dhruv-Kapri/streamlit-smoke` (private, with `app.py` and `requirements.txt`)
  exists for testing the deploy.
- ✅ **Deploy tested on 4 Nov 2026.** `streamlit-smoke` was made public, deployed from
  share.streamlit.io/deploy (repo, branch `main`, file `app.py`), and went live at
  `https://<random>.streamlit.app/` within about a minute. An anonymous visitor goes through a
  `/-/login` cookie hop and then gets HTTP 200, so no sign-in is needed. Gotcha: the form keeps
  stale "does not exist" errors until you click outside the field. You can set a custom subdomain
  under "App URL (optional)".
- ✅ Cleaned up on 4 Nov 2026: the Streamlit app, the GitHub repo (deleted in the
  web UI) and the local copy are all gone.
- Flow after Start: build in the submission repo, make it public when the first demoable version
  exists (check that `scratch/`, `.env` and `data/raw/` are ignored first), then deploy.
- Free tier (third-party sources, not confirmed): apps sleep after about 12 h idle, about 1 GB RAM.
  Fine for a demo. Secrets go in App settings → Secrets as TOML (`ANTHROPIC_API_KEY = "..."`), read
  through `st.secrets`.

**Option 2: Hugging Face Spaces, which can't host a free Streamlit app (checked 4 Nov 2026)**
- ⚠️ On the new-Space form for this free account, **Docker shows a "Paid" lock** and **CPU Basic is
  greyed out**. The only free combination is **Gradio + ZeroGPU**. **Protected** Spaces (public app,
  private code) also need PRO. Evidence: `scratch/evidence/hf-docker-paid-cpu-basic-disabled.jpg`.
  This contradicts HF's docs, which still list CPU Basic as free.
- So on the free tier, option 2 means: **write the UI in Gradio, not Streamlit**, make the Space
  **public** (a private Space can't be opened by reviewers), and accept ZeroGPU's daily quota. If you
  choose this, decide it in wave 0, because the UI ticket changes.
- The GitHub repo can still stay private; the Space is a separate git repo on HF, and its code is
  public.
- ✅ The `hf` CLI 2.4.0 is installed (`uv tool install huggingface_hub`).
- ✅ HF account exists (Dhruv-Kapri, signed in in Chrome).
- ⬜ You: create a **write** token (Settings → Access
  Tokens). Run `! hf auth login` and paste the token there; don't paste it into chat.
- Note: HF **deprecated the built-in Streamlit SDK** (changelog, 2025-04-30). A Docker setup is
  kept here for the case where you have PRO:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```yaml
---
title: <app name>
sdk: docker
app_port: 8501
---
```

  Deploy (flags checked against `hf` 2.4.0): `hf repos create <user>/<name> --type space --sdk
  docker --flavor cpu-basic --secrets-file .env`, then `hf upload <user>/<name> . --repo-type
  space`. Secrets can also go in Space Settings → Variables and secrets; the app reads them as
  environment variables.
- Vercel: not considered (JS only, and we're building in Python).
- Keep the LLM key out of the deployed app, or put a spending cap on the key. A public demo link with
  a live key can be abused.

## LLM API

- ✅ **Working (4 Nov 2026).** The key lives in `.env` as `ANTHROPIC_API_KEY` (git-ignored; the name
  is listed in `.env.example`). It belongs to Console workspace **`sandbox`**, which has a **$2/month
  spend limit** (change it under Settings → Spend limits → Workspace limits → "Adjust limit"). The
  limit resets on the 1st, UTC. The Default workspace has no keys.
- Billing: the org's monthly API credits come from a linked plan ($200/month, expiring at the end of
  each cycle). No card is on file, so spending can't go past the credits.
- Smoke test passed: `cd /tmp/pf-smoke && uv run python smoke.py` printed `OK` (`claude-sonnet-5-5`).
- Model choice: `claude-sonnet-5-5` for parsing and explanations; `claude-opus-5-5` only if the
  reasoning is hard. $2 is plenty for development. If the deployed demo gets traffic, cache
  responses or add a per-session call cap so the limit doesn't cut the demo off mid-review.
- For the deploy, put the key in Streamlit's Secrets (TOML: `ANTHROPIC_API_KEY = "..."`) and read
  it with `st.secrets` or the environment. Never commit it.

## Google Drive (supporting files)

- ✅ Drive folder created: "Property Finder Product Builder - supporting files" (My Drive).
  ⬜ Turn on link sharing ("anyone with the link can view") at submission time, then paste the link.
- ⬜ Plan to export AI chats. Claude Code transcripts are JSONL files under your Claude Code projects
  directory (for example `~/.claude-dir/projects/<this-repo>/`). Copy the session files for the
  6-hour window, or write a short markdown "decision log" as you go. The rules say "the thinking and
  the decisions must be mine", so a running decision log is probably worth more than raw transcripts.

## Public data (for the top ideas)

| Source | What | Login-free download? | Licence |
|---|---|---|---|
| DLD Open Data, https://dubailand.gov.ae/en/open-data/real-estate-data/ | Transactions, Rents (Ejari), Projects, Valuations, Units, Brokers, Developers | No login, but **every search needs a captcha** and a date range. Export only by hand; no direct file URLs. The current year may be the only one available | Not stated (page footer: "© Dubai Land Department, All Rights Reserved") ❓ |
| Dubai Pulse, https://www.dubaipulse.gov.ae/organisation/dld | The same DLD datasets as CSV/API (`dld_transactions-open`, `dld_rent_contracts-open`, …) | ❓ Probably login- or request-gated; timed out from my tools. Last updated about Apr 2024 | ❓ |
| data.dubai, https://data.dubai/ | Successor portal for older DLD years | ❓ blocked automated checks | ❓ |
| DLD Rental Index, https://dubailand.gov.ae/en/eservices/rental-index/rental-index/ | Official rent-range calculator | Interactive only, no file | n/a |
| Kaggle UAE listing sets | About 5k listings, **scraped from portals** | Needs a Kaggle login | Terms risk; avoid |
| propertyfinder.ae | Listings | robots.txt disallows search URLs, map-search, transactions-with-query and APIs. **Do not scrape** | n/a |

- ✅ **Done 4 Nov 2026** (you ticked the captcha, I exported). Both files are in `data/raw/dld/`
  (ignored by git, so if you work in worktrees, copy them in):
  - `transactions_2026-10-04_2026-11-04.csv`: 17,866 rows, 4.4 MB, 22 columns (`INSTANCE_DATE`,
    `GROUP_EN` Sales/Mortgage/Gifts, `PROCEDURE_EN`, `IS_OFFPLAN_EN`, `AREA_EN`, `PROP_SB_TYPE_EN`,
    `TRANS_VALUE`, `ACTUAL_AREA` in sqm, `ROOMS_EN`, `NEAREST_METRO_EN`, `PROJECT_EN`, …). 11,686
    Sales and 8,840 sales of flats. The **Mortgage count is exactly 5,000, which may be an export
    cap.** No names or other personal data.
  - `rents_2026-10-04_2026-11-04.csv`: 112,403 rows, 27 MB, 20 columns (`REGISTRATION_DATE`,
    `START_DATE`, `END_DATE`, `VERSION_EN` New/Renewed, `AREA_EN`, `ANNUAL_AMOUNT`,
    `ACTUAL_AREA`, `PROP_SUB_TYPE_EN`, `ROOMS`, `USAGE_EN`, `NEAREST_METRO_EN`, `PROJECT_EN`, …).
    66,253 rows are residential, single-unit flats. **`ROOMS` is empty in 96% of rows**, and
    `PROJECT_EN` is filled for 41% of flats. Median annual rent for flats: New 70,000 vs Renewed
    60,059. Marsa Dubai has 2,461 contracts, median 115,000.
  - The DLD reCAPTCHA shows "This site is exceeding the reCAPTCHA Enterprise free quota"
    (evidence: `scratch/evidence/dld-recaptcha-quota-warning.png`). After Start, assume you **can't**
    re-export, so work from these files.
- Previous plan: **Before Start (10 min, by hand, in a normal browser):** on the DLD Open Data page, export one
  recent month of **Rents** and one of **Transactions** for Dubai (you'll need to tick the captcha
  yourself). Keep the files in `data/raw/`, which is ignored. Note the row count and the columns.
  This is the only realistic real-data path for ideas #1 and #5 in the teardown. If the brief comes
  with its own data, use that instead.
- Fallback: a small synthetic fixture shaped like the DLD columns, clearly labelled as synthetic in
  the README.
- ❓ Licence: DLD doesn't publish open-data terms on the page. In the README, say "public DLD open data,
  terms not published; a small sample is used for a non-commercial prototype", and commit only an
  aggregated or small sample.

## Do before Start

- ❌ **Scout** couldn't be tested: the web version is waitlisted and the Android app has no entry point.
  Treat it as gated; build anything Scout-like from the public pages only.
- ⬜ Spend 5 minutes in the **app** (Home Valuation, Rent in 12) and on **mobile web** on your phone.
  I didn't test mobile web.
- ✅ Bayut reviewed first-hand after you cleared its check (see the teardown).
- ⬜ Turn off notifications. The challenge page logs tab switches, so keep it in its own window.

## 3-hour plan (inside the 6-hour window)

| Clock | Wave | Output |
|---|---|---|
| 0:00-0:20 | Read the task, choose the idea, write a decision log | Problem, user, one metric, what would prove it wrong (in Drive) |
| 0:20-0:40 | Wave 0, contracts | `pyproject` deps, data model and function stubs, committed fixture, 3-4 tickets |
| 0:40-2:10 | Wave 1, parallel build | Data loader, core logic, LLM call, Streamlit UI; each with a seam test |
| 2:10-2:30 | Wave 2, integrate | Merge, wire end to end, `uv run pytest` once |
| 2:30-2:50 | Measure and deploy | Run the evaluation (e.g. held-out coverage), deploy to Streamlit Cloud, check the live link |
| 2:50-3:20 | Wave 3, write-up | README, Drive folder, submit all three links |
| 3:20-6:00 | Buffer | Fixes, never new features. **Submit a first version by 3:30 and update it later** |

## Write-up structure (README)

The brief doesn't prescribe one. Based on "submit what you have and explain what is missing":

1. **Live link, repo and the one-line pitch**
2. **Numbers first:** the metric and the evaluation result (e.g. "the fair-price band contains the
   actual rent in 78% of 200 held-out contracts")
3. **Problem and user:** what you saw on propertyfinder.ae, with screenshots from the teardown
4. **What I built**, and the key decisions with the reasons for each
5. **What works / what doesn't / what's missing**, and what you'd need to finish it
6. **Assumptions**, and **what would prove this wrong**
7. **Data:** source, licence and size; AI tools used, and how
8. **Cut:** what you dropped for time
9. **Next steps:** how Property Finder would ship and A/B test it (metric, guardrail)
