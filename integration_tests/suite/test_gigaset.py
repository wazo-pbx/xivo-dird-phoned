# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to

from .helpers.base import (
    BasePhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    VALID_XIVO_USER_UUID,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

VENDOR = 'gigaset'


class TestGigaset(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Menu - There is no menu for gigaset

    def test_that_menu_return_error_when_query_ssl(self):
        response = self.get_ssl_menu_result(
            vendor=VENDOR, xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_menu_return_error_when_query(self):
        response = self.get_menu_result(
            vendor=VENDOR, xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    # Input - there is no input for gigaset

    def test_that_input_return_error_when_query_ssl(self):
        response = self.get_ssl_input_result(
            vendor=VENDOR, xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_input_return_error_when_query(self):
        response = self.get_input_result(
            vendor=VENDOR, xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    # Lookup

    def test_that_lookup_return_no_error_when_query_ssl(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=VALID_XIVO_USER_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_no_error_when_query(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=VALID_XIVO_USER_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_no_error_when_no_term(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(200))


class TestAuthError(BasePhonedIntegrationTest):

    asset = 'no_auth_server'

    def test_no_auth_server_gives_503(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(503))


class TestDirdError(BasePhonedIntegrationTest):

    asset = 'no_dird_server'

    def test_no_dird_server_gives_503(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=VALID_XIVO_USER_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(503))
