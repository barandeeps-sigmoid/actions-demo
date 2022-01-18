import sys

import requests


class RestApiCallToGithub:
    """Call to GitHub Rest API"""

    def __init__(self, url, params):
        self._url = url
        self._params = params

    def _get_closed_pr_list_json(self):
        data = requests.get(url=self._url, params=self._params)
        return data.json()

    def _perform_task(self):
        closed_pr_list = self._get_closed_pr_list_json()

        for item in range(0, 2):
            print(closed_pr_list[item]["url"])
            print(closed_pr_list[item]["number"])
            print(closed_pr_list[item]["merged_at"])
            print(closed_pr_list[item]["merge_commit_sha"])
            print("=======================")

        print()
        print(f"""{closed_pr_list[1]["merge_commit_sha"]},{closed_pr_list[0]["merge_commit_sha"]}""")

    def main(self):
        self._perform_task()


if __name__ == "__main__":
    URL = "https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls"
    PARAMS = {
        "base": sys.argv[1],
        "state": "closed"
    }
    RestApiCallToGithub(URL, PARAMS).main()
