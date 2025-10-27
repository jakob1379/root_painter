"""Pytest fixtures for GUI integration tests using pytest-qt.

Autouse fixture `sanitized_argv` prevents pytest argv from being interpreted
by the application as a .seg_proj project file during test collection/execution.

Fixtures in this module construct RootPainter windows in both landing and
active-project configurations using temporary sync directories populated with
dummy data.
"""

import json
import os
import sys
from pathlib import Path

import pytest
import numpy as np
from PIL import Image

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from root_painter.qt_compat import Qt, QtCore, QtWidgets

try:
    from PyQt6 import QtGui as _QtGui

    if not hasattr(QtWidgets, "QShortcut") and hasattr(_QtGui, "QShortcut"):
        QtWidgets.QShortcut = _QtGui.QShortcut
except Exception:
    pass

try:
    QtCore.Qt.Checked
except AttributeError:
    try:
        QtCore.Qt.Checked = Qt.CheckState.Checked
    except AttributeError:
        pass

try:
    Qt.ControlModifier
except AttributeError:
    try:
        Qt.ControlModifier = Qt.KeyboardModifier.Control
    except AttributeError:
        Qt.ControlModifier = Qt.KeyboardModifier(2)

QtChecked = getattr(Qt, "CheckState", Qt)
QtModifier = getattr(Qt, "KeyboardModifier", Qt)


def _create_dummy_image(path: Path, color: int, mode: str = "RGB") -> None:
    channels = 4 if mode == "RGBA" else 3
    arr = np.zeros((32, 32, channels), dtype=np.uint8)
    if channels == 3:
        arr[..., 0] = (color >> 16) & 0xFF
        arr[..., 1] = (color >> 8) & 0xFF
        arr[..., 2] = color & 0xFF
    else:
        arr[..., 3] = 0
    Image.fromarray(arr, mode=mode).save(path)


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
    from root_painter.root_painter import RootPainter

    win = RootPainter(tmp_path)
    qtbot.addWidget(win)
    win.show()
    qtbot.waitExposed(win, timeout=2000)
    qapp.processEvents()
    yield win
    try:
        win.close()
    except Exception:
        pass
    finally:
        try:
            win.deleteLater()
        except Exception:
            pass
        QtWidgets.QApplication.processEvents()


@pytest.fixture
def project_window(qtbot, tmp_path, monkeypatch):
    """Create a RootPainter window with an active project and dummy dataset."""

    sync_dir = tmp_path
    dataset_dir = sync_dir / "datasets" / "demo_dataset"
    project_dir = sync_dir / "projects" / "demo_project"
    annotations_train = project_dir / "annotations" / "train"
    annotations_val = project_dir / "annotations" / "val"
    segmentation_dir = project_dir / "segmentations"
    model_dir = project_dir / "models"
    message_dir = project_dir / "messages"
    log_dir = project_dir / "logs"
    instructions_dir = sync_dir / "instructions"

    dataset_dir.mkdir(parents=True)
    project_dir.mkdir(parents=True)
    annotations_train.mkdir(parents=True)
    annotations_val.mkdir(parents=True)
    segmentation_dir.mkdir(parents=True)
    model_dir.mkdir(parents=True)
    message_dir.mkdir(parents=True)
    log_dir.mkdir(parents=True)
    instructions_dir.mkdir(parents=True)

    image_names = []
    for idx, color in enumerate((0x336699, 0x993333, 0x339966)):
        name = f"image_{idx:03d}.png"
        _create_dummy_image(dataset_dir / name, color)
        image_names.append(name)

    # Create placeholder segmentation files to keep navigation enabled
    for name in image_names:
        _create_dummy_image(segmentation_dir / name, 0x000000, mode="RGBA")

    proj_info = {
        "name": "demo_project",
        "dataset": "demo_dataset",
        "original_model_file": "random weights",
        "location": "projects/demo_project",
        "file_names": image_names,
    }
    proj_file = project_dir / "demo_project.seg_proj"
    with open(proj_file, "w", encoding="utf-8") as fh:
        json.dump(proj_info, fh, indent=4)

    from root_painter import root_painter as root_painter_module
    from root_painter.root_painter import RootPainter

    monkeypatch.setattr(
        root_painter_module.RootPainter, "track_changes", lambda self: None
    )

    orig_argv = sys.argv[:]
    sys.argv[:] = [orig_argv[0], str(proj_file)]

    win = RootPainter(sync_dir)
    win.send_instruction = lambda *args, **kwargs: None
    qtbot.addWidget(win)
    win.show()
    qtbot.waitExposed(win, timeout=3000)

    yield win

    try:
        win.close()
    except Exception:
        pass
    finally:
        try:
            win.deleteLater()
        except Exception:
            pass
        QtWidgets.QApplication.processEvents()
        sys.argv[:] = orig_argv
