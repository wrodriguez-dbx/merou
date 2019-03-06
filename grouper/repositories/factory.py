from typing import TYPE_CHECKING

from grouper.repositories.audit_log import AuditLogRepository
from grouper.repositories.checkpoint import CheckpointRepository
from grouper.repositories.group_edge import GraphGroupEdgeRepository, SQLGroupEdgeRepository
from grouper.repositories.group_request import GroupRequestRepository
from grouper.repositories.permission import GraphPermissionRepository, SQLPermissionRepository
from grouper.repositories.permission_grant import GraphPermissionGrantRepository
from grouper.repositories.service_account import (
    GraphServiceAccountRepository,
    SQLServiceAccountRepository,
)
from grouper.repositories.transaction import TransactionRepository
from grouper.repositories.user import GraphUserRepository, SQLUserRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from grouper.repositories.interfaces import (
        PermissionRepository,
        PermissionGrantRepository,
        ServiceAccountRepository,
        UserRepository,
    )


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

    def create_group_edge_repository(self):
        sql_group_edge_repository = SQLGroupEdgeRepository(self.session)
        return GraphGroupEdgeRepository(self.graph, sql_group_edge_repository)

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

    def create_service_account_repository(self):
        # type: () -> ServiceAccountRepository
        sql_group_edge_repository = SQLGroupEdgeRepository(self.session)
        group_edge_repository = GraphGroupEdgeRepository(self.graph, sql_group_edge_repository)

        sql_user_repository = SQLUserRepository(self.session)
        user_repository = GraphUserRepository(
            self.graph,
            sql_user_repository,
            group_edge_repository)
        
        sql_service_account_repository = SQLServiceAccountRepository(self.session, user_repository)
        return GraphServiceAccountRepository(self.graph, sql_service_account_repository)

    def create_transaction_repository(self):
        # type: () -> TransactionRepository
        return TransactionRepository(self.session)

    def create_user_repository(self):
        # type: () -> UserRepository
        sql_user_repository = SQLUserRepository(self.session)
        sql_group_edge_repository = SQLGroupEdgeRepository(self.session)
        group_edge_repository = GraphGroupEdgeRepository(self.graph, sql_group_edge_repository)
        return GraphUserRepository(self.graph, sql_user_repository, group_edge_repository)
