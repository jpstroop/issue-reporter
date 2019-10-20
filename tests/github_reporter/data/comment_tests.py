from github_reporter.data.comment import Comment
from unittest.mock import Mock

class CommentTests():

# Mocking:
#   https://pygithub.readthedocs.io/en/latest/github_objects/IssueComment.html

    def test_delegates_with_username(self, comment_props_with_username):
        gh_comment = Mock(**comment_props_with_username)
        comment = Comment(gh_comment)
        assert comment.body == comment_props_with_username['body']
        assert comment.html_url == comment_props_with_username['html_url']
        assert comment.updated_at == comment_props_with_username['updated_at']
        assert comment.user_name == comment_props_with_username['user.name']

    def test_delegates_without_username(self, comment_props_without_username):
        gh_comment = Mock(**comment_props_without_username)
        comment = Comment(gh_comment)
        assert comment.body == comment_props_without_username['body']
        assert comment.html_url == comment_props_without_username['html_url']
        assert comment.updated_at == comment_props_without_username['updated_at']
        assert comment.user_name == comment_props_without_username['user.login']

    def test_cast_to_dict(self, comment_props_with_username):
        gh_comment = Mock(**comment_props_with_username)
        comment = Comment(gh_comment)
        expected = {
            'body' : comment_props_with_username['body'],
            'html_url' : comment_props_with_username['html_url'],
            'updated_at' : comment_props_with_username['updated_at'],
            'user_name' : comment_props_with_username['user.name']
        }
        assert dict(comment) == expected
