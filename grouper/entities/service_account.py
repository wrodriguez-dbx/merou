from typing import NamedTuple

ServiceAccount = NamedTuple(
    "ServiceAccount", [
        ("id", int),
        ("name", str),
        ("enabled", bool),
        ("description", str),
        ("machine_set", str)
    ]
)

class ServiceAccountNotFoundException(Exception):
    """Attempt to operate on a service account not found in the storage layer."""

    def __init__(self, name):
        # type: (str) -> None
        msg = "Service account {} not found".format(name)
        super(ServiceAccountNotFoundException, self).__init__(msg)
