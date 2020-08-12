import toml

import downforeveryone


def test_version_set():
    assert isinstance(downforeveryone.__version__, str)
    assert len(downforeveryone.__version__) > 0


def test_version_matches_pyproject():
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)
        pyproject_version = pyproject.get("tool").get("poetry").get("version")

        assert pyproject_version == downforeveryone.__version__
