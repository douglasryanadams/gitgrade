This project will accept a URL from popular git websites and score the repo for quality.

Work in progress. (Not generating a grade yet)

See Makefile for valid make commands to run various aspects

----

# Quickstart

Requires:

  - Python 3.10.1+
  - Poetry
  - Make
  - git
  - cloc
  - hadolint
  - yamllint
  - docker
  - docker-compose
  - awscli

```bash
make build
vim .env  # Add Environment Variables (see below) 
make run
open http://localhost:8000
```

Copy a URL for a Github or Bitbucket Repo (example: <https://github.com/git/git>) and put it into the form.

## Environment Variables

```bash
SECRET_KEY=local-testing-key  # Used for CSRF token in Django
GITGRADE_BASE_URL=http://localhost:8000  # Used for SSO/OAuth redirects
GITHUB_SSO_CLIENT_ID=<client id>  # Used for the server side calls for OAuth
GITHUB_SSO_CLIENT_SECRET=<client secret>  # Used for server side calls for OAuth
```

To get the Github SSO ID and Secret, you can either create your own Github app or contact <admin@builtonbits.com> and request a new secret key for development purposes.

## Pushing Changes

Currently, the Makefile contains some commands for pushing updates to the hosted version of gitgrade.net, consider this an example for pushing the container to AWS. The commands will not work for others unless <admin@builtonbits.com> has given your AWS account access. In the future, environment variables may be used here to make it easier for others to use to host their own servers.

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
- Django + WSGI + Nginx: <https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html>



----

TODO

- [x] Cache Data in DB
- [x] Make UI Pretty + Add Boostrap
  - "Pretty" might require additional work, but basic starting place is there
- [ ] Support for Accounts + Oauth Login to reduce rate limiting
- [ ] Host it somewhere
- [ ] Include sub-grades per metric
- [ ] Support 'deal breaker' limits (like has no recent authors)
- [ ] Tooltips for individual metrics
- [ ] Write out description of how calculation works and include on site
- [ ] Show recent search results on front page

Additional Metrics

- [ ] Latest Release
- [ ] Number of Releases
- [ ] Avg time between releases
- [ ] Avg time to resolve issues
- [ ] Avg time to merge PRs
- [ ] Size (files and lines of code) for primary language in repo
