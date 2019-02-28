from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import aliased
from sqlalchemy.sql import label

from grouper.entities.group_request import UserGroupRequest
from grouper.models.base.constants import OBJ_TYPES
from grouper.models.comment import Comment
from grouper.models.group import Group
from grouper.models.request import Request
from grouper.models.request_status_change import RequestStatusChange
from grouper.models.user import User

if TYPE_CHECKING:
    from grouper.models.base.session import Session
    from grouper.usecases.authorization import Authorization
    from typing import List


class UnknownUserGroupRequestException(Exception):
    """Request being updated does not exist."""

    def __init__(self, request):
        # type: (UserGroupRequest) -> None
        msg = "Group membership request {} not found".format(request.id)
        super(UnknownUserGroupRequestException, self).__init__(msg)


class UnknownUserException(Exception):
    """User processing a request does not exist."""

    pass


class GroupRequestRepository(object):
    """SQL storage layer for requests to join groups."""

    def __init__(self, session):
        # type: (Session) -> None
        self.session = session

    def cancel_user_request(self, request, authorization):
        # type: (UserGroupRequest, Authorization) -> None
        now = datetime.utcnow()
        request = Request.get(self.session, request.id)
        if not request:
            raise UnknownUserGroupRequestException(request)
        actor = User.get(self.session, name=authorization.actor)
        if not actor:
            raise UnknownUserException("Unknown user {}".format(authorization.actor))

        request_status_change = RequestStatusChange(
            request=request,
            user_id=actor.id,
            from_status=request.status.value,
            to_status="cancelled",
            change_at=now,
        ).add(self.session)
        self.session.flush()

        Comment(
            obj_type=OBJ_TYPES["RequestStatusChange"],
            obj_pk=request_status_change.id,
            user_id=actor.id,
            comment="User converted to service account",
            created_on=now,
        ).add(self.session)

    def pending_requests_for_user(self, user):
        # type: (str) -> List[UserGroupRequest]
        requester = aliased(User)
        on_behalf_of = aliased(User)
        sql_requests = self.session.query(
            Request.id,
            label("requester", requester.username),
            Group.groupname,
            label("on_behalf_of", on_behalf_of.username),
        ).filter(
            Request.on_behalf_obj_type == OBJ_TYPES["User"],
            Request.on_behalf_obj_pk == on_behalf_of.id,
            Request.requester_id == requester.id,
            Request.requesting_id == Group.id,
            Request.status == "pending",
        )

        requests = []
        for sql_request in sql_requests:
            request = UserGroupRequest(
                id=sql_request.id,
                user=sql_request.on_behalf_of,
                group=sql_request.groupname,
                requester=sql_request.requester,
                status=sql_request.status,
            )
            requests.append(request)
        return requests
