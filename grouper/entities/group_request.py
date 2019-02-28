from enum import Enum
from typing import NamedTuple


class GroupRequestStatus(Enum):
    PENDING = "pending"
    ACTIONED = "actioned"
    CANCELLED = "cancelled"


UserGroupRequest = NamedTuple(
    "GroupRequest",
    [
        ("id", int),
        ("user", str),
        ("group", str),
        ("requester", str),
        ("status", GroupRequestStatus),
    ],
)
