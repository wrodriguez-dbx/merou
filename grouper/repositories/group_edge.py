from typing import TYPE_CHECKING

from grouper.group_member import persist_group_member_changes
from grouper.models.base.constants import OBJ_TYPES
from grouper.models.group import Group
from grouper.models.group_edge import GroupEdge, GROUP_EDGE_ROLES
from grouper.models.user import User
from grouper.repositories.interfaces import GroupEdgeRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from typing import List

class UnknownGroupException(Exception):
    """Group involved in a logged action does not exist."""
    pass

class UnknownUserException(Exception):
    """User involved in a logged action does not exist."""
    pass

class GraphGroupEdgeRepository(GroupEdgeRepository):
    """Graph-aware storage layer for group edges.group

    WARNING: This repository should only be used from other repositories. At higher levels -- the
    service layer, the use case layer, and the UI layer -- the abstraction should be that there
    are users and groups, and group edges (membership) is a relationship between those. Thus a
    service needing to act on the group edges corresponding to a user would call into the user
    repository (which would in turn call into this repository), and equivalently for a group.
    """

    def __init__(self, graph, repository):
        # type: (GroupGraph, GroupEdgeRepository) -> None
        self.graph = graph
        self.repository = repository

    def add_user_to_group(self, username, groupname, role):
        # type: (str, str, str) -> None
        return self.repository.add_user_to_group(username, groupname, role)

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        user_details = self.graph.get_user_details(username)
        return [group["name"] for group in user_details["groups"]]


class SQLGroupEdgeRepository(GroupEdgeRepository):
    """SQL storage layer for group edges.group

    WARNING: This repository should only be used from other repositories. At higher levels -- the
    service layer, the use case layer, and the UI layer -- the abstraction should be that there
    are users and groups, and group edges (membership) are a relationship between those. Thus a
    service needing to act on the group edges corresponding to a user would call into the user
    repository (which would in turn call into this repository), and equivalently for a group.
    """

    def __init__(self, session):
        # type: (Session) -> None
        self.session = session

    def add_user_to_group(self, username, groupname, role):
        # type: (str, str, str) -> None
        group_id = self._id_for_group(groupname)
        member_type = OBJ_TYPES["User"]
        member_id = self._id_for_user(username)
        role_index = GROUP_EDGE_ROLES.index(role)

        edge = GroupEdge(
            group_id=group_id,
            member_type=member_type,
            member_pk=member_id,
            expiration=None,
            active=True,
            _role=role_index,
        )
        edge.add(self.session)

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        raise NotImplementedError()

    def _id_for_group(self, groupname):
        # type: (str) -> int
        group_obj = Group.get(self.session, name=groupname)
        if not group_obj:
            raise UnknownGroupException("unknown group {}".format(groupname))
        return group_obj.id

    def _id_for_user(self, username):
        # type: (str) -> int
        user_obj = User.get(self.session, name=username)
        if not user_obj:
            raise UnknownUserException("unknown user {}".format(username))
        return user_obj.id