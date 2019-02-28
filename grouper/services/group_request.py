from typing import TYPE_CHECKING

from grouper.usecases.interfaces import GroupRequestInterface

if TYPE_CHECKING:
    from grouper.repositories.group_request import GroupRequestRepository
    from grouper.usecases.authorization import Authorization


class GroupRequestService(GroupRequestInterface):
    """High-level logic to manipulate requests to join groups."""

    def __init__(self, group_request_repository):
        # type: (GroupRequestRepository) -> None
        self.group_request_repository = group_request_repository

    def cancel_all_requests_for_user(self, user, authorization):
        # type: (str, Authorization) -> None
        pending_requests = self.group_request_repository.pending_requests_for_user(user)
        for request in pending_requests:
            self.group_request_repository.cancel_user_request(request, authorization)
