# pylint: disable=W,C,R

REPO = {
    "scm": "git",
    "has_wiki": False,
    "links": {
        "watchers": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/watchers"
        },
        "branches": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/refs/branches"
        },
        "tags": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/refs/tags"
        },
        "commits": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/commits"
        },
        "clone": [
            {
                "href": "https://bitbucket.org/atlassian/bamboo-tomcat-plugin.git",
                "name": "https",
            },
            {
                "href": "git@bitbucket.org:atlassian/bamboo-tomcat-plugin.git",
                "name": "ssh",
            },
        ],
        "self": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin"
        },
        "source": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/src"
        },
        "html": {"href": "https://bitbucket.org/atlassian/bamboo-tomcat-plugin"},
        "avatar": {
            "href": "https://bytebucket.org/ravatar/%7Bb258bff3-7c1a-4684-8332-2e82557e4006%7D?ts=default"
        },
        "hooks": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/hooks"
        },
        "forks": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/forks"
        },
        "downloads": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/downloads"
        },
        "pullrequests": {
            "href": "https://api.bitbucket.org/2.0/repositories/atlassian/bamboo-tomcat-plugin/pullrequests"
        },
    },
    "created_on": "2020-04-07T18:21:31.341436+00:00",
    "full_name": "atlassian/bamboo-tomcat-plugin",
    "owner": {
        "username": "atlassian",
        "display_name": "Atlassian",
        "type": "team",
        "uuid": "{02b941e3-cfaa-40f9-9a58-cec53e20bdc3}",
        "links": {
            "self": {
                "href": "https://api.bitbucket.org/2.0/workspaces/%7B02b941e3-cfaa-40f9-9a58-cec53e20bdc3%7D"
            },
            "html": {
                "href": "https://bitbucket.org/%7B02b941e3-cfaa-40f9-9a58-cec53e20bdc3%7D/"
            },
            "avatar": {"href": "https://bitbucket.org/account/atlassian/avatar/"},
        },
    },
    "size": 398213,
    "uuid": "{b258bff3-7c1a-4684-8332-2e82557e4006}",
    "type": "repository",
    "website": None,
    "override_settings": {
        "branching_model": False,
        "default_merge_strategy": False,
        "branch_restrictions": False,
    },
    "description": "",
    "has_issues": False,
    "slug": "bamboo-tomcat-plugin",
    "is_private": False,
    "name": "bamboo-tomcat-plugin",
    "language": "",
    "fork_policy": "allow_forks",
    "project": {
        "links": {
            "self": {
                "href": "https://api.bitbucket.org/2.0/workspaces/atlassian/projects/BAM"
            },
            "html": {"href": "https://bitbucket.org/atlassian/workspace/projects/BAM"},
            "avatar": {
                "href": "https://bitbucket.org/account/user/atlassian/projects/BAM/avatar/32?ts=1477882292"
            },
        },
        "type": "project",
        "name": "BAMBOO",
        "key": "BAM",
        "uuid": "{deceb48f-358a-4d1d-9cda-7fc4d8ee05e9}",
    },
    "mainbranch": {"type": "branch", "name": "master"},
    "workspace": {
        "slug": "atlassian",
        "type": "workspace",
        "name": "Atlassian",
        "links": {
            "self": {"href": "https://api.bitbucket.org/2.0/workspaces/atlassian"},
            "html": {"href": "https://bitbucket.org/atlassian/"},
            "avatar": {
                "href": "https://bitbucket.org/workspaces/atlassian/avatar/?ts=1612327398"
            },
        },
        "uuid": "{02b941e3-cfaa-40f9-9a58-cec53e20bdc3}",
    },
    "updated_on": "2021-03-29T08:36:27.991707+00:00",
}

WATCHERS = {
    "pagelen": 10,
    "values": [
        {
            "username": "atlassian",
            "display_name": "Atlassian",
            "type": "team",
            "uuid": "{02b941e3-cfaa-40f9-9a58-cec53e20bdc3}",
            "links": {
                "self": {
                    "href": "https://api.bitbucket.org/2.0/workspaces/%7B02b941e3-cfaa-40f9-9a58-cec53e20bdc3%7D"
                },
                "html": {
                    "href": "https://bitbucket.org/%7B02b941e3-cfaa-40f9-9a58-cec53e20bdc3%7D/"
                },
                "avatar": {"href": "https://bitbucket.org/account/atlassian/avatar/"},
            },
        },
        {
            "display_name": "Alexey Chystoprudov",
            "uuid": "{3c8851fc-170d-4c07-bdeb-533b2a98a905}",
            "links": {
                "self": {
                    "href": "https://api.bitbucket.org/2.0/users/%7B3c8851fc-170d-4c07-bdeb-533b2a98a905%7D"
                },
                "html": {
                    "href": "https://bitbucket.org/%7B3c8851fc-170d-4c07-bdeb-533b2a98a905%7D/"
                },
                "avatar": {
                    "href": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/initials/AC-2.png"
                },
            },
            "type": "user",
            "nickname": "Alexey Chystoprudov",
            "account_id": "557057:24f42a7e-e777-48f6-a987-05c51062f814",
        },
    ],
    "page": 1,
    "size": 2,
}

ALL_PRS = {
    "pagelen": 10,
    "values": [
        {
            "description": "",
            "links": {
                "decline": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/decline"
                },
                "diffstat": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/diffstat/schae/test-test-test:886f495685ca%0D932128721a5c?from_pullrequest_id=1"
                },
                "commits": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/commits"
                },
                "self": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1"
                },
                "comments": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/comments"
                },
                "merge": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/merge"
                },
                "html": {
                    "href": "https://bitbucket.org/schae/test-test-test/pull-requests/1"
                },
                "activity": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/activity"
                },
                "request-changes": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/request-changes"
                },
                "diff": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/diff/schae/test-test-test:886f495685ca%0D932128721a5c?from_pullrequest_id=1"
                },
                "approve": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/approve"
                },
                "statuses": {
                    "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/pullrequests/1/statuses"
                },
            },
            "title": "test commit 111",
            "close_source_branch": False,
            "type": "pullrequest",
            "id": 1,
            "destination": {
                "commit": {
                    "hash": "932128721a5c",
                    "type": "commit",
                    "links": {
                        "self": {
                            "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/commit/932128721a5c"
                        },
                        "html": {
                            "href": "https://bitbucket.org/schae/test-test-test/commits/932128721a5c"
                        },
                    },
                },
                "repository": {
                    "links": {
                        "self": {
                            "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test"
                        },
                        "html": {"href": "https://bitbucket.org/schae/test-test-test"},
                        "avatar": {
                            "href": "https://bytebucket.org/ravatar/%7B36c68da3-5f3e-4fdf-abdf-96cb346a094d%7D?ts=default"
                        },
                    },
                    "type": "repository",
                    "name": "test-test-test",
                    "full_name": "schae/test-test-test",
                    "uuid": "{36c68da3-5f3e-4fdf-abdf-96cb346a094d}",
                },
                "branch": {"name": "master"},
            },
            "created_on": "2018-01-20T06:48:29.429326+00:00",
            "summary": {
                "raw": "",
                "markup": "markdown",
                "html": "",
                "type": "rendered",
            },
            "source": {
                "commit": {
                    "hash": "886f495685ca",
                    "type": "commit",
                    "links": {
                        "self": {
                            "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test/commit/886f495685ca"
                        },
                        "html": {
                            "href": "https://bitbucket.org/schae/test-test-test/commits/886f495685ca"
                        },
                    },
                },
                "repository": {
                    "links": {
                        "self": {
                            "href": "https://api.bitbucket.org/2.0/repositories/schae/test-test-test"
                        },
                        "html": {"href": "https://bitbucket.org/schae/test-test-test"},
                        "avatar": {
                            "href": "https://bytebucket.org/ravatar/%7B36c68da3-5f3e-4fdf-abdf-96cb346a094d%7D?ts=default"
                        },
                    },
                    "type": "repository",
                    "name": "test-test-test",
                    "full_name": "schae/test-test-test",
                    "uuid": "{36c68da3-5f3e-4fdf-abdf-96cb346a094d}",
                },
                "branch": {"name": "test-branch-1"},
            },
            "comment_count": 0,
            "state": "OPEN",
            "task_count": 0,
            "reason": "",
            "updated_on": "2018-11-09T15:04:41.829219+00:00",
            "author": {
                "display_name": "Steve Chae",
                "uuid": "{22d326fe-cd53-42a6-b0b7-72df0b6d625a}",
                "links": {
                    "self": {
                        "href": "https://api.bitbucket.org/2.0/users/%7B22d326fe-cd53-42a6-b0b7-72df0b6d625a%7D"
                    },
                    "html": {
                        "href": "https://bitbucket.org/%7B22d326fe-cd53-42a6-b0b7-72df0b6d625a%7D/"
                    },
                    "avatar": {
                        "href": "https://secure.gravatar.com/avatar/d833ddeee53338bd50076ffb72c6b046?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FSC-5.png"
                    },
                },
                "type": "user",
                "nickname": "schae",
                "account_id": "557058:3bc6d179-1a87-4eb4-81a0-227b016caffd",
            },
            "merge_commit": None,
            "closed_by": None,
        }
    ],
    "page": 1,
    "size": 1,
}

OPEN_PRS = {"pagelen": 10, "values": [], "page": 1, "size": 0}
