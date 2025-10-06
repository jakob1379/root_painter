"""Pytest fixtures for GUI integration tests using pytest-qt.

Autouse fixture `sanitized_argv` prevents pytest argv from being interpreted
by the application as a .seg_proj project file during test collection/execution.

Fixture `main_window` constructs the RootPainter main window using the
`tmp_path` as the sync directory and yields the visible window for tests.
"""

import sys
import pytest


@pytest.fixture(autouse=True)
def sanitized_argv():
    """Ensure sys.argv does not contain extra paths that RootPainter may parse.

    Many tests call application code that inspects sys.argv to decide whether
    to open a project file on startup. Pytest injects test filenames into
    argv which can confuse the app; clear argv for the duration of each test.
    """
    orig = sys.argv[:]
    sys.argv[:] = [orig[0]]
    try:
        yield
    finally:
        sys.argv[:] = orig


@pytest.fixture
def main_window(qtbot, qapp, tmp_path):
    """Create and show the RootPainter main window using a temporary sync dir.

    Yields the shown window and ensures it is closed after the test.
    """
    # Import lazily so tests that don't require Qt can still collect.
    from root_painter.root_painter import RootPainter

    # tmp_path is a pathlib.Path; RootPainter expects a Path-like sync dir.
    win = RootPainter(tmp_path)
    qtbot.addWidget(win)
    win.show()
    # Wait until exposed to avoid race conditions with dialogs/actions
    qtbot.waitExposed(win, timeout=2000)
    qapp.processEvents()
    yield win
    try:
        win.close()
    except Exception:
        pass
