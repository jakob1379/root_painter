"""Integration tests covering key project-mode menu interactions."""

import json
from pathlib import Path

import pytest

from root_painter import root_painter as root_painter_module
from root_painter.qt_compat import Qt, QtCore, QtGui, QtWidgets


def _find_menu_action(window, menu_text: str, action_text: str) -> QtWidgets.QAction:
    menu_action = next(
        (action for action in window.menuBar().actions() if menu_text in action.text()),
        None,
    )
    assert menu_action is not None, f"Menu '{menu_text}' not found"
    menu = menu_action.menu()
    action = next((a for a in menu.actions() if action_text in a.text()), None)
    assert action is not None, f"Action '{action_text}' not found in menu '{menu_text}'"
    return action


def _trigger(window, menu_text: str, action_text: str) -> None:
    action = _find_menu_action(window, menu_text, action_text)
    action.trigger()
    QtWidgets.QApplication.processEvents()


def test_close_project_action_closes_window(project_window, qtbot):
    closed = []
    project_window.closed.connect(lambda: closed.append(True))

    _trigger(project_window, "Project", "Close project")
    qtbot.wait(100)
    assert closed
    assert not project_window.isVisible()


@pytest.mark.parametrize(
    ("action_text", "method_name"),
    [
        ("Undo", "undo"),
        ("Redo", "redo"),
    ],
)
def test_edit_menu_calls_scene_methods(
    project_window, monkeypatch, action_text, method_name
):
    scene = project_window.scene
    base = scene.annot_pixmap.copy()
    scene.history = [base.copy(), base.copy()]
    scene.redo_list = [base.copy()] if method_name == "redo" else []

    original = getattr(scene, method_name)
    called = {}

    def wrapped():
        called["called"] = True
        original()

    monkeypatch.setattr(scene, method_name, wrapped)
    action = _find_menu_action(project_window, "Edit", action_text)
    action.triggered.disconnect()
    action.triggered.connect(getattr(scene, method_name))
    action.trigger()
    QtWidgets.QApplication.processEvents()
    assert called.get("called")


def test_options_menu_updates_state(project_window, monkeypatch):
    monkeypatch.setattr(
        QtWidgets.QInputDialog, "getInt", staticmethod(lambda *_, **__: (7, True))
    )
    _trigger(project_window, "Options", "Pre-Segment")
    assert project_window.pre_segment_count == 7

    responses = iter([("Enabled", True), ("Disabled", True)])
    monkeypatch.setattr(
        QtWidgets.QInputDialog,
        "getItem",
        staticmethod(lambda *_, **__: next(responses)),
    )
    monkeypatch.setattr(
        QtWidgets.QApplication,
        "keyboardModifiers",
        staticmethod(lambda: Qt.KeyboardModifier.NoModifier),
    )
    _trigger(project_window, "Options", "Contrast enhance")
    assert project_window.contrast_enhance_enabled
    _trigger(project_window, "Options", "Contrast enhance")
    assert not project_window.contrast_enhance_enabled

    monkeypatch.setattr(
        QtWidgets.QInputDialog, "getInt", staticmethod(lambda *_, **__: (21, True))
    )
    _trigger(project_window, "Options", "Change brush size")
    assert project_window.scene.brush_size == 21


@pytest.mark.parametrize(
    ("action_text", "attr_name"),
    [
        ("Foreground brush colour", "foreground_color"),
        ("Background brush colour", "background_color"),
    ],
)
def test_colour_dialog_actions(project_window, monkeypatch, action_text, attr_name):
    new_color = QtGui.QColor(12, 34, 56)
    monkeypatch.setattr(
        QtWidgets.QColorDialog, "getColor", staticmethod(lambda *_, **__: new_color)
    )
    _trigger(project_window, "Options", action_text)
    assert getattr(project_window.scene, attr_name) == new_color


@pytest.mark.parametrize(
    ("menu_text", "action_text", "attr_name"),
    [
        ("Brushes", "Foreground", "foreground_color"),
        ("Brushes", "Background", "background_color"),
        ("Brushes", "Eraser", "eraser_color"),
    ],
)
def test_brush_menu_changes_active_color(
    project_window, menu_text, action_text, attr_name
):
    project_window.scene.brush_color = project_window.scene.background_color
    _trigger(project_window, menu_text, action_text)
    assert project_window.scene.brush_color == getattr(project_window.scene, attr_name)


def test_view_menu_controls_zoom_and_visibility(project_window, monkeypatch):
    view = project_window.graphics_view
    initial_zoom = view.zoom

    _trigger(project_window, "View", "Fit to View")
    assert view.zoom != initial_zoom

    _trigger(project_window, "View", "Actual size")
    assert view.zoom == 1

    for action_text, method_name in (
        ("Toggle segmentation visibility", "show_hide_seg"),
        ("Toggle annotation visibility", "show_hide_annot"),
        ("Toggle image visibility", "show_hide_image"),
    ):
        original = getattr(project_window, method_name)
        called = {}

        def wrapped():
            called["called"] = True
            original()

        monkeypatch.setattr(project_window, method_name, wrapped)
        action = _find_menu_action(project_window, "View", action_text)
        action.triggered.disconnect()
        action.triggered.connect(getattr(project_window, method_name))
        action.trigger()
        QtWidgets.QApplication.processEvents()
        assert called.get("called")

    before_zoom = view.zoom
    _trigger(project_window, "View", "Zoom in")
    assert view.zoom > before_zoom
    _trigger(project_window, "View", "Zoom out")
    assert view.zoom < before_zoom or view.zoom == before_zoom


def test_view_context_action_uses_viewer(project_window, monkeypatch, tmp_path):
    originals = tmp_path / "orig"
    originals.mkdir()
    src = Path(project_window.image_path)
    (originals / src.name).write_bytes(src.read_bytes())

    proj_path = Path(project_window.proj_file_path)
    proj_data = json.loads(proj_path.read_text(encoding="utf-8"))
    proj_data["original_image_dir"] = str(originals)
    proj_path.write_text(json.dumps(proj_data), encoding="utf-8")

    created = {}

    class DummyViewer:
        def __init__(self, *_, **__):
            created["instance"] = self

        def show(self):
            created["shown"] = True

        def update(self, path, pixmap):
            created["update"] = (path, pixmap)

    monkeypatch.setattr(root_painter_module, "ContextViewer", DummyViewer)
    monkeypatch.setattr(
        project_window,
        "update_context_viewer",
        lambda: created.__setitem__("update_called", True),
    )
    _trigger(project_window, "View", "View image context")

    assert "instance" in created
    assert "shown" in created
    assert "update_called" in created


def test_controls_dialog_opens(project_window, qtbot, monkeypatch):
    created = {}

    class DummyDialog(QtWidgets.QDialog):
        closed = QtCore.pyqtSignal()

        def __init__(self, parent=None):
            super().__init__(parent)
            created["instance"] = self

        def show(self):
            created["shown"] = True
            super().show()

    monkeypatch.setattr(root_painter_module, "ControlsDialog", DummyDialog)
    project_window.show_controls(QtCore.Qt.Checked)
    QtWidgets.QApplication.processEvents()
    assert created.get("instance") is project_window.controls_dialog
    assert created.get("shown")
    project_window.controls_dialog.close()


@pytest.mark.parametrize(
    ("action_text", "expected"),
    [
        ("Start training", "start_training"),
        ("Stop training", "stop_training"),
    ],
)
def test_network_actions_forward_instructions(
    project_window, monkeypatch, action_text, expected
):
    captured = {}

    def fake_send(name, payload):
        captured["name"] = name
        captured["payload"] = payload

    monkeypatch.setattr(project_window, "send_instruction", fake_send)
    _trigger(project_window, "Network", action_text)
    assert captured.get("name") == expected


def test_export_metrics_widget(project_window, qtbot):
    _trigger(project_window, "Extras", "Export metrics CSV")
    qtbot.waitUntil(
        lambda: hasattr(project_window, "extract_metrics_widget"), timeout=2000
    )
    widget = project_window.extract_metrics_widget
    qtbot.addWidget(widget)
    assert widget.isVisible()
    widget.close()


def test_extend_dataset_updates_navigation(project_window, monkeypatch):
    new_files = [f"image_{idx:03d}.png" for idx in range(4)]

    def fake_extend(self_ref, dataset_dir, file_names, proj_file_path):
        return True, new_files

    monkeypatch.setattr(root_painter_module, "check_extend_dataset", fake_extend)
    _trigger(project_window, "Extras", "Extend dataset")
    assert project_window.image_fnames == new_files
    assert project_window.nav.all_fnames == new_files


@pytest.mark.parametrize(
    ("handler", "flag_attr", "method_name"),
    [
        ("im_checkbox_change", "image_visible", "show_hide_image"),
        ("seg_checkbox_change", "seg_visible", "show_hide_seg"),
        ("annot_checkbox_change", "annot_visible", "show_hide_annot"),
    ],
)
def test_visibility_handlers_toggle_flags(
    project_window, monkeypatch, handler, flag_attr, method_name
):
    called = {}

    def wrapped():
        called["called"] = True

    monkeypatch.setattr(project_window, method_name, wrapped)
    current = getattr(project_window, flag_attr)
    target_state = (
        QtCore.Qt.CheckState.Checked if not current else QtCore.Qt.CheckState.Unchecked
    )
    getattr(project_window, handler)(target_state)
    assert called.get("called")
