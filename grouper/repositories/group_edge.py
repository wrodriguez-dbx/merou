from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grouper.graph import GroupGraph
    from grouper.models.base.session import Session
    from typing import List


class GroupEdgeRepository(object):
    """Storage layer for group edges."""

    def __init__(self, graph):
        # type: (GroupGraph) -> None
        self.graph = graph

    def groups_of_user(self, username):
        # type: (str) -> List[str]
        user_details = self.graph.get_user_details(username)
        return [group for group in user_details["groups"]]
