import os
from pathlib import Path


class FilePathBuilderForTest:
    """This class builds file path for config file."""
    def __init__(self, target: Path, backup: Path, backup_for_test: Path, base: Path = Path(os.getcwd())):
        self._target: Path = target
        self._backup: Path = backup
        self._backup_for_test: Path = backup_for_test
        self._base: Path = base

    @property
    def target(self) -> Path:
        """This method return path to target file"""
        return self._base / self._target

    @property
    def backup(self) -> Path:
        """This method return path to backup file"""
        return self._base / self._backup

    @property
    def backup_for_test(self) -> Path:
        """This method return path to backup file for test"""
        return self._base / self._backup_for_test


class FixtureFilePathBuilderForTest(FilePathBuilderForTest):
    def __init__(
            self,
            target: Path,
            backup: Path,
            backup_for_test: Path,
            resource: Path,
            base: Path = Path(os.getcwd()),
            base_resource: Path = Path(os.getcwd()) / 'tests'
    ):
        super().__init__(target, backup, backup_for_test, base)
        self._reource = resource
        self._base_resource = base_resource

    @property
    def resource(self) -> Path:
        """This method return path to resource file"""
        return self._base_resource / self._reource
