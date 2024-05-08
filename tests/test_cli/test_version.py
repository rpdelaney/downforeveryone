from pathlib import Path

import semver
import toml

import downforeveryone


def test_version_set():
    """Verify that there is a version."""
    assert isinstance(downforeveryone.__version__, str)
    assert len(downforeveryone.__version__) > 0


def test_version_is_semver():
    """Verify that the version conforms to the semver spec."""
    assert semver.VersionInfo.parse(downforeveryone.__version__)


def test_version_matches_pyproject():
    """Verify that the version matches the build system."""
    root_dir = Path(__file__).parent.parent.parent
    with Path.open(Path(root_dir, "pyproject.toml")) as f:
        pyproject = toml.load(f)
        pyproject_version = pyproject.get("tool").get("poetry").get("version")

        assert pyproject_version == downforeveryone.__version__
