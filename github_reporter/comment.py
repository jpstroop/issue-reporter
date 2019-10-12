from github_reporter.abstract_data_class import AbstractDataClass

class Comment(AbstractDataClass):
    def __init__(self, comment):
        super().__init__()
        self.body = comment.body
        self.html_url = comment.html_url
        self.updated_at = comment.updated_at.isoformat()
        self.user_name = comment.user.name
        if not self.user_name:
            self.user_name = comment.user.login

    @property
    def _vals(self):
        return (self.user_name, self.updated_at, self.html_url, self.body)

    def keys(self):
        return ('user_name','updated_at','html_url','body')
