"""GUI smoke test: ensure the main window can be created and shown.

Uses pytest-qt's qapp/qtbot fixtures to create a QApplication and show the
RootPainter main window. This is a lightweight smoke-test that verifies the
Qt bindings and basic UI construction paths work in the test environment.
"""


def test_root_painter_starts(qtbot, qapp, tmp_path):
    """Create RootPainter with a temporary sync directory and ensure it shows.

    This will raise if the Qt bindings are missing or if key UI classes
    (e.g. QAction) are not available under the expected modules.
    """
    # Import lazily so pytest collection can run in environments without Qt
    from root_painter.root_painter import RootPainter

    sync_dir = tmp_path
    # Construct the main window
    window = RootPainter(sync_dir)
    qtbot.addWidget(window)
    window.show()
    # Wait until visible or timeout (milliseconds)
    qtbot.waitUntil(lambda: window.isVisible(), timeout=2000)
    assert window.isVisible()
    # Close the window to clean up
    window.close()
