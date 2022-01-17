This project will accept a URL from popular git websites and score the repo for quality.

Work in progress.

See Makefile for valid make commands to run various aspects

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
