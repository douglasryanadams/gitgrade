import logging
from dataclasses import asdict
from typing import Optional, Dict, Final, Any

from repo.services.data import TestGrades
from repo.services.db_cache_service import check_cache, patch_cache
from repo.services.errors import CacheMiss
from repo.services.grade_calculator_service import calculate_grade
from repo.services.local_git_service import fetch_local_data
from repo.services.rest_api_service import fetch_api_data
from repo.services.url_service import identify_source

logger = logging.getLogger(__name__)


def repo_input_util(
    repo_url: str, github_token: Optional[str] = None
) -> Dict[str, Any]:
    repo_data = identify_source(repo_url)

    try:
        api_data, local_data = check_cache(repo_data)
    except CacheMiss:
        repo_data.sso_token = github_token

        api_data = fetch_api_data(repo_data)
        local_data = fetch_local_data(repo_data)
        patch_cache(repo_data, api_data, local_data)

    test_grades: Final[TestGrades] = calculate_grade(api_data, local_data)

    response_json = {
        "metadata": asdict(repo_data),
        "grades": asdict(test_grades),
        **asdict(api_data),
        **asdict(local_data),
    }
    return response_json
