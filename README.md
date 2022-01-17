This project will accept a URL from popular git websites and score the repo for quality.

Work in progress. (Not generating a grade yet)

See Makefile for valid make commands to run various aspects

----

# Quickstart

Requires: Python 3.10.1+, Poetry, Make

```bash
make init
export SECRET_KEY='whatever you want'
make run
open http://localhost:8000/repo/repo-input
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

----

TODO

- [ ] Cache Data in DB
- [ ] Make UI Pretty
- [ ] Support for Accounts + Oauth Login to reduce rate limiting
- [ ] Host it somewhere
