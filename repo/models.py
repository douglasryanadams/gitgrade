from typing import Any, Tuple

from django.db.models import (
    Model,
    CharField,
    IntegerField,
    DateField,
    BooleanField,
    Manager,
    UniqueConstraint,
)

from repo.services.data import UrlMetadata, ApiData, LocalData


class GitRepoDataManager(Manager):
    def get_by_natural_key(self, source: str, owner: str, repo: str) -> Any:
        return self.get(source=source, owner=owner, repo=repo)

    def create_git_repo_data(
        self, url_metadata: UrlMetadata, api_data: ApiData, local_data: LocalData
    ):
        git_repo_data = self.create(
            source=url_metadata.source,
            owner=url_metadata.owner,
            repo=url_metadata.repo,
            days_since_update=api_data.days_since_update,
            days_since_create=api_data.days_since_create,
            watchers=api_data.watchers,
            pull_requests_open=api_data.pull_requests_open,
            pull_requests_total=api_data.pull_requests_total,
            has_issues=api_data.has_issues,
            open_issues=api_data.open_issues,
            commits_total=local_data.commits_total,
            commits_recent=local_data.commits_recent,
            branch_count=local_data.branch_count,
            authors_total=local_data.authors_total,
            authors_recent=local_data.authors_recent,
            lines_of_code_total=local_data.lines_of_code_total,
            files_total=local_data.files_total,
        )

        return git_repo_data


class GitRepoData(Model):
    row_created_date = DateField(auto_now_add=True)
    row_updated_date = DateField(auto_now=True)

    # UrlMetadata
    source = CharField(max_length=255)
    owner = CharField(max_length=255)
    repo = CharField(max_length=255)

    # ApiData
    days_since_update = IntegerField()
    days_since_create = IntegerField()
    watchers = IntegerField()
    pull_requests_open = IntegerField()
    pull_requests_total = IntegerField()
    has_issues = BooleanField()
    open_issues = IntegerField()

    # LocalData
    commits_total = IntegerField()
    commits_recent = IntegerField()
    branch_count = IntegerField()
    authors_total = IntegerField()
    authors_recent = IntegerField()
    lines_of_code_total = IntegerField()
    files_total = IntegerField()

    objects = GitRepoDataManager()

    class Meta:
        #  pylint: disable=too-few-public-methods
        constraints = [
            UniqueConstraint(fields=["source", "owner", "repo"], name="unique_repo")
        ]

    def natural_key(self) -> Tuple[str, str, str]:
        return self.source, self.owner, self.repo
