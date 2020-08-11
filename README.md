# Fixture File Handler

[![Test](https://github.com/yukihiko-shinoda/fixture-file-handler/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/fixture-file-handler/actions?query=workflow%3ATest)
[![Maintainability](https://api.codeclimate.com/v1/badges/063cfb039d7d9a2ff69d/maintainability)](https://codeclimate.com/github/yukihiko-shinoda/fixture-file-handler/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/063cfb039d7d9a2ff69d/test_coverage)](https://codeclimate.com/github/yukihiko-shinoda/fixture-file-handler/test_coverage)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/yukihiko-shinoda/fixture-file-handler)](https://codeclimate.com/github/yukihiko-shinoda/fixture-file-handler)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fixturefilehandler)](https://pypi.org/project/fixturefilehandler/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fixturefilehandler)](https://pypi.org/project/fixturefilehandler/)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Ffixture-file-handler)](http://twitter.com/share?text=Fixture%20File%20Handler&url=https://pypi.org/project/fixturefilehandler/&hashtags=python)

This project helps you to vacate specific file path or deploy resource file into specific file path when unit testing.

## Context

The most popular setup / teardown tasks about file system on unit testing is
almost 2 kinds.

1. vacate specific file path for testing file export function
2. deploy fixture file / directory into specific file path for testing file import /export function

Then we have to think about how to back up existing file / directory between unit testing
because maybe developer wants to keep those handwritten files for development.

`Fixture File Handler` is framework to realize simply implement
the vacate and deploy actions while keeping the existing files.
Of course, even if there is no file in the target path, it works fine.

## Ubiquitous Language

### target

The target file path to vacate or deploy file / directory for unit testing.

### backup

The file path to back up existing file / directory on target file path between unit testing.

### resource

The file / directory you want to deploy and let product code read / write in unit testing.
It may test resource file or template file like `*.dist` file.

## Basic behavior

### Vacator

target path|backup path
---|---
existing file /dir|&nbsp;

↓ setup

target path|backup path
---|---
&nbsp;|existing file / dir

↓ teardown

target path|backup path
---|---
existing file / dir|&nbsp;

### Deployer

target path|backup path|resource path
---|---|---
existing file / dir|&nbsp;|resource file / dir

↓ setup

target path|backup path|resource path
---|---|---
resource file / dir|existing file /dir|resource file / dir

↓ teardown

target path|backup path|resource path
---|---|---
existing file / dir|&nbsp;|resource file / dir

### Common behavior

If file / directory already exists on backup path,
setup raise `BackupAlreadyExistError`
because it's unexpected situation and developer may want to resque those backup files.

## Quickstart

### 1. Install

```console
pip install fixturefilehandler
```

### 2-1. Case when unittest: implement setUp() and doCleanups()

```python
from pathlib import Path
import unittest

from fixturefilehandler.factories import VacatorFactory
from fixturefilehandler.file_paths import RelativeVacateFilePath

VACATOR = VacatorFactory.create(
    RelativeVacateFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path(__file__).parent
    )
)


class ConfigurableTestCase(unittest.TestCase):
    def setUp(self):
        VACATOR.setup()

    def doCleanups(self):
        VACATOR.teardown()
```

### 2-2. Case when pytest: implement fixture

```python
from pathlib import Path
import pytest

from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import RelativeDeployFilePath

DEPLOYER = DeployerFactory.create(
    RelativeDeployFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path('testresources/test.txt.dist'),
        Path(__file__).parent
    )
)


@pytest.fixture
def fixture_file():
    DEPLOYER.setup()
    yield DEPLOYER.FILE_PATH
    DEPLOYER.teardown()


def test_something(fixture_file):
    """test something"""
```

## API

### file_paths

#### SimpleVacateFilePath

This instance holds path to target and backup.
Each path is independent each other.

#### SimpleDeployFilePath

This instance holds path to target, backup, and resource.
Each path is independent each other.

#### RelativeVacateFilePath

This instance holds path to target, backup, and base.
Each path is relative based on base path.

#### RelativeDeployFilePath

This instance holds path to target, backup, resource, and base.
Each path is relative based on base path.

<!-- markdownlint-disable no-trailing-punctuation -->
## How do I...
<!-- markdownlint-enable no-trailing-punctuation -->

<!-- markdownlint-disable no-trailing-punctuation -->
### Use different paths for each test?
<!-- markdownlint-enable no-trailing-punctuation -->

`setup()` and `teardown()` also accept file_paths argument.

Case when unittest:

```python
from pathlib import Path

import unittest

from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.file_paths import RelativeDeployFilePath


class AdvancedConfigurableTestCase(unittest.TestCase):
    @property
    def file_path(self) -> RelativeDeployFilePath:
        return RelativeDeployFilePath(
            Path('test.txt'),
            Path('test.txt.bak'),
            Path(f'testresources/{self._testMethodName}.txt'),
            Path(__file__).parent
        )

    def setUp(self):
        ResourceFileDeployer.setup(self.file_path)

    def doCleanups(self):
        ResourceFileDeployer.teardown(self.file_path)
```

Case when pytest:

```python
from pathlib import Path

import pytest

from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.file_paths import RelativeDeployFilePath


@pytest.fixture
def fixture_file_advanced(request):
    file_path = RelativeDeployFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path(f'testresources/{request.node.name}.txt'),
        Path(__file__).parent
    )

    ResourceFileDeployer.setup(file_path)
    yield file_path
    ResourceFileDeployer.teardown(file_path)


def test_something(fixture_file_advanced):
    """test something"""
```
