# 01: Fill the Drive folder with supporting files

Status: ready-for-human
Type: task
Due: before the timer ends (01:16 IST, 6 Nov 2026). Do item 5 last; Drive must not change after the deadline.

Drive folder (already set to "Anyone with the link: Viewer"):
https://drive.google.com/drive/folders/1jiedNJopefHYhD2Kvq87_ZuFR0L-IEtd

Stage files in `scratch/drive/` (git-ignored), review them, then upload.

## Upload, in priority order

1. [ ] **Decision log** (1-2 pages): each big call, the options, the pick and why (building chosen
   for the audit, problem behind the problem, rule thresholds, where it lives, what was cut). Claude
   can draft a skeleton from the transcripts and git history; rewrite it in your own words.
2. [ ] **AI chat transcripts, redacted**: the Claude Code session JSONL files under
   `~/.claude-dir/projects/-Users-dhruvkapri-Desktop-Developer-sandbox-1104/` converted to readable
   markdown. **Both sessions quote the verbatim task text.** Replace it with `[task text removed]`
   and grep the output for it before uploading. No API keys were found (checked 5 Nov).
3. [ ] **Audit evidence snapshot**: zip `data/raw/pf/` (about 19 MB: listing captures, details,
   photo hashes) so the audit can still be checked after listings change. Skip `data/raw/dld/`:
   it's public, so cite its source in the README.
4. [ ] **Blocker screenshots** from `scratch/evidence/`, after checking each for name, email or
   session data.
5. [ ] **Final docs as PDF** (ONE-PAGER, AUDIT, RULES, AI-LOG), exported at the end so Drive
   pins what was submitted.

## Never upload

`scratch/brief.md`, `scratch/email-raw.md`, `scratch/task/`, or anything quoting the task text
(the rules forbid sharing it, and the folder is open to anyone with the link).
