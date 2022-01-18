import requests
from datetime import datetime
from dataclasses import dataclass, field

FORMAT = '%Y-%m-%dT%H:%M:%SZ'
SHA = "fa24da82f8518e03d32768b57bf4e6b987776c8d"
URL = "https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls?state=closed"
# PARAMS= {"base": sys.argv[1]}
PARAMS= {"base": "main"}


def _get_closed_pr_list():
    data = requests.get(url=URL, params=PARAMS)
    return data.json()


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
        self.sort_index = self.closed_at


def _get_cell_no(pull_requests):

    temp = -1
    for pr in pull_requests:
        temp = temp + 1
        if SHA == pr.merge_commit_sha:
            return temp


def _get_sorted_pull_requests():
    data = requests.get(url=URL, params=PARAMS)
    closed_pr_list = data.json()
    pull_requests = []

    for item in range(10):
        _number = closed_pr_list[item]["number"]
        _url = closed_pr_list[item]["url"]
        _updated_at = datetime.strptime(closed_pr_list[item]["updated_at"], FORMAT)
        _merged_at = datetime.strptime(closed_pr_list[item]["merged_at"], FORMAT)
        _closed_at = datetime.strptime(closed_pr_list[item]["closed_at"], FORMAT)
        _created_at = datetime.strptime(closed_pr_list[item]["created_at"], FORMAT)
        _merge_commit_sha = closed_pr_list[item]["merge_commit_sha"]

        pr = PullRequest(number=_number, url=_url, updated_at=_updated_at, created_at=_created_at, closed_at=_closed_at, merged_at=_merged_at, merge_commit_sha=_merge_commit_sha)
        pull_requests.append(pr)

    pull_requests.sort(reverse=True)
    return pull_requests


def main():
    pull_requests = _get_sorted_pull_requests()

    for pr in pull_requests:
        print(f"PR number: {pr.number}")
        print(f"closed at: {pr.closed_at}")
        print(f"merge commit sha: {pr.merge_commit_sha}")
        print()

    temp = _get_cell_no(pull_requests)
    print(temp)
    current_sha = SHA
    previous_sha = pull_requests[temp+1].merge_commit_sha
    print(f"prev sha: {previous_sha}, cur sha: {current_sha}")


if __name__ == "__main__":
    main()