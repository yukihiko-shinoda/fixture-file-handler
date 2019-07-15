"""Tests for factories module."""
from pathlib import Path
import pytest

from fixturefilehandler import TargetFilePathVacator, ResourceFileDeployer
from fixturefilehandler.factories import VacatorFactory, DeployerFactory
from fixturefilehandler.file_paths import SimpleDeployFilePath, RelativeDeployFilePath, YamlConfigFilePathBuilder


class TestVacatorFactory:
    """Tests for VacatorFactory."""
    @staticmethod
    @pytest.mark.parametrize('file_path', [
        (SimpleDeployFilePath(Path('path_b'), Path('path_c'), Path('path_a'))),
        (RelativeDeployFilePath(Path('path_1'), Path('path_2'), Path('path_3'))),
        (YamlConfigFilePathBuilder()),
    ])
    def test(file_path):
        """
        Factory creates vacator instance.
        Created handler has same file_path with argument.
        """
        vacator = VacatorFactory.create(file_path)
        assert issubclass(vacator, TargetFilePathVacator)
        assert vacator.FILE_PATH == file_path


class TestDeployerFactory:
    """Tests for DeployerFactory."""
    @staticmethod
    @pytest.mark.parametrize('file_path', [
        (SimpleDeployFilePath(Path('path_b'), Path('path_c'), Path('path_a'))),
        (RelativeDeployFilePath(Path('path_1'), Path('path_2'), Path('path_3'))),
        (YamlConfigFilePathBuilder()),
    ])
    def test(file_path):
        """
        Factory creates deployer instance.
        Created handler has same file_path with argument.
        """
        deployer = DeployerFactory.create(file_path)
        assert issubclass(deployer, ResourceFileDeployer)
        assert deployer.FILE_PATH == file_path
