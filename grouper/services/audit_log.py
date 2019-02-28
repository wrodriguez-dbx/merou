from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grouper.entities.group_request import GroupRequestStatus, UserGroupRequest
    from grouper.repositories.audit_log import AuditLogRepository
    from grouper.usecases.authorization import Authorization


class AuditLogService(object):
    """Updates the audit log when changes are made."""

    def __init__(self, audit_log_repository):
        # type: (AuditLogRepository) -> None
        self.audit_log_repository = audit_log_repository

    def log_disable_permission(self, permission, authorization):
        # type: (str, Authorization) -> None
        self.audit_log_repository.log(
            authorization=authorization,
            action="disable_permission",
            description="Disabled permission",
            on_permission=permission,
        )

    def log_user_group_request_status_change(self, request, status, authorization):
        # type: (UserGroupRequest, GroupRequestStatus, Authorization) -> None
        self.audit_log_repository.log(
            authorization=authorization,
            action="update_request",
            description="Updated request to status: {}".format(status.value),
            on_group=request.group,
            on_user=request.requester,
        )
