from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grouper.entities.pagination import PaginatedList, Pagination
    from grouper.entities.permission import Permission
    from grouper.entities.permission_grant import PermissionGrant
    from grouper.usecases.list_permissions import ListPermissionsSortKey
    from typing import List, Optional


class PermissionRepository(object):
    """Abstract base class for permission repositories."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_permission(self, name):
        # type: (str) -> Optional[Permission]
        pass

    @abstractmethod
    def disable_permission(self, name):
        # type: (str) -> None
        pass

    @abstractmethod
    def list_permissions(self, pagination, audited_only):
        # type: (Pagination[ListPermissionsSortKey], bool) -> PaginatedList[Permission]
        pass


class PermissionGrantRepository(object):
    """Abstract base class for permission grant repositories."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def permissions_for_user(self, user):
        # type: (str) -> List[PermissionGrant]
        pass

    @abstractmethod
    def user_has_permission(self, user, permission):
        # type: (str, str) -> bool
        pass


class ServiceAccountRepository(object):
    """Abstract base class for service account repositories."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def assign_service_account_to_group(self, username, groupname):
        # type: (str, str) -> None
        pass

    @abstractmethod
    def enable_service_account(self, name):
        # type: (str) -> None
        pass

    @abstractmethod
    def set_service_account_description(self, name, description):
        # type: (str, str) -> None
        pass

    @abstractmethod
    def set_service_account_mdbset(self, name, mdbset):
        # type: (str, str) -> None
        pass


class UserRepository(object):
    """Abstract base class for user repositories."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def add_user_to_group(self, username, groupname):
        # type: (str, str) -> None
        pass

    @abstractmethod
    def disable_user(self, username):
        # type: (str) -> None
        pass

    @abstractmethod
    def enable_user(self, username):
        # type: (str) -> None
        pass

    @abstractmethod
    def groups_of_user(self, username):
        # type: (str) -> List[str]
        pass

    @abstractmethod
    def mark_disabled_user_as_service_account(self, username):
        # type: (str) -> None
        # WARNING: This function encodes the fact that the user and service account repos
        # are in fact the same thing, as it assumes that a service account is just a user
        # that is marked in a special way. This is a temporary breaking of the abstractions
        # and will have to be cleaned up once the repositories are properly separate.
        pass
