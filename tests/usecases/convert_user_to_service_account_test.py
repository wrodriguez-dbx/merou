from typing import TYPE_CHECKING

from mock import call, MagicMock

from grouper.constants import USER_ADMIN
from grouper.models.user import User

if TYPE_CHECKING:
    from tests.setup import SetupTest


def test_success(setup):
    # type: (SetupTest) -> None
    setup.grant_permission_to_group(USER_ADMIN, "", "admins")
    setup.add_user_to_group("gary@a.co", "admins")
    setup.create_user("service@a.co")
    setup.create_group("some-group")
    setup.commit()
    mock_ui = MagicMock()
    usecase = setup.usecase_factory.create_convert_user_to_service_account_usecase(
        "gary@a.co", mock_ui
    )
    usecase.convert_user_to_service_account("service@a.co", "some-group")
    assert mock_ui.mock_calls == [
        call.converted_user_to_service_account("service@a.co", "some-group")
    ]
    service_account_user = User.get(setup.session, name="service@a.co")
    assert service_account_user
    assert service_account_user.is_service_account
    assert service_account_user.service_account.owner.groupname == "some-group"
