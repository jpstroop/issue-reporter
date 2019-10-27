from github import Github, InputGitTreeElement
from github_reporter import timestamp
from os import sep
from sys import stderr


class GithubCommitter:
    def __init__(self, github_token, repo_name):
        self.github = Github(github_token)
        self.repo = self.github.get_user().get_repo(repo_name)

    def commit(self, path_data_pairs, commit_message, branch):
        try:
            branch_ref = self.repo.get_git_ref(f"heads/{branch}")
            branch_sha = branch_ref.object.sha
            base_tree = self.repo.get_git_tree(branch_sha)
            element_list = self._build_element_list(path_data_pairs)
            tree = self.repo.create_git_tree(element_list, base_tree)
            parent = self.repo.get_git_commit(branch_sha)
            commit = self.repo.create_git_commit(commit_message, tree, [parent])
            print(f"{timestamp()} - Commit sha: {commit.sha}")
            branch_ref.edit(commit.sha)
        except Exception as e:
            print(f"{timestamp()} - {e}")
            return False
        else:
            return True

    def _build_element_list(self, path_data_pairs):
        element_list = []
        for path, data in path_data_pairs:
            print(f"{timestamp()} - Adding {path} to commit")
            element = InputGitTreeElement(path, "100644", "blob", data.read())
            element_list.append(element)
        return element_list
