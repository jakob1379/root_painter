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
    # Grab the rendered content and verify it is not a fully black/empty image.
    pixmap = window.grab()
    assert not pixmap.isNull()
    img = pixmap.toImage()
    w, h = img.width(), img.height()
    assert w > 0 and h > 0, "Grabbed image has zero size"
    # Sample a small 3x3 area around the center and check average brightness
    cx, cy = w // 2, h // 2
    brightness_total = 0
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            x, y = cx + dx, cy + dy
            if 0 <= x < w and 0 <= y < h:
                color = img.pixelColor(x, y)
                brightness_total += (color.red() + color.green() + color.blue()) / 3
                count += 1
    avg_brightness = brightness_total / max(1, count)
    assert avg_brightness > 10, (
        f"Window content appears too dark (avg={avg_brightness})"
    )
    # Close the window to clean up
    window.close()
