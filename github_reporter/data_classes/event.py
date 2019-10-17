from github_reporter.data_classes.anstract_data_class import AbstractDataClass

class Event(AbstractDataClass):
    def __init__(self, event):
        super().__init__()
        self.actor_name = event.actor.name
        self.created_at = event.created_at
        self.type = event.event

    @property
    def _vals(self):
        return (self.actor_name, self.created_at, self.type)

    def keys(self):
        return ('actor_name', 'created_at', 'type')
