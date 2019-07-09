from tests.testscenarios import CONTENT_IN_PROJECT_TEST_RESOURCE_FILE


def test_something(fixture_file):
    with fixture_file.target.open('r') as file_target:
        assert file_target.read() == CONTENT_IN_PROJECT_TEST_RESOURCE_FILE
