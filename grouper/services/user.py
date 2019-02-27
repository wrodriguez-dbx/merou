from typing import TYPE_CHECKING

from grouper.constants import PERMISSION_ADMIN, PERMISSION_CREATE, USER_ADMIN
from grouper.usecases.interfaces import UserInterface

if TYPE_CHECKING:
    from grouper.repositories.interfaces import PermissionGrantRepository, UserRepository
    from typing import List


class UserService(UserInterface):
    """High-level logic to manipulate users."""

    def __init__(self, user_repository, permission_grant_repository):
        # type: (UserRepository, PermissionGrantRepository) -> None
        self.user_repository = user_repository
        self.permission_grant_repository = permission_grant_repository

    def disable_user(self, user):
        # type: (str) -> None
        return self.user_repository.disable_user(user)

    def groups_of_user(self, user):
        # type: (str) -> List[str]
        return self.user_repository.groups_of_user(user)

    def user_is_permission_admin(self, user):
        # type: (str) -> bool
        return self.permission_grant_repository.user_has_permission(user, PERMISSION_ADMIN)

    def user_is_user_admin(self, user):
        # type: (str) -> bool
        return self.permission_grant_repository.user_has_permission(user, USER_ADMIN)

    def user_can_create_permissions(self, user):
        # type: (str) -> bool
        return self.permission_grant_repository.user_has_permission(user, PERMISSION_CREATE)
