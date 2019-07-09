import os
import shutil
from tests.testlibraries.file_path_builder_for_test import FilePathBuilderForTest
from tests.testlibraries.file_path_builder_for_test import FixtureFilePathBuilderForTest


class FixtureFileHandlerForTest:
    FILE_PATH: FilePathBuilderForTest

    @classmethod
    def _restore_target_if_backup_for_test_exist(cls):
        if not cls.FILE_PATH.backup_for_test.is_file():
            return
        if cls.FILE_PATH.target.is_file():
            os.unlink(str(cls.FILE_PATH.target))
        os.replace(str(cls.FILE_PATH.backup_for_test), str(cls.FILE_PATH.target))

    @classmethod
    def _vacate_target_if_exist(cls):
        if cls.FILE_PATH.target.is_file():
            os.replace(str(cls.FILE_PATH.target), str(cls.FILE_PATH.backup_for_test))

    @classmethod
    def _remove_backup_if_exist(cls):
        if cls.FILE_PATH.backup.exists():
            os.unlink(str(cls.FILE_PATH.backup))


class TargetFilePathVacatorForTest(FixtureFileHandlerForTest):
    @classmethod
    def set_up(cls):
        cls._vacate_target_if_exist()
        cls._remove_backup_if_exist()

    @classmethod
    def do_cleanups(cls):
        cls._restore_target_if_backup_for_test_exist()


class FixtureFileDeployerForTest(TargetFilePathVacatorForTest):
    FILE_PATH: FixtureFilePathBuilderForTest
    @classmethod
    def set_up(cls):
        super().set_up()
        shutil.copy(str(cls.FILE_PATH.resource), str(cls.FILE_PATH.target))
