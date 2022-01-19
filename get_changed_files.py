import sys
from dataclasses import dataclass

import requests


@dataclass
class RestApiCallToGithub:
    """Call to GitHub Rest API"""

    _url: str
    _folder_filter: str
    _bearer_token: str

    def _get_pr_changed_files(self):
        headers = {"Authorization": f"Bearer {self._bearer_token}"}
        data = requests.get(url=self._url, headers=headers)
        return data.json()

    def _get_changed_files(self):
        changed_files_list = self._get_pr_changed_files()
        changed_files_matched_filter = []
        changed_files_skipped_filter = []
        total_changed_counter = 0
        for item in changed_files_list:
            print(f"Filename=>{item['filename']}; Status=>{item['status']}")
            if item['filename'].startswith(self._folder_filter) and item['status'] in ('added', 'modified'):
                changed_files_matched_filter.append(item['filename'])
            else:
                changed_files_skipped_filter.append(item['filename'])
            total_changed_counter += 1

        print(f"Total changed files {total_changed_counter}")
        print("==========================")
        print(f"Files skipped filter count {len(changed_files_skipped_filter)}")
        print(f"Files skipped filter {';'.join(changed_files_skipped_filter)}")
        print("==========================")
        print(f"Files matching filter count {len(changed_files_matched_filter)}")
        print("Files matching filter ")
        print(';'.join(changed_files_matched_filter))

    def _perform_task(self):
        self._get_changed_files()

    def main(self):
        self._perform_task()


if __name__ == "__main__":
    pr_number = sys.argv[1]
    folder_filter = sys.argv[2]
    bearer_token = sys.argv[3]
    URL = f"https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls/{pr_number}/files"
    print(f"Extracting changed files for PR#=>{pr_number}")
    print("==========================")
    RestApiCallToGithub(_url=URL, _folder_filter=folder_filter,_bearer_token=bearer_token) \
        .main()
