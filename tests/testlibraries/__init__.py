from tests.testlibraries.file_path_builder_for_test import FilePathBuilderForTest, FixtureFilePathBuilderForTest
from tests.testlibraries.fixture_file_handler_for_test import TargetFilePathVacatorForTest, FixtureFileDeployerForTest


def file_path_empty_for_test(file_path: FilePathBuilderForTest):
    class Vacator(TargetFilePathVacatorForTest):
        FILE_PATH = file_path

    Vacator.set_up()
    yield
    Vacator.do_cleanups()


def fixture_file_for_test(file_path: FixtureFilePathBuilderForTest):
    class Deployer(FixtureFileDeployerForTest):
        FILE_PATH = file_path

    Deployer.set_up()
    yield
    Deployer.do_cleanups()
