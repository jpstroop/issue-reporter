from faker.providers import BaseProvider
from random import choice

# Note that the class name _must_ be `Provider`.
class Provider(BaseProvider):
    def event_type(self):
        # See: https://developer.github.com/v3/issues/events/
        types = ('added_to_project','assigned','closed',
            'converted_note_to_issue','demilestoned','head_ref_deleted',
            'head_ref_restored','labeled','locked','mentioned',
            'marked_as_duplicate','merged','milestoned',
            'moved_columns_in_project','referenced','removed_from_project',
            'renamed','reopened','review_dismissed','review_requested',
            'review_request_removed','subscribed','unassigned','unlabeled',
            'unlocked','unmarked_as_duplicate','user_blocked')
        return choice(types)
