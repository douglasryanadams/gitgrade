This project will accept a URL from popular git websites and score the repo for quality.

Work in progress. (Not generating a grade yet)

See Makefile for valid make commands to run various aspects

----

# Quickstart

Requires: Python 3.10.1+, Poetry, Make, cloc

```bash
make init
export SECRET_KEY='whatever you want'
make run
open http://localhost:8000
```

Copy a URL for a Github or Bitbucket Repo (example: <https://github.com/git/git>) and put it into the form.

----

Notes

- Github API Rate Limit:
    - Unauthenticated: 1 / Minute / IP
    - OAuth: 5000 / Hour (~1/second)
- Bitbucket API Rate Limit:
    - Unauthenticated: 1 / Minute
    - Auth: 1000 / Hour ( ~ 1 / 5 seconds )
- Git Remote Commands
  - `git clone --filter=tree:0 --single-branch --shallow-since=2021-01-17 https://github.com/git/git.git`
    - Smallest clone that allows inspection of the last year on the default branch
  - `git ls-remote --heads`
    - Returns list of branches
  - `git shortlog --numbered --summary --all`
    - List contributes and commits per contributor



----

TODO

- [x] Cache Data in DB
- [ ] Make UI Pretty + Add Boostrap
- [ ] Support for Accounts + Oauth Login to reduce rate limiting
- [ ] Host it somewhere

Additional Metrics

- [ ] Latest Release
- [ ] Number of Releases
- [ ] Avg time between releases
- [ ] Avg time to resolve issues
- [ ] Avg time to merge PRs
- [ ] Size (files and lines of code) for primary language in repo