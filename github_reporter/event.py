class Event():
    def __init__(self, event):
        self.actor_name = event.actor.name
        self.created_at = event.created_at
        self.type = event.event

    def keys(self):
        return ('actor_name', 'created_at', 'type')

    def __getitem__(self, key):
        vals = (self.actor_name, self.created_at.isoformat(), self.type)
        return dict(zip(self.keys(), vals))[key]
