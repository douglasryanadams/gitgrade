# mypy: ignore-errors
from typing import Any, Tuple

from django.db.models import (
    Model,
    CharField,
    IntegerField,
    DateField,
    Manager,
    UniqueConstraint,
    FloatField,
)

from repo.data.general import RepoRequest
from repo.data.git_data import GitData


class CacheDataManager(Manager):
    def get_by_natural_key(self, source: str, owner: str, repo: str) -> Any:
        return self.get(source=source, owner=owner, repo=repo)

    def create_git_repo_data(self, version: str, url_metadata: RepoRequest, data: GitData):
        git_repo_data = self.create(
            version=version,
            source=url_metadata.source,
            owner=url_metadata.owner,
            repo=url_metadata.repo,
            # code_lines_of_code=data.code.lines_of_code,
            # code_file_count=data.code.file_count,
            pull_request_count=data.pull_request.count,
            pull_request_count_open=data.pull_request.count_open,
            # commit_all_count=data.commit_all.count,
            # commit_all_count_primary_author=data.commit_all.count_primary_author,
            # commit_all_interval_mean=data.commit_all.interval.mean,
            # commit_all_interval_standard_deviation=data.commit_all.interval.standard_deviation,
            commit_recent_count=data.commit_recent.count,
            commit_recent_count_primary_author=data.commit_recent.count_primary_author,
            commit_recent_interval_mean=data.commit_recent.interval.mean,
            commit_recent_interval_standard_deviation=data.commit_recent.interval.standard_deviation,
            contributor_days_since_create=data.contributor.days_since_create,
            contributor_days_since_commit=data.contributor.days_since_commit,
            # contributor_author_count_all=data.contributor.author_count_all,
            contributor_author_count_recent=data.contributor.author_count_recent,
            popularity_watcher_count=data.popularity.watcher_count,
            popularity_open_issue_count=data.popularity.open_issue_count,
        )

        return git_repo_data


class CacheData(Model):
    """
    This model represents that data that's cached in the DB.

    All of these fields have a 1-1 relationship with the primary
    key, so it didn't seem worth it to normalize the data into
    separate tables.

    We could cache all this as JSON blobs but we have the DB so
    we might as well properly organize the data for now.
    """

    row_created_date = DateField(auto_now_add=True)
    row_updated_date = DateField(auto_now=True)

    version = CharField(max_length=32)

    # UrlMetadata + Primary Key
    source = CharField(max_length=255)
    owner = CharField(max_length=255)
    repo = CharField(max_length=255)

    # Data
    # code_lines_of_code = IntegerField()
    # code_file_count = IntegerField()

    pull_request_count = IntegerField()
    pull_request_count_open = IntegerField()

    # commit_all_count = IntegerField()
    # commit_all_count_primary_author = IntegerField()
    # commit_all_interval_mean = FloatField()
    # commit_all_interval_standard_deviation = FloatField()

    commit_recent_count = IntegerField()
    commit_recent_count_primary_author = IntegerField()
    commit_recent_interval_mean = FloatField()
    commit_recent_interval_standard_deviation = FloatField()

    contributor_days_since_create = IntegerField()
    contributor_days_since_commit = IntegerField()
    # contributor_author_count_all = IntegerField()
    contributor_author_count_recent = IntegerField()

    popularity_watcher_count = IntegerField()
    popularity_open_issue_count = IntegerField()

    objects = CacheDataManager()

    class Meta:
        #  pylint: disable=too-few-public-methods
        constraints = [UniqueConstraint(fields=["source", "owner", "repo"], name="unique_repo")]

    def natural_key(self) -> Tuple[str, str, str]:
        return self.source, self.owner, self.repo
