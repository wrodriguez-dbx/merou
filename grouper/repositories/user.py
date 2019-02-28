from typing import TYPE_CHECKING

from grouper.entities.user import UserNotFoundException
from grouper.models.user import User as SQLUser
from grouper.repositories.interfaces import UserRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph

class GraphUserRepository(UserRepository):
    """Graph-aware storage layer for permissions."""

    def __init__(self, graph, repository):
        # type: (GroupGraph, UserRepository) -> None
        self.graph = graph
        self.repository = repository

    def disable_user(self, user):
        # type: (str) -> None
        return self.repository.disable_user(user)

    def groups_of_user(self, user):
        # type: (str) -> List[str]
        user_details = self.graph.get_user_details(user)
        return [group["name"] for group in user_details["groups"]]

class SQLUserRepository(UserRepository):
    """SQL storage layer for users."""

    def __init__(self, session):
        # type: (Session) -> None
        self.session = session

    def disable_user(self, username):
        # type: (str) -> None
        user = SQLUser.get(session, name=username)
        if not user:
            raise UserNotFoundException(username)
        user.enabled = False

    def groups_of_user(self, user):
        # type: (str) -> List[str]
        raise NotImplementedError()