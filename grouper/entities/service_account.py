from typing import NamedTuple

ServiceAccount = NamedTuple(
    "ServiceAccount",
    [("id", int), ("name", str), ("enabled", bool), ("description", str), ("machine_set", str)],
)


class ServiceAccountNotFoundException(Exception):
    """Attempt to operate on a service account not found in the storage layer."""

    def __init__(self, name):
        # type: (str) -> None
        msg = "Service account {} not found".format(name)
        super(ServiceAccountNotFoundException, self).__init__(msg)


class ServiceAccountHasOwnerException(Exception):
    """Attempt to add owner to a service account that already has an owner."""

    def __init__(self, name, group_id):
        # type: (str, int) -> None
        msg = "Service account {} already has an owner (id {})".format(name, group_id)
        super(ServiceAccountHasOwnerException, self).__init__(msg)
