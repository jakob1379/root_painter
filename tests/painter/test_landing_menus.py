"""Integration tests for landing state menu actions without existing coverage."""

import sys
from pathlib import Path

import pytest

from root_painter import root_painter as root_painter_module
from root_painter.qt_compat import QtWidgets


def _find_menu_action(window, menu_text: str, action_text: str):
    menu_action = next(
        (action for action in window.menuBar().actions() if menu_text in action.text()),
        None,
    )
    assert menu_action is not None, f"Menu '{menu_text}' not found"
    menu = menu_action.menu()
    action = next((a for a in menu.actions() if action_text in a.text()), None)
    assert action is not None, f"Action '{action_text}' not found in menu '{menu_text}'"
    return action


@pytest.mark.parametrize(
    ("action_text", "attr_name"),
    [
        ("Extract count", "extract_count_widget"),
        ("Extract length", "extract_length_widget"),
        ("Extract region properties", "extract_regions_widget"),
    ],
)
def test_measurements_actions_show_widgets(main_window, qtbot, action_text, attr_name):
    action = _find_menu_action(main_window, "Measurements", action_text)
    action.trigger()

    qtbot.waitUntil(lambda: hasattr(main_window, attr_name), timeout=2000)
    widget = getattr(main_window, attr_name)
    qtbot.addWidget(widget)
    assert widget.isVisible()
    widget.close()


@pytest.mark.parametrize(
    ("action_text", "attr_name"),
    [
        ("Extract composites", "extract_comp_widget"),
        ("Convert segmentations for RhizoVision Explorer", "convert_to_rve_widget"),
        ("Convert segmentations to annotations", "convert_to_annot_widget"),
        ("Mask images", "mask_im_widget"),
        ("Assign Corrections", "assign_corrections_widget"),
        ("Create random split", "random_split_widget"),
        ("Resize images", "resize_images_widget"),
    ],
)
def test_extras_actions_create_widgets(main_window, qtbot, action_text, attr_name):
    action = _find_menu_action(main_window, "Extras", action_text)
    action.trigger()

    qtbot.waitUntil(lambda: hasattr(main_window, attr_name), timeout=2000)
    widget = getattr(main_window, attr_name)
    qtbot.addWidget(widget)
    assert widget.isVisible()
    widget.close()


def test_specify_sync_directory_updates_paths(
    main_window, qtbot, tmp_path, monkeypatch
):
    new_sync = tmp_path / "new_sync"
    new_sync.mkdir()
    fake_home = tmp_path / "home"
    fake_home.mkdir()

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getExistingDirectory",
        staticmethod(lambda *args, **kwargs: str(new_sync)),
    )

    action = _find_menu_action(main_window, "Extras", "Specify sync directory")
    action.trigger()

    qtbot.waitUntil(lambda: main_window.sync_dir == new_sync.resolve(), timeout=2000)
    assert main_window.instruction_dir == new_sync.resolve() / "instructions"


def test_open_sync_directory_invokes_platform_opener(main_window, monkeypatch):
    called = {}

    if sys.platform == "win32":

        def fake_startfile(path):
            called["path"] = path

        monkeypatch.setattr(root_painter_module.os, "startfile", fake_startfile)
    else:

        def fake_call(args):
            called["args"] = args
            return 0

        monkeypatch.setattr(root_painter_module.subprocess, "call", fake_call)

    action = _find_menu_action(main_window, "Extras", "Open sync directory")
    action.trigger()

    if sys.platform == "win32":
        assert Path(called["path"]) == main_window.sync_dir
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        assert called["args"][0] == opener
        assert Path(called["args"][1]) == main_window.sync_dir
