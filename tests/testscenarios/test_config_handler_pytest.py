"""Tests for pytest scenario"""
import shutil
from pathlib import Path

import pytest

from tests.testscenarios import CONTENT_IN_PROJECT_TEST_RESOURCE_FILE, PATH_YOUR_PROJECT_HOME, \
    CONTENT_IN_TEST_RESOURCE_FILE, PATH_TEST_RESOURCES_HOME, PATH_PROJECT_HOME, \
    CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED
# noinspection PyUnresolvedReferences
from yourproduct.pytest_context_basic import fixture_file  # noqa: F401
# noinspection PyUnresolvedReferences
from yourproduct.pytest_context_advanced import fixture_file_advanced  # noqa: F401


pytest_plugins = ['pytester']


class TestConfigHandlerPytest:
    """Tests for pytest scenario"""
    @staticmethod
    def test(fixture_file):  # noqa: F811
        """Config file for test should be loaded."""
        assert fixture_file.target.read_text() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE


@pytest.fixture
def directory_testdir(testdir):
    sample_code = (PATH_YOUR_PROJECT_HOME / 'pytest_context_basic.py').read_text()
    print(testdir.makeconftest(
        f"import sys\nsys.path.append(" + rf'{str(PATH_PROJECT_HOME).__repr__()}' + ")\n" + sample_code
    ).read_text(encoding='UTF-8'))
    testdir.makepyfile((Path(__file__).parent.parent / 'testresources/pytest_code_pytest_context.py').read_text())
    shutil.copy(
        str(PATH_YOUR_PROJECT_HOME / 'testresources/test.txt.dist'),
        str(Path(testdir.mkdir('testresources')) / 'test.txt.dist')
    )
    yield testdir


@pytest.fixture
def directory_target_testdir(directory_testdir):
    shutil.copy(str(PATH_TEST_RESOURCES_HOME / 'test.txt.dist'), str(Path(directory_testdir.tmpdir) / 'test.txt'))
    yield directory_testdir


class TestConfigHandlerPytestBeforeAfter:
    @staticmethod
    def test_case_when_target_exist(directory_target_testdir):
        """
        Target file should be test resource before set up.
        Target file should be project test resource between set up and do cleanups.
        Target file should be test resource after do cleanups.
        """
        target = Path(directory_target_testdir.tmpdir) / 'test.txt'
        assert target.read_text() == CONTENT_IN_TEST_RESOURCE_FILE
        result = directory_target_testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)
        assert target.read_text() == CONTENT_IN_TEST_RESOURCE_FILE

    @staticmethod
    def test_case_when_target_not_exist(directory_testdir):
        """
        Target file should not exist before set up.
        Target file should be project test resource between set up and do cleanups.
        Target file should be project test resource after do cleanups.
        """
        target = Path(directory_testdir.tmpdir) / 'test.txt'
        assert not target.exists()
        result = directory_testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)
        assert target.read_text() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE


class TestAdvancedConfigHandlerPytest:
    """Tests for pytest scenario"""
    @staticmethod
    def test_advanced(fixture_file_advanced):  # noqa: F811
        """Config file for test should be loaded."""
        assert fixture_file_advanced.target.read_text() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED
