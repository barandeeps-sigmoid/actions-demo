import operator
import sys
from dataclasses import dataclass
from datetime import datetime

import requests

FORMAT = '%Y-%m-%dT%H:%M:%SZ'


@dataclass(order=True)
class PullRequest:
    number: int
    url: str
    updated_at: str
    merged_at: str
    closed_at: datetime
    created_at: str
    merge_commit_sha: str


class RestApiCallToGithub:
    """Call to GitHub Rest API"""

    def __init__(self, url, params, sha):
        self._url = url
        self._params = params
        self._sha = sha

    def _get_closed_pr_list_json(self):
        data = requests.get(url=self._url, params=self._params)
        return data.json()

    def _get_cell_no(self, pull_requests):

        cell = -1
        for pr in pull_requests:
            cell = cell + 1
            if self._sha == pr.merge_commit_sha:
                return cell

    def _get_closed_pr_list_json(self, key="closed_at"):
        data = requests.get(url=self._url, params=self._params)
        closed_pr_list = data.json()
        pull_requests = []

        for item in range(5):
            _number = closed_pr_list[item]["number"]
            _url = closed_pr_list[item]["url"]
            _updated_at = datetime.strptime(closed_pr_list[item]["updated_at"], FORMAT)
            _merged_at = datetime.strptime(closed_pr_list[item]["merged_at"], FORMAT)
            _closed_at = datetime.strptime(closed_pr_list[item]["closed_at"], FORMAT)
            _created_at = datetime.strptime(closed_pr_list[item]["created_at"], FORMAT)
            _merge_commit_sha = closed_pr_list[item]["merge_commit_sha"]

            pr = PullRequest(number=_number, url=_url, updated_at=_updated_at, created_at=_created_at,
                             closed_at=_closed_at, merged_at=_merged_at, merge_commit_sha=_merge_commit_sha)
            pull_requests.append(pr)

        pull_requests.sort(key=operator.attrgetter(key))
        return pull_requests

    def _perform_task(self):
        closed_pr_list = self._get_closed_pr_list_json()

        matched_cell = self._get_cell_no(closed_pr_list)
        print(f"Value matched at cell {matched_cell}")
        current_sha = self._sha
        previous_sha = closed_pr_list[matched_cell + 1].merge_commit_sha
        print(f"prev sha: {previous_sha}, cur sha: {current_sha}")

        for item in range(matched_cell, matched_cell + 2):
            print(f"URL=>{closed_pr_list[item].url}")
            print(f"PR no.=> {closed_pr_list[item].number}")
            print(f"Created at=> {closed_pr_list[item].created_at}")
            print(f"Closed at=> {closed_pr_list[item].closed_at}")
            print(f"Merged at=> {closed_pr_list[item].merged_at}")
            print(f"SHA=> {closed_pr_list[item].merge_commit_sha}")
            print("=======================")

        print()
        print(f"""{previous_sha},{current_sha}""")

    def main(self):
        self._perform_task()


if __name__ == "__main__":
    URL = "https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls"
    print(f"Branch => {sys.argv[1]} and SHA => {sys.argv[2]}")
    PARAMS = {
        "base": sys.argv[1],
        "state": "closed"
    }
    RestApiCallToGithub(URL, PARAMS, sys.argv[2]).main()
