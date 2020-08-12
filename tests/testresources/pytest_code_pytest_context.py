"""This module is run in test_dir on pytest for test pytest.fixture."""
from tests.testscenarios import CONTENT_IN_PROJECT_TEST_RESOURCE_FILE


def test_something(fixture_file):
    """This test is run in test_dir on pytest for test pytest.fixture."""
    with fixture_file.target.open("r") as file_target:
        assert file_target.read() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE
