from typing import TYPE_CHECKING

from grouper.repositories.audit_log import AuditLogRepository
from grouper.repositories.checkpoint import CheckpointRepository
from grouper.repositories.group_request import GroupRequestRepository
from grouper.repositories.permission import GraphPermissionRepository, SQLPermissionRepository
from grouper.repositories.permission_grant import GraphPermissionGrantRepository
from grouper.repositories.transaction import TransactionRepository
from grouper.repositories.user import UserRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from grouper.repositories.interfaces import PermissionRepository, PermissionGrantRepository


class RepositoryFactory(object):
    """Create repositories, which abstract storage away from the database layer."""

    def __init__(self, session, graph):
        # type: (Session, GroupGraph) -> None
        self.session = session
        self.graph = graph

    def create_audit_log_repository(self):
        # type: () -> AuditLogRepository
        return AuditLogRepository(self.session)

    def create_checkpoint_repository(self):
        # type: () -> CheckpointRepository
        return CheckpointRepository(self.session)

    def create_group_request_repository(self):
        # type: () -> GroupRequestRepository
        return GroupRequestRepository(self.session)

    def create_permission_repository(self):
        # type: () -> PermissionRepository
        sql_permission_repository = SQLPermissionRepository(self.session)
        return GraphPermissionRepository(self.graph, sql_permission_repository)

    def create_permission_grant_repository(self):
        # type: () -> PermissionGrantRepository
        return GraphPermissionGrantRepository(self.graph)

    def create_transaction_repository(self):
        # type: () -> TransactionRepository
        return TransactionRepository(self.session)

    def create_user_repository(self):
        # type: () -> UserRepository
        return UserRepository(self.session)
