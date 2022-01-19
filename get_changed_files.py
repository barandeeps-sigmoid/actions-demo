import sys
from dataclasses import dataclass

import requests


@dataclass
class RestApiCallToGithub:
    """Call to GitHub Rest API"""

    _url: str
    _folder_filter: str

    def _get_pr_changed_files(self):
        data = requests.get(url=self._url)
        return data.json()

    def _get_changed_files(self):
        changed_files_list = self._get_pr_changed_files()
        changed_files_filtered = []
        counter = 0
        for item in changed_files_list:
            print(f"Filename=>{item['filename']}")
            print(f"Status=>{item['status']}")
            if item['filename'].startswith(self._folder_filter):
                changed_files_filtered.append(item['filename'])
            counter += 1
            print("==========================")

        print(f"Total changed files {counter}")
        print(f"Files matching filter count {len(changed_files_filtered)}")
        print(f"Files matching filter {';'.join(changed_files_filtered)}")

    def _perform_task(self):
        self._get_changed_files()

    def main(self):
        self._perform_task()


if __name__ == "__main__":
    # pr_number = "14"
    # folder_filter="snowflake/"
    pr_number = sys.argv[1]
    folder_filter = sys.argv[2]

    URL = f"https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls/{pr_number}/files"
    print(f"Extracting changed files for PR#=>{pr_number}")
    print("==========================")
    RestApiCallToGithub(_url=URL, _folder_filter=folder_filter) \
        .main()
