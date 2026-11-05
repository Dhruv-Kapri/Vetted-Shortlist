# Issue tracker: GitHub Issues

Issues and specs for this repo live in GitHub Issues on `Dhruv-Kapri/Vetted-Shortlist`. Use the `gh`
CLI. Don't keep tickets as local markdown files.

## Conventions

- One issue per ticket. A spec is an issue too, labelled `spec`; its tickets link back with
  `Part of #N`.
- Triage state is a label (see `triage-labels.md`); exactly one triage label per open issue.
- Dependencies are a `Blocked by: #N, #N` line near the top of the body.
- Discussion and progress go in issue comments, not in edits to the body.
- Never put the task text, the brief or anything from `scratch/` in an issue. The repo may be shared.

## Commands

```sh
gh issue create --title "<title>" --label ready-for-agent --body-file <file>   # publish
gh issue view <N> --comments                                                    # fetch a ticket
gh issue list --label ready-for-agent --state open                              # open work
gh issue comment <N> --body "<text>"                                            # comment
gh issue edit <N> --add-label <label> --remove-label <label>                    # change triage state
gh issue close <N> --comment "<what was done, commit or PR>"                    # resolve
```

## When a skill says "publish to the issue tracker"

Create a GitHub issue with `gh issue create`.

## When a skill says "fetch the relevant ticket"

`gh issue view <N> --comments`. The user will normally pass the issue number or URL.

## Wayfinding operations

Used by `/wayfinder`. The **map** is one issue; each **child** ticket is its own issue.

- **Map**: an issue titled `Map: <effort>`, labelled `map`, holding the Notes / Decisions-so-far /
  Fog body.
- **Child ticket**: an issue whose body starts with `Part of #<map>` and a `Type:` line
  (`research`/`prototype`/`grilling`/`task`), with the question in the body.
- **Blocking**: a `Blocked by: #N, #N` line near the top. A ticket is unblocked when every issue it
  lists is closed.
- **Frontier**: open, unblocked, unassigned child issues of the map; lowest number wins.
- **Claim**: assign yourself (`gh issue edit <N> --add-assignee @me`) before any work.
- **Resolve**: comment the answer under an `## Answer` heading, close the issue, then add a pointer
  (gist + issue link) to the map issue's Decisions-so-far.
