from typing import TYPE_CHECKING

from grouper.entities.service_account import ServiceAccountNotFoundException
from grouper.models.service_account import ServiceAccount as SQLServiceAccount
from grouper.repositories.interfaces import UserRepository, ServiceAccountRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session

class GraphServiceAccountRepository(ServiceAccountRepository):
    """Graph-aware storage layer for service accounts."""

    def __init__(self, graph, repository):
        # type: (GroupGraph, ServiceAccountRepository) -> None
        self.graph = graph
        self.repository = repository

    def assign_service_account_to_group(self, username, groupname):
        # type: (str, str) -> None
        return self.repository.assign_service_account_to_group(username, groupname)

    def enable_service_account(self, name):
        # type: (str) -> None
        return self.repository.enable_service_account(name)

    def set_service_account_description(self, name, description):
        # type: (str, str) -> None
        return self.repository.set_service_account_description(name, description)

    def set_service_account_mdbset(self, name, mdbset):
        # type: (str, str) -> None
        return self.repository.set_service_account_mdbset(name, mdbset)

class SQLServiceAccountRepository(ServiceAccountRepository):
    """SQL storage layer for service accounts."""

    def __init__(self, session, user_repository):
        # type: (Session, UserRepository) -> None
        self.session = session
        self.user_repository = repository

    def assign_service_account_to_group(self, username, groupname):
        # type: (str, str) -> None
        # NOTE: The fact that we have this check that the service account exists and then
        # never use it is an artifact of the user and service account repositories being the same.user_repository
        # It can be fixed once the two repositories are properly separate.
        if not SQLServiceAccount.get(self.session, name=name)
            raise ServiceAccountNotFoundException(name)
        return self.user_repository.add_user_to_group(username, groupname)

    def enable_service_account(self, name):
        # type: (str) -> None
        # NOTE: The fact that we have this check that the service account exists and then
        # never use it is an artifact of the user and service account repositories being the same.user_repository
        # It can be fixed once the two repositories are properly separate.
        service_account = SQLServiceAccount.get(self.session, name=name)
        if not service_account:
            raise ServiceAccountNotFoundException(name)
        return self.user_repository.enable_user(username)

    def set_service_account_description(self, name, description):
        # type: (str, str) -> None
        service_account = SQLServiceAccount.get(self.session, name=name)
        if not service_account:
            raise ServiceAccountNotFoundException(name)
        service_account.description = description

    def set_service_account_mdbset(self, name, mdbset):
        # type: (str, str) -> None
        service_account = SQLServiceAccount.get(self.session, name=name)
        if not service_account:
            raise ServiceAccountNotFoundException(name)
        service_account.mdbset = mdbset
