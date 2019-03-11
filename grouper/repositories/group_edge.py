from typing import TYPE_CHECKING

from grouper.repositories.interfaces import GroupEdgeRepository

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from typing import List


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
        raise NotImplementedError()

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        user_details = self.graph.get_user_details(username)
        return [group for group in user_details["groups"]]


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
        raise NotImplementedError()

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        raise NotImplementedError()
