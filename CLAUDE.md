# Working rules for this repo

This repo may be shared publicly later. Keep it clean:

- No secrets in git. API keys go in `.env` (ignored); list the variable names in `.env.example`.
- No personal data: no phone numbers, personal emails, salary, or notes about job applications or other companies' internal matters.
- Only use public data or data provided with the task. Note the source of every dataset in the README.
- Python: type hints on every function (parameters and return, `-> None` too), modern syntax (`list[str]`, `X | None`).
- Tests pin behaviour that matters (rules, contracts, edge cases); fewer, sharper tests over many shallow ones.
- Simplest thing that works; no speculative abstractions.
- README states honestly what works, what doesn't, and what was assumed. No claims the code can't back.
- Commit in small, readable steps with clear messages.
