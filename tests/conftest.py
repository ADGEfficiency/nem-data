import pytest


@pytest.fixture(scope="function")
def base_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("nem-data") / "data"
