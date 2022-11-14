from shutil import rmtree

import pytest


@pytest.fixture(scope="session")
def temp_data_dir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_data")
    yield temp_dir
    rmtree(temp_dir)
