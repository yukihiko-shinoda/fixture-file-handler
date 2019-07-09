from contextlib import contextmanager
from pathlib import Path

import pytest

from fixturefilehandler import FixtureFileHandler, TargetFilePathVacator, ResourceFileDeployer
from fixturefilehandler.exceptions import BackupAlreadyExistError
from fixturefilehandler.file_paths import RelativeVacateFilePath, RelativeDeployFilePath
PATH_TARGET = Path('test.txt')
PATH_BACKUP = Path('test.txt.bak')
PATH_RESOURCE = Path('test.txt.dist')
CONTENT_EXISTING = 'Content in existing file'
CONTENT_BACKUP = 'Content in backup file'
CONTENT_RESOURCE = 'Content in resource file'


@pytest.fixture
def deploy_file_path(tmp_path):
    yield RelativeDeployFilePath(PATH_TARGET, PATH_BACKUP, PATH_RESOURCE, tmp_path)


@pytest.fixture
def vacator(tmp_path):
    class Vacator(TargetFilePathVacator):
        FILE_PATH = RelativeVacateFilePath(PATH_TARGET, PATH_BACKUP, tmp_path)
    yield Vacator


@pytest.fixture
def deployer(tmp_path):
    class Deployer(ResourceFileDeployer):
        FILE_PATH = RelativeDeployFilePath(PATH_TARGET, PATH_BACKUP, PATH_RESOURCE, tmp_path)
    yield Deployer


@pytest.fixture
def deploy_file_path_two_files_exist(deploy_file_path):
    yield prepare_two_file(deploy_file_path)


@pytest.fixture
def deploy_file_path_target_not_exist(deploy_file_path):
    deploy_file_path.backup.write_text(CONTENT_BACKUP)
    return deploy_file_path


@pytest.fixture
def deploy_file_path_backup_not_exist(deploy_file_path):
    yield prepare_target_file(deploy_file_path)


@pytest.fixture
def vacator_two_files_exist(vacator):
    prepare_two_file(vacator.FILE_PATH)
    yield vacator


@pytest.fixture
def deployer_resource_only(deployer):
    file_path = deployer.FILE_PATH
    file_path.resource.write_text(CONTENT_RESOURCE)
    yield deployer


@pytest.fixture
def vacator_existing_only(vacator):
    prepare_target_file(vacator.FILE_PATH)
    yield vacator


@pytest.fixture
def deployer_three_files_exist(deployer):
    file_path = deployer.FILE_PATH
    file_path.target.write_text(CONTENT_EXISTING)
    file_path.backup.write_text(CONTENT_BACKUP)
    file_path.resource.write_text(CONTENT_RESOURCE)
    yield deployer


@pytest.fixture
def deployer_resource_and_existing(deployer):
    file_path = deployer.FILE_PATH
    file_path.target.write_text(CONTENT_EXISTING)
    file_path.resource.write_text(CONTENT_RESOURCE)
    yield deployer


def prepare_target_file(file_path: RelativeVacateFilePath):
    file_path.target.write_text(CONTENT_EXISTING)
    return file_path


def prepare_two_file(file_path: RelativeVacateFilePath):
    file_path.target.write_text(CONTENT_EXISTING)
    file_path.backup.write_text(CONTENT_BACKUP)
    return file_path


@contextmanager
def context_vacate_existing_only(file_path):
    assert file_path.target.read_text() == CONTENT_EXISTING
    assert not file_path.backup.exists()
    yield
    assert not file_path.target.exists()
    assert file_path.backup.read_text() == CONTENT_EXISTING


@contextmanager
def context_restore_two_files_exist(file_path):
    assert file_path.target.read_text() == CONTENT_EXISTING
    assert file_path.backup.read_text() == CONTENT_BACKUP
    yield
    assert file_path.target.read_text() == CONTENT_BACKUP
    assert not file_path.backup.exists()


class TestFixtureFileHandler:
    @staticmethod
    def test_vacate_target_if_exist_exist(deploy_file_path_backup_not_exist):
        with context_vacate_existing_only(deploy_file_path_backup_not_exist):
            FixtureFileHandler.vacate_target_if_exist(deploy_file_path_backup_not_exist)

    @staticmethod
    def test_vacate_target_if_exist_not_exist(deploy_file_path):
        file_path = deploy_file_path
        assert not file_path.target.exists()
        assert not file_path.backup.exists()
        FixtureFileHandler.vacate_target_if_exist(file_path)
        assert not file_path.target.exists()
        assert not file_path.backup.exists()

    @staticmethod
    def test_vacate_target_if_exist_backup_already_exist(deploy_file_path_target_not_exist):
        file_path = deploy_file_path_target_not_exist
        assert not file_path.target.exists()
        assert file_path.backup.read_text() == CONTENT_BACKUP
        with pytest.raises(BackupAlreadyExistError):
            FixtureFileHandler.vacate_target_if_exist(file_path)
        assert not file_path.target.exists()
        assert file_path.backup.read_text() == CONTENT_BACKUP

    @staticmethod
    def test_setup_target_exist(deployer_resource_and_existing):
        file_path = deployer_resource_and_existing.FILE_PATH
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert not file_path.backup.exists()
        assert file_path.resource.read_text() == CONTENT_RESOURCE
        FixtureFileHandler.deploy_resource(file_path)
        assert file_path.target.read_text() == CONTENT_RESOURCE
        assert file_path.backup.read_text() == CONTENT_EXISTING
        assert file_path.resource.read_text() == CONTENT_RESOURCE

    @staticmethod
    def test_setup_target_not_exist(deployer_resource_only):
        file_path = deployer_resource_only.FILE_PATH
        assert not file_path.target.exists()
        assert not file_path.backup.exists()
        assert file_path.resource.read_text() == CONTENT_RESOURCE
        FixtureFileHandler.deploy_resource(file_path)
        assert file_path.target.read_text() == CONTENT_RESOURCE
        assert not file_path.backup.exists()
        assert file_path.resource.read_text() == CONTENT_RESOURCE

    @staticmethod
    def test_setup_fixture_not_exist(deployer):
        file_path = deployer.FILE_PATH
        assert not file_path.resource.exists()
        assert not file_path.target.exists()
        assert not file_path.backup.exists()
        with pytest.raises(FileNotFoundError):
            FixtureFileHandler.deploy_resource(file_path)
        assert not file_path.resource.exists()
        assert not file_path.target.exists()
        assert not file_path.backup.exists()

    @staticmethod
    def test_restore_backup_if_exist_exist(deploy_file_path_two_files_exist):
        with context_restore_two_files_exist(deploy_file_path_two_files_exist):
            FixtureFileHandler.restore_backup_if_exist(deploy_file_path_two_files_exist)

    @staticmethod
    def test_restore_backup_if_exist_not_exist(deploy_file_path_backup_not_exist):
        file_path = deploy_file_path_backup_not_exist
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert not file_path.backup.exists()
        FixtureFileHandler.restore_backup_if_exist(file_path)
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert not file_path.backup.exists()


class TestTargetFilePathVacator:
    @staticmethod
    def test_setup(vacator_existing_only):
        with context_vacate_existing_only(vacator_existing_only.FILE_PATH):
            vacator_existing_only.setup()

    @staticmethod
    def test_setup_with_argument(vacator_existing_only):
        file_path = vacator_existing_only.FILE_PATH
        with context_vacate_existing_only(file_path):
            TargetFilePathVacator.setup(file_path)

    @staticmethod
    def test_teardown(vacator_two_files_exist):
        with context_restore_two_files_exist(vacator_two_files_exist.FILE_PATH):
            vacator_two_files_exist.teardown()

    @staticmethod
    def test_teardown_with_argument(vacator_two_files_exist):
        file_path = vacator_two_files_exist.FILE_PATH
        with context_restore_two_files_exist(file_path):
            TargetFilePathVacator.teardown(file_path)


class TestResourceFileDeployer:
    @staticmethod
    @contextmanager
    def context_existing_only(deployer_resource_and_existing):
        file_path = deployer_resource_and_existing.FILE_PATH
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert not file_path.backup.exists()
        assert file_path.resource.read_text() == CONTENT_RESOURCE
        yield
        assert file_path.target.read_text() == CONTENT_RESOURCE
        assert file_path.backup.read_text() == CONTENT_EXISTING
        assert file_path.resource.read_text() == CONTENT_RESOURCE

    @staticmethod
    def test_setup(deployer_resource_and_existing):
        with TestResourceFileDeployer.context_existing_only(deployer_resource_and_existing):
            deployer_resource_and_existing.setup()

    @staticmethod
    def test_setup_with_argument(deployer_resource_and_existing):
        with TestResourceFileDeployer.context_existing_only(deployer_resource_and_existing):
            ResourceFileDeployer.setup(deployer_resource_and_existing.FILE_PATH)

    @staticmethod
    def test_integration_teardown_exist(deployer_three_files_exist):
        file_path = deployer_three_files_exist.FILE_PATH
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert file_path.backup.read_text() == CONTENT_BACKUP
        deployer_three_files_exist.teardown()
        assert file_path.target.read_text() == CONTENT_BACKUP
        assert not file_path.backup.exists()

    @staticmethod
    def test_integration_teardown_not_exist(deployer_resource_and_existing):
        file_path = deployer_resource_and_existing.FILE_PATH
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert not file_path.backup.exists()
        assert file_path.resource.read_text() == CONTENT_RESOURCE
        deployer_resource_and_existing.teardown()
        assert file_path.target.read_text() == CONTENT_EXISTING
        assert not file_path.backup.exists()
        assert file_path.resource.read_text() == CONTENT_RESOURCE
