"""This module implements file state dependencies."""
from abc import abstractmethod
from pathlib import Path

from fixturefilehandler.file_paths import RelativeDeployFilePath
from tests.testlibraries.parametrizer.checkers import NotExistChecker, ContentChecker


class FileStateDependency:
    """This class implements abstract file state dependency."""
    @staticmethod
    @abstractmethod
    def create_checker(path: Path):
        """This method returns checker."""
    @staticmethod
    @abstractmethod
    def create_file(file_path: RelativeDeployFilePath):
        """This method returns checker."""
    @classmethod
    def assert_file_state(cls, path: Path):
        """This method checks file state."""
        checker = cls.create_checker(path)
        checker.do_assertion()


class NoExistDependency(FileStateDependency):
    """This class implements abstract file state dependency on case when not exist."""
    @staticmethod
    def create_checker(path: Path):
        return NotExistChecker(path)

    @staticmethod
    def create_file(file_path: RelativeDeployFilePath):
        pass


class ContentExistingDependency(FileStateDependency):
    """This class implements abstract file state dependency on case when existing content."""
    CONTENT = 'Content in existing file'
    @staticmethod
    def create_checker(path: Path):
        return ContentChecker(path, ContentExistingDependency.CONTENT)

    @staticmethod
    def create_file(file_path: RelativeDeployFilePath):
        file_path.target.write_text(ContentExistingDependency.CONTENT)


class ContentBackupDependency(FileStateDependency):
    """This class implements abstract file state dependency on case when backup content."""
    CONTENT = 'Content in backup file'
    @staticmethod
    def create_checker(path: Path):
        return ContentChecker(path, ContentBackupDependency.CONTENT)

    @staticmethod
    def create_file(file_path: RelativeDeployFilePath):
        file_path.backup.write_text(ContentBackupDependency.CONTENT)


class ContentResourceDependency(FileStateDependency):
    """This class implements abstract file state dependency on case when resource content."""
    CONTENT = 'Content in resource file'
    @staticmethod
    def create_checker(path: Path):
        return ContentChecker(path, ContentResourceDependency.CONTENT)

    @staticmethod
    def create_file(file_path: RelativeDeployFilePath):
        file_path.resource.write_text(ContentResourceDependency.CONTENT)
