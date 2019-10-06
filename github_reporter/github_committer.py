from datetime import datetime as dt
from github import Github
from github import InputGitTreeElement
from os import sep
from sys import stderr

class GithubCommitter():
    def __init__(self, github_token, repo_path, repo_name='issue-reporter'):
        # repo_path is the path up to and including the root directory of the
        # git repo on the local file system, e.g.
        # /Users/jstroop/workspace/github_reporter
        self.github = Github(github_token)
        self.repo = self.github.get_user().get_repo(repo_name)
        self.repo_path = repo_path
        if not self.repo_path.endswith(sep):
            self.repo_path = f'{self.repo_path}{sep}'

    def commit(self, files=[], commit_message='', branch='master'):
        try:
            branch_ref = self.repo.get_git_ref(f'heads/{branch}')
            branch_sha = branch_ref.object.sha
            base_tree = self.repo.get_git_tree(branch_sha)
            element_list = self._build_element_list(files)
            tree = self.repo.create_git_tree(element_list, base_tree)
            parent = self.repo.get_git_commit(branch_sha)
            commit = self.repo.create_git_commit(commit_message, tree, [parent])
            print(f'{dt.now().isoformat()} - Commit sha: {commit.sha}')
            branch_ref.edit(commit.sha)
        except Exception as e:
            print(f'{dt.now().isoformat()} - {e}')
            return False
        else:
            return True


    def _build_element_list(self, files):
        element_list = []
        for file_path in files:
            with open(file_path, 'r') as input_file:
                data = input_file.read()
            local_path = file_path.split(self.repo_path)[-1]
            print(f'{dt.now().isoformat()} - Adding {local_path} to commit')
            element = InputGitTreeElement(local_path, '100644', 'blob', data)
            element_list.append(element)
        return element_list
