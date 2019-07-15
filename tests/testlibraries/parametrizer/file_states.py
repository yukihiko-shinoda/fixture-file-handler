"""This module implements """
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Type, Generic

from fixturefilehandler import VacateFilePathInterface, DeployFilePathInterface
from tests.testlibraries.parametrizer import TypeVarVacateFilePathInterface
from tests.testlibraries.parametrizer.file_state_dependency_factories import FileStateDependency, \
    NoExistDependency, ContentExistingDependency, ContentBackupDependency, \
    ContentResourceDependency


class FileState(Enum):
    """This class implements kinds of file state."""
    NOT_EXIST: Type[FileStateDependency] = NoExistDependency
    EXISTING: Type[FileStateDependency] = ContentExistingDependency
    BACKUP: Type[FileStateDependency] = ContentBackupDependency
    RESOURCE: Type[FileStateDependency] = ContentResourceDependency

    def assert_file_state(self, path):
        """This method checks file state."""
        self.value.assert_file_state(path)

    def create_file(self, path):
        """This method creates file."""
        self.value.create_file(path)

    @property
    def value(self) -> Type[FileStateDependency]:
        return super().value


class MultipleFileState(Generic[TypeVarVacateFilePathInterface]):
    """This class implements abstract multiple file state."""
    @abstractmethod
    def assert_state(self, file_path: TypeVarVacateFilePathInterface):
        """This method checks file state."""


@dataclass
class TwoFilesState(MultipleFileState):
    """This class implements states of two files."""
    expect_target: FileState
    expect_backup: FileState

    def assert_state(self, file_path: VacateFilePathInterface):
        self.expect_target.assert_file_state(file_path.target)
        self.expect_backup.assert_file_state(file_path.backup)


@dataclass
class ThreeFilesState(MultipleFileState):
    """This class implements states of three files."""
    expect_target: FileState
    expect_backup: FileState
    expect_resource: FileState

    def assert_state(self, file_path: DeployFilePathInterface):
        self.expect_target.assert_file_state(file_path.target)
        self.expect_backup.assert_file_state(file_path.backup)
        self.expect_resource.assert_file_state(file_path.resource)
