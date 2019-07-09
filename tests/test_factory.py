from pathlib import Path

import pytest

from fixturefilehandler import TargetFilePathVacator, ResourceFileDeployer
from fixturefilehandler.factories import VacatorFactory, DeployerFactory
from fixturefilehandler.file_paths import SimpleDeployFilePath, RelativeDeployFilePath, YamlConfigFilePathBuilder


class TestVacatorFactory:
    @staticmethod
    @pytest.mark.parametrize('file_path', [
        (SimpleDeployFilePath(Path('path_b'), Path('path_c'), Path('path_a'))),
        (RelativeDeployFilePath(Path('path_1'), Path('path_2'), Path('path_3'))),
        (YamlConfigFilePathBuilder()),
    ])
    def test(file_path):
        vacator = VacatorFactory.create(file_path)
        assert issubclass(vacator, TargetFilePathVacator)
        assert vacator.FILE_PATH == file_path


class TestDeployerFactory:
    @staticmethod
    @pytest.mark.parametrize('file_path', [
        (SimpleDeployFilePath(Path('path_b'), Path('path_c'), Path('path_a'))),
        (RelativeDeployFilePath(Path('path_1'), Path('path_2'), Path('path_3'))),
        (YamlConfigFilePathBuilder()),
    ])
    def test(file_path):
        deployer = DeployerFactory.create(file_path)
        assert issubclass(deployer, ResourceFileDeployer)
        assert deployer.FILE_PATH == file_path
