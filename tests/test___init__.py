"""Tests for fixturefilehandler.__init__ module."""

import pytest

from fixturefilehandler.file_paths import VacateFilePathInterface
from tests.testlibraries.parametrizer.action_executors import Action as Act
from tests.testlibraries.parametrizer.file_path_with_fire_factories import FilePathWithFileFactory
from tests.testlibraries.parametrizer.file_states import FileState as Stt
from tests.testlibraries.parametrizer.file_states import MultipleFileState
from tests.testlibraries.parametrizer.file_states import TwoFilesState as TwS
from tests.testlibraries.parametrizer.file_states import ThreeFilesState as ThS

# pylint: disable=line-too-long,bad-whitespace
PARAMS = [
    # TestFixtureFileHandler
    # test_vacate_target_if_exist
    (TwS(Stt.EXISTING,  Stt.NOT_EXIST),                 Act.VACATE_TARGET_IF_EXIST,                 TwS(Stt.NOT_EXIST,  Stt.EXISTING)),                     # noqa E501
    (TwS(Stt.NOT_EXIST, Stt.NOT_EXIST),                 Act.VACATE_TARGET_IF_EXIST,                 TwS(Stt.NOT_EXIST,  Stt.NOT_EXIST)),                    # noqa E501
    (TwS(Stt.NOT_EXIST, Stt.BACKUP),                    Act.VACATE_TARGET_IF_EXIST_ASSERT_ERROR,    TwS(Stt.NOT_EXIST,  Stt.BACKUP)),                       # noqa E501
    # test_restore_backup_if_exist
    (TwS(Stt.EXISTING,  Stt.BACKUP),                    Act.RESTORE_BACKUP_IF_EXIST,                TwS(Stt.BACKUP,     Stt.NOT_EXIST)),                    # noqa E501
    (TwS(Stt.EXISTING,  Stt.NOT_EXIST),                 Act.RESTORE_BACKUP_IF_EXIST,                TwS(Stt.EXISTING,   Stt.NOT_EXIST)),                    # noqa E501
    # test_deploy_resource
    (ThS(Stt.EXISTING,  Stt.NOT_EXIST,  Stt.RESOURCE),  Act.DEPLOY_RESOURCE,                        ThS(Stt.RESOURCE,   Stt.EXISTING,   Stt.RESOURCE)),     # noqa E501
    (ThS(Stt.NOT_EXIST, Stt.NOT_EXIST,  Stt.RESOURCE),  Act.DEPLOY_RESOURCE,                        ThS(Stt.RESOURCE,   Stt.NOT_EXIST,  Stt.RESOURCE)),     # noqa E501
    (ThS(Stt.NOT_EXIST, Stt.NOT_EXIST,  Stt.NOT_EXIST), Act.DEPLOY_RESOURCE_ASSERT_ERROR,           ThS(Stt.NOT_EXIST,  Stt.NOT_EXIST,  Stt.NOT_EXIST)),    # noqa E501
    # TestTargetFilePathVacator
    # test_setup
    (TwS(Stt.EXISTING,  Stt.NOT_EXIST),                 Act.VACATOR_SETUP,                          TwS(Stt.NOT_EXIST,  Stt.EXISTING)),                     # noqa E501
    (TwS(Stt.EXISTING,  Stt.NOT_EXIST),                 Act.VACATOR_SETUP_WITH_ARGUMENT,            TwS(Stt.NOT_EXIST,  Stt.EXISTING)),                     # noqa E501
    # test_teardown
    (TwS(Stt.EXISTING,  Stt.BACKUP),                    Act.VACATOR_TEARDOWN,                       TwS(Stt.BACKUP,     Stt.NOT_EXIST)),                    # noqa E501
    (TwS(Stt.EXISTING,  Stt.BACKUP),                    Act.VACATOR_TEARDOWN_WITH_ARGUMENT,         TwS(Stt.BACKUP,     Stt.NOT_EXIST)),                    # noqa E501
    # TestResourceFileDeployer
    # test_setup
    (ThS(Stt.EXISTING,  Stt.NOT_EXIST,  Stt.RESOURCE),  Act.DEPLOYER_SETUP,                         ThS(Stt.RESOURCE,   Stt.EXISTING,   Stt.RESOURCE)),     # noqa E501
    (ThS(Stt.EXISTING,  Stt.NOT_EXIST,  Stt.RESOURCE),  Act.DEPLOYER_SETUP_WITH_ARGUMENT,           ThS(Stt.RESOURCE,   Stt.EXISTING,   Stt.RESOURCE)),     # noqa E501
    # test_teardown (integration test)
    (ThS(Stt.EXISTING,  Stt.BACKUP,     Stt.RESOURCE),  Act.DEPLOYER_TEARDOWN,                      ThS(Stt.BACKUP,     Stt.NOT_EXIST,  Stt.RESOURCE)),     # noqa E501
    (ThS(Stt.EXISTING,  Stt.NOT_EXIST,  Stt.RESOURCE),  Act.DEPLOYER_TEARDOWN,                      ThS(Stt.EXISTING,   Stt.NOT_EXIST,  Stt.RESOURCE)),     # noqa E501
]


@pytest.fixture
def file_path_with_file(request, tmp_path):
    """
    This fixture prepares file path aggregate
    and files specified by param (TwoFilesState or ThreeFileState) on tmp_path.
    """
    yield FilePathWithFileFactory.create(tmp_path, request.param)


class TestFixtureFileHandlerModules:
    """Tests for fixturefilehandler modules."""
    @staticmethod
    @pytest.mark.parametrize('file_path_with_file, action, expect', PARAMS, indirect=['file_path_with_file'])
    def test(file_path_with_file: VacateFilePathInterface, action: Act, expect: MultipleFileState):
        """Specific action should update state of each files to appropriate states."""
        action.execute(file_path_with_file)
        expect.assert_state(file_path_with_file)
