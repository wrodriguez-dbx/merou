from typing import TYPE_CHECKING

from grouper.entities.user import UserNotFoundException
from grouper.models.service_account import ServiceAccount as SQLServiceAccount
from grouper.models.user import User as SQLUser
from grouper.repositories.interfaces import UserRepository, GroupEdgeRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from typing import List

class GraphUserRepository(UserRepository):
    """Graph-aware storage layer for users."""

    def __init__(self, graph, repository, group_edge_repository):
        # type: (GroupGraph, UserRepository, GroupEdgeRepository) -> None
        self.graph = graph
        self.repository = repository
        self.group_edge_repository = group_edge_repository

    def add_user_to_group(self, username, groupname, role):
        # type: (str, str, str) -> None
        return self.group_edge_repository.add_user_to_group(username, groupname, role)

    def disable_user(self, username):
        # type: (str) -> None
        return self.repository.disable_user(username)

    def enable_user(self, username):
        # type: (str) -> None
        return self.repository.enable_user(username)

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        return self.group_edge_repository.groups_of_user(username)

    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        return self.repository.mark_disabled_user_as_service_account(username)

class SQLUserRepository(UserRepository):
    """SQL storage layer for users."""

    def __init__(self, session):
        # type: (Session) -> None
        self.session = session

    def add_user_to_group(self, username, groupname, role):
        # type: (str, str, str) -> None
        raise NotImplementedError()

    def disable_user(self, username):
        # type: (str) -> None
        user = SQLUser.get(self.session, name=username)
        if not user:
            raise UserNotFoundException(username)
        user.enabled = False

    def enable_user(self, username):
        # type: (str) -> None
        user = SQLUser.get(self.session, name=username)
        if not user:
            raise UserNotFoundException(username)
        user.enabled = True

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        raise NotImplementedError()

    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        user = SQLUser.get(self.session, name=username)
        if not user:
            raise UserNotFoundException(username)

        service_account = SQLServiceAccount(
            user_id=user.id,
        )
        service_account.add(self.session)

        user.is_service_account = True

