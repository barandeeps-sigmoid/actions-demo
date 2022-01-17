import requests
import sys

URL = "https://api.github.com/repos/barandeeps-sigmoid/actions-demo/pulls?state=closed"
PARAMS = {"base": sys.argv[1]}


def get_closed_pr_list():
    data = requests.get(url=URL, params=PARAMS)
    return data.json()


def main():
    try:
        closed_pr_list = get_closed_pr_list()

        for item in range(0, 2):
            print(closed_pr_list[item]["url"])
            print(closed_pr_list[item]["number"])
            print(closed_pr_list[item]["merged_at"])
            print(closed_pr_list[item]["merge_commit_sha"])
            print("=======================")

        print()
        print(f"""{closed_pr_list[1]["merge_commit_sha"]},{closed_pr_list[0]["merge_commit_sha"]}""")
    except Exception as ex:
        print("Caught Exception")
        print(ex)


if __name__ == "__main__":
    print("Hello")
    main()
