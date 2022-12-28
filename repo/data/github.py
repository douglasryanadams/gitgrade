"""
This module contains data classes representing
responses from Github's API.

Note: only the data we use or are likely to use is
modeled here, many other fields exist and may be
added as needed.
"""
from dataclasses import dataclass


@dataclass
class Repo:
    id: int  # pylint: disable=invalid-name
    name: str
    created_at: str
    updated_at: str
    language: str
    open_issues_count: int
    watchers_count: int
    forks_count: int


@dataclass
class Author:
    name: str
    date: str


@dataclass
class Commit:
    author: Author
    message: str
    comment_count: int


@dataclass
class Release:
    tag: str
    created_at: str
