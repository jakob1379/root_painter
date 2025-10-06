import sys
import pytest


@pytest.fixture(scope="session")
def qapp_path():
    """Ensure sys.argv doesn't confuse the application during collection/run."""
    # pytest-qt provides the QApplication (qapp) fixture; ensure argv is safe.
    sys.argv = [sys.argv[0]]
    return sys.argv


@pytest.fixture
def main_window(qtbot, qapp, tmp_path, qapp_path):
    """Create a RootPainter main window with a temporary sync directory.

    The import is done inside the fixture so pytest collection can run in
    environments without Qt installed.
    """
    # Import lazily to avoid requiring Qt at collection time
    from root_painter.root_painter import RootPainter

    sync_dir = tmp_path
    window = RootPainter(sync_dir)
    qtbot.addWidget(window)
    window.show()
    # wait until the window is exposed
    qtbot.waitExposed(window, timeout=2000)
    qapp.processEvents()
    yield window
    # cleanup
    try:
        window.close()
    except Exception:
        pass
