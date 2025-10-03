import shutil
from pathlib import Path

import pytest


@pytest.fixture
def datadir(tmp_path, request):
    """Provide a writable test data directory.

    If a folder trainer/tests/data/{test_name} exists it will be copied into a
    temporary directory so tests can modify the files. Otherwise an empty
    directory is returned.
    """
    test_data_dir = Path(__file__).parent / "data" / request.node.name
    dest = tmp_path / request.node.name
    if test_data_dir.exists():
        shutil.copytree(test_data_dir, dest)
    else:
        dest.mkdir(parents=True, exist_ok=True)
    return dest
