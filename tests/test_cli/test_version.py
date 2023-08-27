import os
import pathlib

import semver
import toml

import downforeveryone


def test_version_set():
    assert isinstance(downforeveryone.__version__, str)
    assert len(downforeveryone.__version__) > 0


def test_version_is_semver():
    assert semver.VersionInfo.parse(downforeveryone.__version__)


def test_version_matches_pyproject():
    root_dir = pathlib.Path(__file__).parent.parent.parent
    with open(os.path.join(root_dir, "pyproject.toml")) as f:
        pyproject = toml.load(f)
        pyproject_version = pyproject.get("tool").get("poetry").get("version")

        assert pyproject_version == downforeveryone.__version__
