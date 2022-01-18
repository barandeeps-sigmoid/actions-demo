from dataclasses import dataclass, field
from datetime import datetime
import sys
import requests


@dataclass(order=True)
class PullRequest:
    sort_index: int = field(init=False, repr=False)
    number: int
    url: str
    updated_at: datetime
    merged_at: datetime
    closed_at: datetime
    created_at: datetime
    merge_commit_sha: str

    def __post_init__(self):
        self.sort_index = self.merged_at


class RestApiCallToGithub:
    """Call to GitHub Rest API"""

    def __init__(self, url, params, sha, date_format):
        self._url = url
        self._params = params
        self._sha = sha
        self._date_format = date_format

    def _get_cell_no(self, pull_requests):
        temp = -1
        for pr in pull_requests:
            temp = temp + 1
            if self._sha == pr.merge_commit_sha:
                return temp

    def _get_closed_pr_list(self):
        data = requests.get(url=URL, params=PARAMS)
        return data.json()

    def _get_sorted_pull_requests(self):
        data = requests.get(url=self._url, params=self._params)
        closed_pr_list = data.json()
        pull_requests = []

        for item in range(10):
            _number = closed_pr_list[item]["number"]
            _url = closed_pr_list[item]["url"]
            _updated_at = datetime.strptime(closed_pr_list[item]["updated_at"], self._date_format)
            _merged_at = datetime.strptime(closed_pr_list[item]["merged_at"], self._date_format)
            _closed_at = datetime.strptime(closed_pr_list[item]["closed_at"], self._date_format)
            _created_at = datetime.strptime(closed_pr_list[item]["created_at"], self._date_format)
            _merge_commit_sha = closed_pr_list[item]["merge_commit_sha"]

            pr = PullRequest(number=_number, url=_url, updated_at=_updated_at, created_at=_created_at,
                             closed_at=_closed_at, merged_at=_merged_at, merge_commit_sha=_merge_commit_sha)
            pull_requests.append(pr)

        pull_requests.sort(reverse=True)
        return pull_requests

    def _perform_task(self):
        closed_pr_list = self._get_sorted_pull_requests()
        matched_cell = self._get_cell_no(closed_pr_list)

        for pr in closed_pr_list:
            print(f"URL=>{pr.url}")
            print(f"PR no.=> {pr.number}")
            print(f"Created at=> {pr.created_at}")
            print(f"Closed at=> {pr.closed_at}")
            print(f"Merged at=> {pr.merged_at}")
            print(f"SHA=> {pr.merge_commit_sha}")
            print("=======================")

        print(f"Value matched at cell {matched_cell}")
        current_sha = self._sha
        previous_sha = closed_pr_list[matched_cell + 1].merge_commit_sha
        print(f"prev sha: {previous_sha}, cur sha: {current_sha}")

        print()
        print(f"""{previous_sha},{current_sha}""")

    def main(self):
        self._perform_task()


if __name__ == "__main__":
    branch_name=sys.argv[1]
    sha=sys.argv[2]
    # branch_name = "main"
    # sha = "fa24da82f8518e03d32768b57bf4e6b987776c8d"

    URL = "https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls"
    print(f"Branch => {branch_name} and SHA => {sha}")
    PARAMS = {
        "base": branch_name,
        "state": "closed"
    }
    RestApiCallToGithub(url=URL, params=PARAMS, sha=sha, date_format='%Y-%m-%dT%H:%M:%SZ').main()
