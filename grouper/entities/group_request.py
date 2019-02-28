from enum import Enum
from typing import NamedTuple


class RequestStatus(Enum):
    PENDING = "pending"
    ACTIONED = "actioned"
    CANCELLED = "cancelled"


UserGroupRequest = NamedTuple(
    "GroupRequest", [("id", int), ("user", str), ("group", str), ("status", RequestStatus)]
)
