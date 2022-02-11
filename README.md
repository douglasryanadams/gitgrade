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

# If using a DB outside of dev:

DATABASE_USERNAME=gitgrade
DATABASE_PASSWORD=<database password>
DATABSE_HOST=<database hostname>
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
- [x] Support for Accounts + Oauth Login to reduce rate limiting
- [x] Host it somewhere
- [x] Include sub-grades per metric
- [x] Support 'deal-breaker' limits (like has no recent authors)
    - Implemented with weighting
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

Bugs

- [ ] Any invalid URL results in a 500

----

# On Release

Update:

- pyproject.toml
- gitgrade/templates/gitgrade/base.html
- aws/gitgrade-carrot.json

# Misc. Notes

The production infrastructure has these parts:

1. An Application Load Balancer listening for HTTPS on 443
    - Security Group 'gitgrade-loadbalancer' that listens for 443 and forwards anywhere
    - Targret group configured during setup of service (see below)
3. ECS Task Definition
    - This is configured by `./aws/gitgrade-carrot.json`
    - Must be updated to reference new version of docker container when a new version is released
    - Requires IAM role access to KMS and SSM for secrets
    - This is basically the equivalent of docker-compose but for ECS
2. ECS Fargate Cluster
    - Cluster that runs the task definition
    - Launches the service with some key properties:
        - Sets up the Load Balancer described above with a new target group
        - Uses its own security group that allows connections from the load balancer (referenced by the load balancer's security group) for connections over port 8000
        - Runs a single instance (cheap), will auto-restart since it's a 'service' if something goes down
3. Docker Image
    - This is built locally and uses the command in the `Makefile` to push it up to AWS
    - Currently runs a single-threaded uWSGI process, but relies on the ALB for HTTPS
4. RDS Aurora Serverless Postgres 10.4
    - Serverless because I don't think this will get used often, at least at first and will keep costs down
    - Postgres because it integrates well with Django and makes local dev easier
    - RDS has a security policy that allows connections from the Fargate Cluster's security group over port 5432
    - Note that Aurora Serverless does not permit connections from outside the VPC regardless of security group
        - For this reason, the Docker image includes running the migrations every time a new container starts
        - This 'automigration' strategy implies that breaking DB changes should be backwards compatible for at least 1 revision to allow task pool draining








