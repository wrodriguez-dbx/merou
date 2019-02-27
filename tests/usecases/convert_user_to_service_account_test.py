from typing import TYPE_CHECKING

from mock import MagicMock

from grouper.constants import USER_ADMIN

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
    assert is_service_account("service@a.co")
    assert is_service_account_owned_by("service@a.co", "some-group")
