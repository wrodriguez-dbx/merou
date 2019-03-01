from typing import TYPE_CHECKING

from grouper.entities.user import UserNotFoundException
from grouper.models.user import User as SQLUser
from grouper.repositories.interfaces import UserRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import session

class GraphUserRepository(UserRepository):
    """Graph-aware storage layer for users."""

    def __init__(self, graph, repository):
        # type: (GroupGraph, UserRepository) -> None
        self.graph = graph
        self.repository = repository

    def add_user_to_group(self, username, groupname):
        # type: (str, str) -> None
        return self.repository.add_user_to_group(username, groupname)

    def disable_user(self, username):
        # type: (str) -> None
        return self.repository.disable_user(username)

    def enable_user(self, username):
        # type: (str) -> None
        return self.repository.enable_user(username)

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        user_details = self.graph.get_user_details(username)
        return [group["name"] for group in user_details["groups"]]

    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        return self.repository.mark_disabled_user_as_service_account(username)

class SQLUserRepository(UserRepository):
    """SQL storage layer for users."""

    def __init__(self, session):
        # type: (Session) -> None
        self.session = session

    def add_user_to_group(self, username, groupname):
        # type: (str, str) -> None

    def disable_user(self, username):
        # type: (str) -> None
        user = SQLUser.get(session, name=username)
        if not user:
            raise UserNotFoundException(username)
        user.enabled = False

    def enable_user(self, username):
        # type: (str) -> None
        user = SQLUser.get(session, name=username)
        if not user:
            raise UserNotFoundException(username)
        user.enabled = True

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        raise NotImplementedError()

    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        user = SQLUser.get(session, name=username)
        if not user:
            raise UserNotFoundException(username)
        user.is_service_account = True
