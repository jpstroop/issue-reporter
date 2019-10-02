class Comment():
    def __init__(self, comment):
        self.body = comment.body
        self.html_url = comment.html_url
        self.updated_at = comment.updated_at
        self.user_name = comment.user.name
        if not self.user_name:
            self.user_name = comment.user.login

    def keys(self):
        return ('user_name','updated_at','html_url','body')

    def __getitem__(self, key):
        vals = (self.user_name, self.updated_at.isoformat(), self.html_url,
            self.body)
        return dict(zip(self.keys(), vals))[key]
