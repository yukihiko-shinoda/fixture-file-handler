"""This module implements factory for file path with file."""
from abc import abstractmethod
from pathlib import Path
from typing import TypeVar, Generic, Type

from fixturefilehandler.file_paths import RelativeVacateFilePath, RelativeDeployFilePath
from tests.testlibraries.parametrizer.file_states import TwoFilesState, ThreeFilesState, MultipleFileState

PATH_TARGET = Path('test.txt')
PATH_BACKUP = Path('test.txt.bak')
PATH_RESOURCE = Path('test.txt.dist')
TypeVarTwoFilesState = TypeVar('TypeVarTwoFilesState', bound=TwoFilesState)


class AbstractFilePathWithFileFactory(Generic[TypeVarTwoFilesState]):
    """This class implements abstract factory."""
    @staticmethod
    @abstractmethod
    def create(tmp_path, file_state: TypeVarTwoFilesState):
        """This class creates files and returns file path"""


class VacateFilePathWithFileFactory(AbstractFilePathWithFileFactory):
    """This class implements factory for vacate file path."""
    @staticmethod
    def create(tmp_path, file_state: TwoFilesState):
        file_path = RelativeVacateFilePath(PATH_TARGET, PATH_BACKUP, tmp_path)
        file_state.expect_target.create_file(file_path)
        file_state.expect_backup.create_file(file_path)
        return file_path


class DeployFilePathWithFileFactory(AbstractFilePathWithFileFactory):
    """This class implements factory for deploy file path."""
    @staticmethod
    def create(tmp_path, file_state: ThreeFilesState):
        file_path = RelativeDeployFilePath(PATH_TARGET, PATH_BACKUP, PATH_RESOURCE, tmp_path)
        file_state.expect_target.create_file(file_path)
        file_state.expect_backup.create_file(file_path)
        file_state.expect_resource.create_file(file_path)
        return file_path


class FilePathWithFileFactory:
    """This class implements factory for file path and file."""
    @staticmethod
    def create(tmp_path, multi_file_state):
        """This class creates files and returns file path"""
        factory = FilePathWithFileFactory._create(multi_file_state)
        return factory.create(tmp_path, multi_file_state)

    @staticmethod
    def _create(multi_file_state: MultipleFileState) -> Type[AbstractFilePathWithFileFactory]:
        if isinstance(multi_file_state, TwoFilesState):
            return VacateFilePathWithFileFactory
        if isinstance(multi_file_state, ThreeFilesState):
            return DeployFilePathWithFileFactory
        raise ValueError()
