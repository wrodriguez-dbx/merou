from typing import TYPE_CHECKING

from grouper.entities.user import UserNotFoundException
from grouper.models.service_account import ServiceAccount as SQLServiceAccount
from grouper.models.user import User as SQLUser
from grouper.repositories.interfaces import UserRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from grouper.repositories.group_request import GroupRequestRepository
    from grouper.repositories.interfaces import GroupEdgeRepository
    from typing import List


class UserIsMemberOfGroupsException(Exception):
    """Operation failed because user is a member of groups."""

    def __init__(self, username):
        # type: (str) -> None
        msg = "User {} is a member of one or more groups".format(username)
        super(UserIsMemberOfGroupsException, self).__init__(msg)


class UserHasPendingRequestsException(Exception):
    """Operation failed because user has pending requests."""

    def __init__(self, username):
        # type: (str) -> None
        msg = "User {} has one or more pending requests".format(username)
        super(UserHasPendingRequestsException, self).__init__(msg)


class GraphUserRepository(UserRepository):
    """Graph-aware storage layer for users."""

    def __init__(self, graph, repository):
        # type: (GroupGraph, UserRepository) -> None
        self.graph = graph
        self.repository = repository

    def add_user_to_group(self, username, groupname, role):
        # type: (str, str, str) -> None
        return self.repository.add_user_to_group(username, groupname, role)

    def disable_user(self, username):
        # type: (str) -> None
        return self.repository.disable_user(username)

    def enable_user(self, username):
        # type: (str) -> None
        return self.repository.enable_user(username)

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        return self.repository.groups_of_user(username)

    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        return self.repository.mark_disabled_user_as_service_account(username)


class SQLUserRepository(UserRepository):
    """SQL storage layer for users."""

    def __init__(self, session, group_edge_repository, group_request_repository):
        # type: (Session, GroupEdgeRepository, GroupRequestRepository) -> None
        self.session = session
        self.group_edge_repository = group_edge_repository
        self.group_request_repository = group_request_repository

    def add_user_to_group(self, username, groupname, role):
        # type: (str, str, str) -> None
        return self.group_edge_repository.add_user_to_group(username, groupname, role)

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
        return self.group_edge_repository.groups_of_user(username)

    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        user = SQLUser.get(self.session, name=username)
        if not user:
            raise UserNotFoundException(username)

        if self.groups_of_user(username) != []:
            raise UserIsMemberOfGroupsException(username)

        if self.group_request_repository.pending_requests_for_user(username) != []:
            raise UserHasPendingRequestsException(username)

        service_account = SQLServiceAccount(user_id=user.id)
        service_account.add(self.session)

        user.is_service_account = True
