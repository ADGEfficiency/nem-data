import pathlib

import pytest


@pytest.fixture(scope="function")
def base_dir(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("nem-data") / "data"
