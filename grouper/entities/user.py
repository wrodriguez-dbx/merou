from typing import NamedTuple

User = NamedTuple("User", [("id", int), ("username", str), ("enabled", bool)])


class UserNotFoundException(Exception):
    """Attempt to operate on a user not found in the storage layer."""

    def __init__(self, name):
        # type: (str) -> None
        msg = "User {} not found".format(name)
        super(UserNotFoundException, self).__init__(msg)
