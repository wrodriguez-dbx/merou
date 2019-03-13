"""Utilities to set up test cases.

Provides a SetupTest object that creates the database session, provides use case factories for
individual tests, and provides methods to create objects in the test database.  These methods try
to minimize the amount of code required to set up a test by creating new objects whenever needed.
So, for instance, one can just call:

    setup.add_user_to_group("user@a.co", "some-group")

without creating the user and group first, and both will be created if not present.

This is the new test setup mechanism, replacing the fixtures defined in tests.fixtures.  All new
tests should use this mechanism and not rely on standard_graph or other pytest fixtures.
"""

import os
from datetime import datetime
from time import time
from typing import TYPE_CHECKING

from grouper.graph import GroupGraph
from grouper.models.base.constants import OBJ_TYPES
from grouper.models.base.model_base import Model
from grouper.models.base.session import get_db_engine, Session
from grouper.models.counter import Counter
from grouper.models.group import Group
from grouper.models.group_edge import GROUP_EDGE_ROLES, GroupEdge
from grouper.models.permission import Permission
from grouper.models.permission_map import PermissionMap
from grouper.models.user import User
from grouper.repositories.factory import RepositoryFactory
from grouper.services.factory import ServiceFactory
from grouper.usecases.factory import UseCaseFactory
from tests.path_util import db_url

if TYPE_CHECKING:
    from py.local import LocalPath
    from typing import Optional


class SetupTest(object):
    """Set up the environment for a test.

    Attributes:
        graph: Underlying graph (not refreshed from the database automatically!)
        repository_factory: Factory for repository objects
        session: The underlying database session
        service_factory: Factory for service objects
        usecase_factory: Factory for usecase objects
    """

    def __init__(self, tmpdir):
        # type: (LocalPath) -> None
        self.session = self.create_session(tmpdir)
        self.graph = GroupGraph()
        self.repository_factory = RepositoryFactory(self.session, self.graph)
        self.service_factory = ServiceFactory(self.repository_factory)
        self.usecase_factory = UseCaseFactory(self.service_factory)

    def create_session(self, tmpdir):
        # type: (LocalPath) -> Session
        db_engine = get_db_engine(db_url(tmpdir))

        # If using a persistent database, clear the database first.
        if "MEROU_TEST_DATABASE" in os.environ:
            Model.metadata.drop_all(db_engine)

        # Create the database schema and the corresponding session.
        Model.metadata.create_all(db_engine)
        Session.configure(bind=db_engine)
        return Session()

    def commit(self):
        # type: () -> None
        Counter.incr(self.session, "updates")
        self.session.commit()
        self.graph.update_from_db(self.session)

    def close(self):
        # type: () -> None
        self.session.close()

    def create_group(self, name):
        # type: (str) -> None
        """Create a group, does nothing if it already exists."""
        if Group.get(self.session, name=name):
            return
        group = Group(groupname=name)
        group.add(self.session)

    def create_permission(
        self, name, description="", audited=False, enabled=True, created_on=None
    ):
        # type: (str, str, bool, bool, Optional[datetime]) -> None
        """Create a permission, does nothing if it already exists.

        Avoid milliseconds in the creation timestamp since they behave differently in SQLite (which
        preserves them) and MySQL (which drops them).
        """
        if Permission.get(self.session, name=name):
            return
        if not created_on:
            created_on = datetime.utcfromtimestamp(int(time()))
        permission = Permission(
            name=name,
            description=description,
            _audited=audited,
            enabled=enabled,
            created_on=created_on,
        )
        permission.add(self.session)

    def create_user(self, name):
        # type: (str) -> None
        """Create a user, does nothing if it already exists."""
        if User.get(self.session, name=name):
            return
        user = User(username=name)
        user.add(self.session)

    def add_user_to_group(self, user, group, role="member"):
        # type: (str, str, str) -> None
        self.create_user(user)
        self.create_group(group)
        user_obj = User.get(self.session, name=user)
        assert user_obj
        group_obj = Group.get(self.session, name=group)
        assert group_obj
        edge = GroupEdge(
            group_id=group_obj.id,
            member_type=OBJ_TYPES["User"],
            member_pk=user_obj.id,
            active=True,
            _role=GROUP_EDGE_ROLES.index(role),
        )
        edge.add(self.session)

    def grant_permission_to_group(self, permission, argument, group):
        # type: (str, str, str) -> None
        self.create_group(group)
        self.create_permission(permission)
        permission_obj = Permission.get(self.session, name=permission)
        assert permission_obj
        group_obj = Group.get(self.session, name=group)
        assert group_obj
        grant = PermissionMap(
            permission_id=permission_obj.id, group_id=group_obj.id, argument=argument
        )
        grant.add(self.session)

    def create_group_request(self, user, group, role="member"):
        # type: (str, str, str) -> None
        self.create_user(user)
        self.create_group(group)

        user_obj = User.get(self.session, name=user)
        assert user_obj
        group_obj = Group.get(self.session, name=group)
        assert group_obj

        # Note: despite the function name, this only creates the request. The flow here is
        # convoluted enough that it seems best to preserve exact behavior for testing.
        group_obj.add_member(
            requester=user_obj, user_or_group=user_obj, reason="", status="pending", role=role
        )
