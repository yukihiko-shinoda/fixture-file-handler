"""Tests for unittest scenario"""
import pytest

from tests.testlibraries import fixture_file_for_test, file_path_empty_for_test
from tests.testscenarios import RESOURCE_FILE_PATH, FILE_PATH, CONTENT_IN_TEST_RESOURCE_FILE, \
    CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED
from yourproduct.unittest_context_advanced import AdvancedConfigurableTestCase
from yourproduct.unittest_context_basic import ConfigurableTestCase


class TestConfigHandlerUnittest(ConfigurableTestCase):
    """Tests for unittest scenario"""
    @staticmethod
    def test():
        """Config file for test should be loaded."""
        assert not RESOURCE_FILE_PATH.target.exists()


@pytest.fixture
def target_file():
    yield from fixture_file_for_test(RESOURCE_FILE_PATH)


@pytest.fixture
def target_file_empty():
    yield from file_path_empty_for_test(FILE_PATH)


class TestConfigHandlerUnittestBeforeAfter:
    # pylint: disable=unused-argument
    def test_case_when_target_exist(self, target_file):
        """
        Target file should be test resource before set up.
        Target file should not exist between set up and do cleanups.
        Target file should be test resource after do cleanups.
        """
        assert RESOURCE_FILE_PATH.target.read_text() == CONTENT_IN_TEST_RESOURCE_FILE
        self._set_up_by_unittest()
        assert not RESOURCE_FILE_PATH.target.exists()
        self._do_cleanups_by_unittest()
        assert RESOURCE_FILE_PATH.target.read_text() == CONTENT_IN_TEST_RESOURCE_FILE

    # pylint: disable=unused-argument
    def test_case_when_target_not_exist(self, target_file_empty):
        """
        Target file should not exist anytime.
        """
        assert not FILE_PATH.target.exists()
        self._set_up_by_unittest()
        assert not FILE_PATH.target.exists()
        self._do_cleanups_by_unittest()
        assert not FILE_PATH.target.exists()

    @staticmethod
    def _set_up_by_unittest():
        ConfigurableTestCase(methodName='setUp').setUp()

    @staticmethod
    def _do_cleanups_by_unittest():
        ConfigurableTestCase(methodName='doCleanups').doCleanups()


class TestAdvancedConfigHandlerUnittest(AdvancedConfigurableTestCase):
    """Tests for unittest scenario"""
    @staticmethod
    def test_advanced():
        """Config file for test should be loaded."""
        assert RESOURCE_FILE_PATH.target.read_text() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED
