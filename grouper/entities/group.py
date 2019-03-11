from datetime import timedelta
from typing import NamedTuple

Group = NamedTuple(
    "Group",
    [
        ("id", int),
        ("name", str),
        ("contact_email", str),
        ("description", str),
        ("enabled", bool),
        ("canjoin", bool),
        ("require_clickthru", bool),
        ("auto_expire", timedelta),
        ("audit_id", int),
    ],
)


class GroupNotFoundException(Exception):
    """Attempt to operate on a group not found in the storage layer."""

    def __init__(self, name):
        # type: (str) -> None
        msg = "Group {} not found".format(name)
        super(GroupNotFoundException, self).__init__(msg)
