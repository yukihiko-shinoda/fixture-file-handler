"""This module implements constant for scenario test."""
from pathlib import Path

from tests.testlibraries.file_path_builder_for_test import FixtureFilePathBuilderForTest, FilePathBuilderForTest

PATH_PROJECT_HOME = Path(__file__).parent.parent.parent
PATH_YOUR_PROJECT_HOME = Path(__file__).parent.parent.parent / 'yourproduct'
PATH_TEST_RESOURCES_HOME = Path(__file__).parent.parent / 'testresources'
CONTENT_IN_PROJECT_TEST_RESOURCE_FILE = 'content in project test resource file'
CONTENT_IN_PROJECT_TEST_RESOURCE_FILE_FOR_ADVANCED = 'content in project test resources for advanced'
CONTENT_IN_TEST_RESOURCE_FILE = 'content in test resource file'
RESOURCE_FILE_PATH = FixtureFilePathBuilderForTest(
    target=Path('test.txt'),
    backup=Path('test.txt.bak'),
    backup_for_test=Path('test.txt.test.bak'),
    resource=Path('test.txt.dist'),
    base=PATH_YOUR_PROJECT_HOME,
    base_resource=PATH_TEST_RESOURCES_HOME
)
FILE_PATH = FilePathBuilderForTest(
    target=Path('test.txt'),
    backup=Path('test.txt.bak'),
    backup_for_test=Path('test.txt.test.bak'),
    base=PATH_YOUR_PROJECT_HOME
)
