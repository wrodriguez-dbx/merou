from typing import TYPE_CHECKING

from grouper.usecases.interfaces import ServiceAccountInterface

if TYPE_CHECKING:
    from grouper.repositories.interfaces import

class ServiceAccountService(ServiceAccountInterface):
    """High-level logic to manipulate service accounts."""

    def __init__(self, service_account_repository):
        # type: (ServiceAccountRepository) -> None
        self.service_account_repository = service_account_repository

    def create_service_account_from_disabled_user(self, user):
        # type: (str) -> None
        assert "user not in any groups"
        assert "user has no pending reqs"

        # WARNING: This logic relies on the fact that the user and service account repos
        # are in fact the same thing, as it never explicitly removes the user from the
        # user repo. This is a temporary breaking of the abstractions and will have to be
        # cleaned up once the repositories are properly separate.
        self.service_account_repository.mark_disabled_user_as_service_account(user)

    def enable_service_account(self, user, owner):
        # type: (str, str) -> None
        self.service_account_repository.assign_service_account_to_group(user, owner)
        self.service_account_repository.enable_service_account(user)