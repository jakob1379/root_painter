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
    # Prevent pytest's argv (which often contains the test file path) from being
    # interpreted by the app as a .seg_proj project file.
    import sys

    sys.argv = [sys.argv[0]]
    from root_painter.root_painter import RootPainter

    sync_dir = tmp_path
    # Construct the main window
    window = RootPainter(sync_dir)
    qtbot.addWidget(window)
    window.show()
    # Wait until the window is exposed to the windowing system and painted
    qtbot.waitExposed(window, timeout=2000)
    # Give the event loop a chance to finish painting
    qapp.processEvents()
    # Basic textual checks (window title, menubar menus, and central buttons)
    assert "RootPainter" in window.windowTitle()
    menu_texts = [a.text() for a in window.menuBar().actions()]
    for expected in ("Project", "Network", "Extras", "About"):
        assert any(expected in t for t in menu_texts), (
            f"Missing menu '{expected}' in {menu_texts}"
        )
    # central project buttons when project not set
    central = window.centralWidget()
    assert central is not None
    from root_painter.qt_compat import QtWidgets

    buttons = [b.text() for b in central.findChildren(QtWidgets.QPushButton)]
    assert any("Open existing project" == t for t in buttons), (
        f"Missing Open button: {buttons}"
    )
    assert any("Create new project" == t for t in buttons), (
        f"Missing Create button: {buttons}"
    )
    assert any("Create training dataset" in t for t in buttons), (
        f"Missing Create dataset button: {buttons}"
    )
    # Close the window to clean up
    from time import sleep

    sleep(4)
    window.close()
