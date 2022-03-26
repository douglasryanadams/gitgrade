# pylint: skip-file
# mypy: ignore-errors
# fmt: off

from typing import Final

from repo.data.github import Commit, Author

COMMITS_PAGE_RAW: Final = [
    {
        "sha": "e8e737bcf6d22927caebc30c5d57ac4634063219",
        "node_id": "C_kwDOBN0Z8doAKGU4ZTczN2JjZjZkMjI5MjdjYWViYzMwYzVkNTdhYzQ2MzQwNjMyMTk",
        "commit": {
            "author": {
                "name": "Matthew Rahtz",
                "email": "matthew.rahtz@gmail.com",
                "date": "2022-03-26T16:55:35Z"
            },
            "committer": {
                "name": "GitHub",
                "email": "noreply@github.com",
                "date": "2022-03-26T16:55:35Z"
            },
            "message": "bpo-43224: Implement PEP 646 grammar changes (GH-31018)\n\nCo-authored-by: Jelle Zijlstra <jelle.zijlstra@gmail.com>",
            "tree": {
                "sha": "6c0d4d51e8216f02fa0e6874aa4d78e20dd9397a",
                "url": "https://api.github.com/repos/python/cpython/git/trees/6c0d4d51e8216f02fa0e6874aa4d78e20dd9397a"
            },
            "url": "https://api.github.com/repos/python/cpython/git/commits/e8e737bcf6d22927caebc30c5d57ac4634063219",
            "comment_count": 0,
            "verification": {
                "verified": True,
                "reason": "valid",
                "signature": "-----BEGIN PGP SIGNATURE-----\n\nwsBcBAABCAAQBQJiP0WHCRBK7hj4Ov3rIwAAez8IACwlKJNtRHyqcn/CuOnNoHUs\nApJnLP+/9wzsXnSHFTdxG8lu8d9xUhZSf36annanCJlF4uf+ZwRtBg7F4jmnpHue\n6tvEXqPPd+/64yLRYZuOpFx4soHKIyxKbx92Itc9jFgTIP6Q/AgdXeWgUdIdnust\nY+6Ky3hoz2UQ8WKPlm34GHXx71LdfrQafOGrzz9HvZwObKStDLxmqjt5x+N2T8aO\nBKQh0x1PqcUaGFxiFhtrgDMhLJLn853JOKcKK4Syltcne2//Ifc/Vvz+e5qmxGtU\nDuajuvuaa2XIEXmZ0g/xvX03hl1V1jcVYlICxPYK1Dxq28IPbDU/QXAcrSrk/iw=\n=TnxY\n-----END PGP SIGNATURE-----\n",
                "payload": "tree 6c0d4d51e8216f02fa0e6874aa4d78e20dd9397a\nparent 26cca8067bf5306e372c0e90036d832c5021fd90\nauthor Matthew Rahtz <matthew.rahtz@gmail.com> 1648313735 +0000\ncommitter GitHub <noreply@github.com> 1648313735 -0700\n\nbpo-43224: Implement PEP 646 grammar changes (GH-31018)\n\nCo-authored-by: Jelle Zijlstra <jelle.zijlstra@gmail.com>"
            }
        },
        "url": "https://api.github.com/repos/python/cpython/commits/e8e737bcf6d22927caebc30c5d57ac4634063219",
        "html_url": "https://github.com/python/cpython/commit/e8e737bcf6d22927caebc30c5d57ac4634063219",
        "comments_url": "https://api.github.com/repos/python/cpython/commits/e8e737bcf6d22927caebc30c5d57ac4634063219/comments",
        "author": {
            "login": "mrahtz",
            "id": 4431336,
            "node_id": "MDQ6VXNlcjQ0MzEzMzY=",
            "avatar_url": "https://avatars.githubusercontent.com/u/4431336?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/mrahtz",
            "html_url": "https://github.com/mrahtz",
            "followers_url": "https://api.github.com/users/mrahtz/followers",
            "following_url": "https://api.github.com/users/mrahtz/following{/other_user}",
            "gists_url": "https://api.github.com/users/mrahtz/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/mrahtz/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/mrahtz/subscriptions",
            "organizations_url": "https://api.github.com/users/mrahtz/orgs",
            "repos_url": "https://api.github.com/users/mrahtz/repos",
            "events_url": "https://api.github.com/users/mrahtz/events{/privacy}",
            "received_events_url": "https://api.github.com/users/mrahtz/received_events",
            "type": "User",
            "site_admin": False
        },
        "committer": {
            "login": "web-flow",
            "id": 19864447,
            "node_id": "MDQ6VXNlcjE5ODY0NDQ3",
            "avatar_url": "https://avatars.githubusercontent.com/u/19864447?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/web-flow",
            "html_url": "https://github.com/web-flow",
            "followers_url": "https://api.github.com/users/web-flow/followers",
            "following_url": "https://api.github.com/users/web-flow/following{/other_user}",
            "gists_url": "https://api.github.com/users/web-flow/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/web-flow/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/web-flow/subscriptions",
            "organizations_url": "https://api.github.com/users/web-flow/orgs",
            "repos_url": "https://api.github.com/users/web-flow/repos",
            "events_url": "https://api.github.com/users/web-flow/events{/privacy}",
            "received_events_url": "https://api.github.com/users/web-flow/received_events",
            "type": "User",
            "site_admin": False
        },
        "parents": [
            {
                "sha": "26cca8067bf5306e372c0e90036d832c5021fd90",
                "url": "https://api.github.com/repos/python/cpython/commits/26cca8067bf5306e372c0e90036d832c5021fd90",
                "html_url": "https://github.com/python/cpython/commit/26cca8067bf5306e372c0e90036d832c5021fd90"
            }
        ]
    },
    {
        "sha": "26cca8067bf5306e372c0e90036d832c5021fd90",
        "node_id": "C_kwDOBN0Z8doAKDI2Y2NhODA2N2JmNTMwNmUzNzJjMGU5MDAzNmQ4MzJjNTAyMWZkOTA",
        "commit": {
            "author": {
                "name": "Pablo Galindo Salgado",
                "email": "Pablogsal@gmail.com",
                "date": "2022-03-26T16:29:02Z"
            },
            "committer": {
                "name": "GitHub",
                "email": "noreply@github.com",
                "date": "2022-03-26T16:29:02Z"
            },
            "message": "bpo-47117: Don't crash if we fail to decode characters when the tokenizer buffers are uninitialized (GH-32129)\n\n\n\nAutomerge-Triggered-By: GH:pablogsal",
            "tree": {
                "sha": "d348b658e593bcae572d6b119de9e239bbbf1cc4",
                "url": "https://api.github.com/repos/python/cpython/git/trees/d348b658e593bcae572d6b119de9e239bbbf1cc4"
            },
            "url": "https://api.github.com/repos/python/cpython/git/commits/26cca8067bf5306e372c0e90036d832c5021fd90",
            "comment_count": 0,
            "verification": {
                "verified": True,
                "reason": "valid",
                "signature": "-----BEGIN PGP SIGNATURE-----\n\nwsBcBAABCAAQBQJiPz9OCRBK7hj4Ov3rIwAAkFoIAKaYh7MoKCm+yB8en1+j8wIr\nSJ5Vu+iqGQjrdrUw3OVYzTen061AKpugcruYplyC9pp6f0E6668fa6XjMaZCOZQ2\n2qRYCd2JSUrmldgG/RVuAfQWox1grqw3xn9qgOCAH+MTsvSHnUFq/DuWh3WoyQnK\n15QJP09yautT2OHD31cte32Tc7pgrXJnt8evKVE12CLlLJRHBS8i+fCCP77A55KD\nmy9OuGfE/PRbBj9AjiFleF07peQEnqJqafIYbygrwpIWHAn6tUyf1lNHbCpwcN/g\n3DOHMnEE0R2rIBqqqcgN/FTe3RHBjmT0Z/1u6vjvlM4roieC/afnDcD153Ry+R0=\n=WErY\n-----END PGP SIGNATURE-----\n",
                "payload": "tree d348b658e593bcae572d6b119de9e239bbbf1cc4\nparent ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864\nauthor Pablo Galindo Salgado <Pablogsal@gmail.com> 1648312142 +0000\ncommitter GitHub <noreply@github.com> 1648312142 -0700\n\nbpo-47117: Don't crash if we fail to decode characters when the tokenizer buffers are uninitialized (GH-32129)\n\n\n\nAutomerge-Triggered-By: GH:pablogsal"
            }
        },
        "url": "https://api.github.com/repos/python/cpython/commits/26cca8067bf5306e372c0e90036d832c5021fd90",
        "html_url": "https://github.com/python/cpython/commit/26cca8067bf5306e372c0e90036d832c5021fd90",
        "comments_url": "https://api.github.com/repos/python/cpython/commits/26cca8067bf5306e372c0e90036d832c5021fd90/comments",
        "author": {
            "login": "pablogsal",
            "id": 11718525,
            "node_id": "MDQ6VXNlcjExNzE4NTI1",
            "avatar_url": "https://avatars.githubusercontent.com/u/11718525?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/pablogsal",
            "html_url": "https://github.com/pablogsal",
            "followers_url": "https://api.github.com/users/pablogsal/followers",
            "following_url": "https://api.github.com/users/pablogsal/following{/other_user}",
            "gists_url": "https://api.github.com/users/pablogsal/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/pablogsal/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/pablogsal/subscriptions",
            "organizations_url": "https://api.github.com/users/pablogsal/orgs",
            "repos_url": "https://api.github.com/users/pablogsal/repos",
            "events_url": "https://api.github.com/users/pablogsal/events{/privacy}",
            "received_events_url": "https://api.github.com/users/pablogsal/received_events",
            "type": "User",
            "site_admin": False
        },
        "committer": {
            "login": "web-flow",
            "id": 19864447,
            "node_id": "MDQ6VXNlcjE5ODY0NDQ3",
            "avatar_url": "https://avatars.githubusercontent.com/u/19864447?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/web-flow",
            "html_url": "https://github.com/web-flow",
            "followers_url": "https://api.github.com/users/web-flow/followers",
            "following_url": "https://api.github.com/users/web-flow/following{/other_user}",
            "gists_url": "https://api.github.com/users/web-flow/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/web-flow/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/web-flow/subscriptions",
            "organizations_url": "https://api.github.com/users/web-flow/orgs",
            "repos_url": "https://api.github.com/users/web-flow/repos",
            "events_url": "https://api.github.com/users/web-flow/events{/privacy}",
            "received_events_url": "https://api.github.com/users/web-flow/received_events",
            "type": "User",
            "site_admin": False
        },
        "parents": [
            {
                "sha": "ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864",
                "url": "https://api.github.com/repos/python/cpython/commits/ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864",
                "html_url": "https://github.com/python/cpython/commit/ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864"
            }
        ]
    },
    {
        "sha": "ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864",
        "node_id": "C_kwDOBN0Z8doAKGVlOTEyYWQ2ZjY2YmI4Y2Y1YThhMmI0YTdlY2QyNzUyYmYwNzA4NjQ",
        "commit": {
            "author": {
                "name": "Alex Hedges",
                "email": "aphedges@users.noreply.github.com",
                "date": "2022-03-26T00:09:40Z"
            },
            "committer": {
                "name": "GitHub",
                "email": "noreply@github.com",
                "date": "2022-03-26T00:09:40Z"
            },
            "message": "bpo-47105: Cite grp.h instead of pwd.h in grp docs (GH-32091)",
            "tree": {
                "sha": "af6ab469cded427b9cf381ea34c6f57f6a4bc98a",
                "url": "https://api.github.com/repos/python/cpython/git/trees/af6ab469cded427b9cf381ea34c6f57f6a4bc98a"
            },
            "url": "https://api.github.com/repos/python/cpython/git/commits/ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864",
            "comment_count": 0,
            "verification": {
                "verified": True,
                "reason": "valid",
                "signature": "-----BEGIN PGP SIGNATURE-----\n\nwsBcBAABCAAQBQJiPlnECRBK7hj4Ov3rIwAAQ6QIAAofMdE1TYXNn97baJEWu3ei\nx4eZsB0fg4evu6W32nRK3bUwyzl+hNoaQ4WikyD7AtQeRaHU2Nk45byDPYpeQmI3\nKU8Fj6Q1BryQG7DIXgZOjRuRk06isYlC8nXvQ76Y3DZcTp4vBr1mIgJK7XaAfqgE\nnGRB2G2o//5wo/gbX1Z0OGHDqSWo8kUX828FkXopgfbBioON/ly30a2pM3mLJpAP\nq1oiwej70wY865f1ACWWMXp5WMMqM4lbeCj0dhclFY8aMiOSBfD5HsMnvIYZpReQ\nGYoIBzx1ucW6B7WqsEXBlTeGJCSs8cgp6I0j+OCAA1jz2dVn8aXT3bS72smo1x8=\n=QU/r\n-----END PGP SIGNATURE-----\n",
                "payload": "tree af6ab469cded427b9cf381ea34c6f57f6a4bc98a\nparent bad6ffaa64eecd33f4320ca31b1201b25cd8fc91\nauthor Alex Hedges <aphedges@users.noreply.github.com> 1648253380 -0400\ncommitter GitHub <noreply@github.com> 1648253380 -0400\n\nbpo-47105: Cite grp.h instead of pwd.h in grp docs (GH-32091)\n\n"
            }
        },
        "url": "https://api.github.com/repos/python/cpython/commits/ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864",
        "html_url": "https://github.com/python/cpython/commit/ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864",
        "comments_url": "https://api.github.com/repos/python/cpython/commits/ee912ad6f66bb8cf5a8a2b4a7ecd2752bf070864/comments",
        "author": {
            "login": "aphedges",
            "id": 14283972,
            "node_id": "MDQ6VXNlcjE0MjgzOTcy",
            "avatar_url": "https://avatars.githubusercontent.com/u/14283972?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/aphedges",
            "html_url": "https://github.com/aphedges",
            "followers_url": "https://api.github.com/users/aphedges/followers",
            "following_url": "https://api.github.com/users/aphedges/following{/other_user}",
            "gists_url": "https://api.github.com/users/aphedges/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/aphedges/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/aphedges/subscriptions",
            "organizations_url": "https://api.github.com/users/aphedges/orgs",
            "repos_url": "https://api.github.com/users/aphedges/repos",
            "events_url": "https://api.github.com/users/aphedges/events{/privacy}",
            "received_events_url": "https://api.github.com/users/aphedges/received_events",
            "type": "User",
            "site_admin": False
        },
        "committer": {
            "login": "web-flow",
            "id": 19864447,
            "node_id": "MDQ6VXNlcjE5ODY0NDQ3",
            "avatar_url": "https://avatars.githubusercontent.com/u/19864447?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/web-flow",
            "html_url": "https://github.com/web-flow",
            "followers_url": "https://api.github.com/users/web-flow/followers",
            "following_url": "https://api.github.com/users/web-flow/following{/other_user}",
            "gists_url": "https://api.github.com/users/web-flow/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/web-flow/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/web-flow/subscriptions",
            "organizations_url": "https://api.github.com/users/web-flow/orgs",
            "repos_url": "https://api.github.com/users/web-flow/repos",
            "events_url": "https://api.github.com/users/web-flow/events{/privacy}",
            "received_events_url": "https://api.github.com/users/web-flow/received_events",
            "type": "User",
            "site_admin": False
        },
        "parents": [
            {
                "sha": "bad6ffaa64eecd33f4320ca31b1201b25cd8fc91",
                "url": "https://api.github.com/repos/python/cpython/commits/bad6ffaa64eecd33f4320ca31b1201b25cd8fc91",
                "html_url": "https://github.com/python/cpython/commit/bad6ffaa64eecd33f4320ca31b1201b25cd8fc91"
            }
        ]
    },
    {
        "sha": "bad6ffaa64eecd33f4320ca31b1201b25cd8fc91",
        "node_id": "C_kwDOBN0Z8doAKGJhZDZmZmFhNjRlZWNkMzNmNDMyMGNhMzFiMTIwMWIyNWNkOGZjOTE",
        "commit": {
            "author": {
                "name": "Andrew Svetlov",
                "email": "andrew.svetlov@gmail.com",
                "date": "2022-03-25T22:26:23Z"
            },
            "committer": {
                "name": "GitHub",
                "email": "noreply@github.com",
                "date": "2022-03-25T22:26:23Z"
            },
            "message": "bpo-47062: Rename factory argument to loop_factory (GH-32113)",
            "tree": {
                "sha": "28413f729dde37eb2d912a881efdaae5eab88744",
                "url": "https://api.github.com/repos/python/cpython/git/trees/28413f729dde37eb2d912a881efdaae5eab88744"
            },
            "url": "https://api.github.com/repos/python/cpython/git/commits/bad6ffaa64eecd33f4320ca31b1201b25cd8fc91",
            "comment_count": 0,
            "verification": {
                "verified": True,
                "reason": "valid",
                "signature": "-----BEGIN PGP SIGNATURE-----\n\nwsBcBAABCAAQBQJiPkGPCRBK7hj4Ov3rIwAA+0EIAJNMfB2r9TXZ2LRC++SYlxwL\njObCT/7C/daRdzYimF6EJL2yt0XWT5VcfztHaItL8jBLnDbo6PPmSBYEOXmD0oyq\niR7eURnEfdpYfnRdAWMOGaLA/yluEGXtghf2g09yzy8DS7lG3neT3VMVa6f9e76v\neU/L7u99Ogl55HV3a4tkig8LG2UR3V1zIDLw1F+kzyGYbfRjuhl3qe/JdeJDg1FO\nAHbQViRK4KdbLO5vc9u83Fl3AjPa1DekhIgJ+MGNW4FVGkQlaWsf+nZbqK+DCjq5\n9VWbCiIeCPdtd1+V2P14XeULKhqKjhGMpU8UB04lR7hF8ZzmUPgTyDe+CEGWfcY=\n=8D8J\n-----END PGP SIGNATURE-----\n",
                "payload": "tree 28413f729dde37eb2d912a881efdaae5eab88744\nparent d03acd7270d66ddb8e987f9743405147ecc15087\nauthor Andrew Svetlov <andrew.svetlov@gmail.com> 1648247183 +0200\ncommitter GitHub <noreply@github.com> 1648247183 +0200\n\nbpo-47062: Rename factory argument to loop_factory (GH-32113)\n\n"
            }
        },
        "url": "https://api.github.com/repos/python/cpython/commits/bad6ffaa64eecd33f4320ca31b1201b25cd8fc91",
        "html_url": "https://github.com/python/cpython/commit/bad6ffaa64eecd33f4320ca31b1201b25cd8fc91",
        "comments_url": "https://api.github.com/repos/python/cpython/commits/bad6ffaa64eecd33f4320ca31b1201b25cd8fc91/comments",
        "author": {
            "login": "asvetlov",
            "id": 356399,
            "node_id": "MDQ6VXNlcjM1NjM5OQ==",
            "avatar_url": "https://avatars.githubusercontent.com/u/356399?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/asvetlov",
            "html_url": "https://github.com/asvetlov",
            "followers_url": "https://api.github.com/users/asvetlov/followers",
            "following_url": "https://api.github.com/users/asvetlov/following{/other_user}",
            "gists_url": "https://api.github.com/users/asvetlov/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/asvetlov/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/asvetlov/subscriptions",
            "organizations_url": "https://api.github.com/users/asvetlov/orgs",
            "repos_url": "https://api.github.com/users/asvetlov/repos",
            "events_url": "https://api.github.com/users/asvetlov/events{/privacy}",
            "received_events_url": "https://api.github.com/users/asvetlov/received_events",
            "type": "User",
            "site_admin": False
        },
        "committer": {
            "login": "web-flow",
            "id": 19864447,
            "node_id": "MDQ6VXNlcjE5ODY0NDQ3",
            "avatar_url": "https://avatars.githubusercontent.com/u/19864447?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/web-flow",
            "html_url": "https://github.com/web-flow",
            "followers_url": "https://api.github.com/users/web-flow/followers",
            "following_url": "https://api.github.com/users/web-flow/following{/other_user}",
            "gists_url": "https://api.github.com/users/web-flow/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/web-flow/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/web-flow/subscriptions",
            "organizations_url": "https://api.github.com/users/web-flow/orgs",
            "repos_url": "https://api.github.com/users/web-flow/repos",
            "events_url": "https://api.github.com/users/web-flow/events{/privacy}",
            "received_events_url": "https://api.github.com/users/web-flow/received_events",
            "type": "User",
            "site_admin": False
        },
        "parents": [
            {
                "sha": "d03acd7270d66ddb8e987f9743405147ecc15087",
                "url": "https://api.github.com/repos/python/cpython/commits/d03acd7270d66ddb8e987f9743405147ecc15087",
                "html_url": "https://github.com/python/cpython/commit/d03acd7270d66ddb8e987f9743405147ecc15087"
            }
        ]
    },
    {
        "sha": "d03acd7270d66ddb8e987f9743405147ecc15087",
        "node_id": "C_kwDOBN0Z8doAKGQwM2FjZDcyNzBkNjZkZGI4ZTk4N2Y5NzQzNDA1MTQ3ZWNjMTUwODc",
        "commit": {
            "author": {
                "name": "Duprat",
                "email": "yduprat@gmail.com",
                "date": "2022-03-25T22:01:21Z"
            },
            "committer": {
                "name": "GitHub",
                "email": "noreply@github.com",
                "date": "2022-03-25T22:01:21Z"
            },
            "message": "bpo-43352: Add a Barrier object in asyncio lib (GH-24903)\n\nCo-authored-by: Yury Selivanov <yury@edgedb.com>\r\nCo-authored-by: Andrew Svetlov <andrew.svetlov@gmail.com>",
            "tree": {
                "sha": "cffe25f0c26d55aef28c910dcf825747da99a6d4",
                "url": "https://api.github.com/repos/python/cpython/git/trees/cffe25f0c26d55aef28c910dcf825747da99a6d4"
            },
            "url": "https://api.github.com/repos/python/cpython/git/commits/d03acd7270d66ddb8e987f9743405147ecc15087",
            "comment_count": 0,
            "verification": {
                "verified": True,
                "reason": "valid",
                "signature": "-----BEGIN PGP SIGNATURE-----\n\nwsBcBAABCAAQBQJiPjuxCRBK7hj4Ov3rIwAARpgIAHICqVrCzLO9xMlW+9wJ6LIt\npRqsooxbWc/J+ylQ7BEt8xA7knelxKrUIzuCWbscp6NDoF9uIq9p9Eb4HqkhmC4r\nDobNrnbsPYJHbUqWvqrnlZ+C8uq+vpTby1/mJaQ4ixv4/k0JEEYxdgmlb7NZuhkJ\nLcu+Wr2XvhCDlyeKxtJHg0UDvZmY9P5KkEKnxGEA+RTqWIdQV++oXC7Q6aJ2OXqA\nqBVCph7YQ4dDpf8js0w0PfJxjKNqLNumIe35XRFQB4si8hjYFd74P4hRthJVE16x\nGvqI2g36ks6eZHv08/W+sX2hK5KmWsbCQG/6LERDu8vOS5ySlcv+GUo4q39V0Yg=\n=xUwr\n-----END PGP SIGNATURE-----\n",
                "payload": "tree cffe25f0c26d55aef28c910dcf825747da99a6d4\nparent 20e6e5636a06fe5e1472062918d0a302d82a71c3\nauthor Duprat <yduprat@gmail.com> 1648245681 +0100\ncommitter GitHub <noreply@github.com> 1648245681 +0200\n\nbpo-43352: Add a Barrier object in asyncio lib (GH-24903)\n\nCo-authored-by: Yury Selivanov <yury@edgedb.com>\r\nCo-authored-by: Andrew Svetlov <andrew.svetlov@gmail.com>"
            }
        },
        "url": "https://api.github.com/repos/python/cpython/commits/d03acd7270d66ddb8e987f9743405147ecc15087",
        "html_url": "https://github.com/python/cpython/commit/d03acd7270d66ddb8e987f9743405147ecc15087",
        "comments_url": "https://api.github.com/repos/python/cpython/commits/d03acd7270d66ddb8e987f9743405147ecc15087/comments",
        "author": {
            "login": "YvesDup",
            "id": 6217656,
            "node_id": "MDQ6VXNlcjYyMTc2NTY=",
            "avatar_url": "https://avatars.githubusercontent.com/u/6217656?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/YvesDup",
            "html_url": "https://github.com/YvesDup",
            "followers_url": "https://api.github.com/users/YvesDup/followers",
            "following_url": "https://api.github.com/users/YvesDup/following{/other_user}",
            "gists_url": "https://api.github.com/users/YvesDup/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/YvesDup/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/YvesDup/subscriptions",
            "organizations_url": "https://api.github.com/users/YvesDup/orgs",
            "repos_url": "https://api.github.com/users/YvesDup/repos",
            "events_url": "https://api.github.com/users/YvesDup/events{/privacy}",
            "received_events_url": "https://api.github.com/users/YvesDup/received_events",
            "type": "User",
            "site_admin": False
        },
        "committer": {
            "login": "web-flow",
            "id": 19864447,
            "node_id": "MDQ6VXNlcjE5ODY0NDQ3",
            "avatar_url": "https://avatars.githubusercontent.com/u/19864447?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/web-flow",
            "html_url": "https://github.com/web-flow",
            "followers_url": "https://api.github.com/users/web-flow/followers",
            "following_url": "https://api.github.com/users/web-flow/following{/other_user}",
            "gists_url": "https://api.github.com/users/web-flow/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/web-flow/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/web-flow/subscriptions",
            "organizations_url": "https://api.github.com/users/web-flow/orgs",
            "repos_url": "https://api.github.com/users/web-flow/repos",
            "events_url": "https://api.github.com/users/web-flow/events{/privacy}",
            "received_events_url": "https://api.github.com/users/web-flow/received_events",
            "type": "User",
            "site_admin": False
        },
        "parents": [
            {
                "sha": "20e6e5636a06fe5e1472062918d0a302d82a71c3",
                "url": "https://api.github.com/repos/python/cpython/commits/20e6e5636a06fe5e1472062918d0a302d82a71c3",
                "html_url": "https://github.com/python/cpython/commit/20e6e5636a06fe5e1472062918d0a302d82a71c3"
            }
        ]
    }
]

COMMITS_PAGE_OBJECTS = [
    Commit(
        author=Author(
            name="Matthew Rahtz",
            date="2022-03-26T16:55:35Z"
        ),
        message="bpo-43224: Implement PEP 646 grammar changes (GH-31018)\n\nCo-authored-by: Jelle Zijlstra <jelle.zijlstra@gmail.com>",
        comment_count=0
    ),
    Commit(
        author=Author(
            name="Pablo Galindo Salgado",
            date="2022-03-26T16:29:02Z"
        ),
        message="bpo-47117: Don't crash if we fail to decode characters when the tokenizer buffers are uninitialized (GH-32129)\n\n\n\nAutomerge-Triggered-By: GH:pablogsal",
        comment_count=0
    ),
    Commit(
        author=Author(
            name="Alex Hedges",
            date="2022-03-26T00:09:40Z"
        ),
        message="bpo-47105: Cite grp.h instead of pwd.h in grp docs (GH-32091)",
        comment_count=0
    ),
    Commit(
        author=Author(
            name="Andrew Svetlov",
            date="2022-03-25T22:26:23Z"
        ),
        message="bpo-47062: Rename factory argument to loop_factory (GH-32113)",
        comment_count=0
    ),
    Commit(
        author=Author(
            name="Duprat",
            date="2022-03-25T22:01:21Z"
        ),
        message="bpo-43352: Add a Barrier object in asyncio lib (GH-24903)\n\nCo-authored-by: Yury Selivanov <yury@edgedb.com>\r\nCo-authored-by: Andrew Svetlov <andrew.svetlov@gmail.com>",
        comment_count=0
    ),
]
