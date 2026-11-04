# CLAUDE.md

A time-boxed build: about 3 hours of work inside a fixed window. Speed of a correct, demoable result
beats completeness. This repo may be shared publicly; write about the product and its users only.

## Status

Scaffold only. The brief is in `scratch/brief.md` (git-ignored, never commit it); product notes are in
`research/`. Record the stack and commands below as soon as they exist.

## Commands

```sh
# TBD once the stack is chosen (default: uv + Python 3.12)
uv sync
uv run pytest path/to/touched_test.py   # while editing
uv run pytest                           # once, at integration
```

## Time box and scope

- Plan in waves, each with a clock budget. Default for a 3-hour build:
  - **Wave 0, contracts (serial, about 20 min, one session):** stack, folder layout, the shared data
    types and function/API signatures (typed stubs that raise `NotImplementedError`), a small committed
    sample dataset or fixture, and the tickets. Nothing else starts until wave 0 is merged.
  - **Wave 1, build (parallel, about 90 min):** one session per ticket, each against the wave-0 stubs
    and fixture, so no ticket waits on another.
  - **Wave 2, integrate and measure (about 40 min, integrator):** merge, wire end to end, run the one
    metric that matters, fix what breaks.
  - **Wave 3, write-up and demo (about 30 min):** README, demo, screenshots. Reserve this time; never
    spend it on features.
- If a wave overruns, cut scope (log it in the README's "Cut" section); don't move the write-up time.
- Prefer one language. Python end to end (e.g. Streamlit for UI) unless the brief needs something else:
  every extra toolchain costs install time in every worktree.

## Seams and tickets (for maximum parallel work)

- **A seam is a typed contract fixed in wave 0:** a data model (pydantic/dataclass), a pure function
  signature, or an HTTP/JSON shape. Tickets meet only at seams.
- **Each ticket owns its files.** Two tickets in one wave never edit the same file. Shared files
  (contracts, `pyproject.toml`, README) change only in wave 0 or by the integrator.
- **Tickets are vertical but thin** (30-45 min each): one user-visible behaviour, built against the
  fixture, with its seam test. Typical wave-1 split: data loading/cleaning, core logic or model, AI/LLM
  call, UI. Mock the neighbour at the seam, don't wait for it.
- **At most 3 sessions at once** (8 GB Apple Silicon), plus at most one browser agent.
- Dependencies a ticket needs are added in wave 0, so worktrees don't race on `uv.lock`.

## Parallel sessions

- One worktree per ticket under `.claude/worktrees/<branch>`, branched from `main` after wave 0,
  each with its own `uv sync`. In a worktree, `unset VIRTUAL_ENV` if uv warns about it.
- One **integrator** session merges ticket branches into `main` (`--no-ff`) and runs the full suite
  once on the merged tip. Ticket sessions hand over their branch; they never commit to `main`.
- Commits are small with clear messages and carry no `Co-Authored-By` line.

## Tests under the clock

- Test the seams: each contract gets one test that pins its behaviour (shape, a rule, an edge case).
  Skip tests that restate the implementation or test a framework.
- Editing: run only the touched test files. Ticket close: the ticket's tests plus `ruff check`.
  Integration: the full suite, once.

## Hygiene (the repo may go public)

- No secrets: keys in `.env` (ignored), names in `.env.example`.
- No personal data, no notes about the hiring process, no copied brief text outside `scratch/`.
- Public or provided data only; name every dataset's source and licence in the README. Never scrape
  behind logins.
- The README says honestly what works, what doesn't, what was assumed, and what would prove the idea
  wrong. Numbers first.

## Agent skills

### Issue tracker

Local markdown: `.scratch/<feature>/spec.md` and one file per ticket in `.scratch/<feature>/issues/`
(with `Blocked by:` lines). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at the root, created lazily. See `docs/agents/domain.md`.
