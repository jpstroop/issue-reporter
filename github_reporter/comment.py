class Comment():
    def __init__(self, comment):
        self.body = comment.body
        self.html_url = comment.html_url
        self.updated_at = comment.updated_at.isoformat()
        self.user_name = comment.user.name
        if not self.user_name:
            self.user_name = comment.user.login
        self.__asdict = None

    @property
    def _asdict(self):
        if self.__asdict is None:
            vals = (self.user_name, self.updated_at, self.html_url, self.body)
            self.__asdict = dict(zip(self.keys(), vals))
        return self.__asdict

    def keys(self):
        return ('user_name','updated_at','html_url','body')

    def __getitem__(self, key):
        return self._asdict[key]
