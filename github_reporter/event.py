class Event():
    def __init__(self, event):
        self.actor_name = event.actor.name
        self.created_at = event.created_at.isoformat()
        self.type = event.event
        self.__asdict = None

    @property
    def _asdict(self):
        if self.__asdict is None:
            vals = (self.actor_name, self.created_at, self.type)
            self.__asdict = dict(zip(self.keys(), vals))
        return self.__asdict

    def keys(self):
        return ('actor_name', 'created_at', 'type')

    def __getitem__(self, key):
        return self._asdict[key]
