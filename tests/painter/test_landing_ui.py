"""Tests for the RootPainter landing UI state (no project loaded)."""

import json
from pathlib import Path

from PIL import Image

from root_painter.qt_compat import Qt, QtWidgets


def _button_texts(widget):
    return [btn.text() for btn in widget.findChildren(QtWidgets.QPushButton)]


def test_landing_buttons_present(main_window):
    central = main_window.centralWidget()
    texts = _button_texts(central)
    assert "Open existing project" in texts
    assert "Create new project" in texts
    assert any("Create training dataset" in t for t in texts)


def test_create_project_button_opens_widget(main_window, qtbot):
    central = main_window.centralWidget()
    button = next(
        btn
        for btn in central.findChildren(QtWidgets.QPushButton)
        if btn.text() == "Create new project"
    )
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(
        lambda: hasattr(main_window, "create_project_widget")
        and main_window.create_project_widget.isVisible(),
        timeout=2000,
    )
    qtbot.addWidget(main_window.create_project_widget)
    assert main_window.create_project_widget.isVisible()


def test_create_dataset_button_opens_widget(main_window, qtbot):
    central = main_window.centralWidget()
    button = next(
        btn
        for btn in central.findChildren(QtWidgets.QPushButton)
        if "Create training dataset" in btn.text()
    )
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(
        lambda: hasattr(main_window, "create_dataset_widget")
        and main_window.create_dataset_widget.isVisible(),
        timeout=2000,
    )
    qtbot.addWidget(main_window.create_dataset_widget)
    assert main_window.create_dataset_widget.isVisible()


def test_open_project_action_loads_project(main_window, qtbot, tmp_path, monkeypatch):
    sync_dir = Path(main_window.sync_dir)
    dataset_dir = sync_dir / "datasets" / "landing_test"
    project_dir = sync_dir / "projects" / "landing_project"
    annotations_train = project_dir / "annotations" / "train"
    annotations_val = project_dir / "annotations" / "val"
    seg_dir = project_dir / "segmentations"
    model_dir = project_dir / "models"
    message_dir = project_dir / "messages"
    log_dir = project_dir / "logs"

    for folder in (
        dataset_dir,
        annotations_train,
        annotations_val,
        seg_dir,
        model_dir,
        message_dir,
        log_dir,
    ):
        folder.mkdir(parents=True, exist_ok=True)

    image_name = "foo.png"
    Image.new("RGB", (16, 16), 0x112233).save(dataset_dir / image_name)
    Image.new("RGBA", (16, 16)).save(seg_dir / image_name)

    proj_file = project_dir / "landing_project.seg_proj"
    proj_info = {
        "name": "landing_project",
        "dataset": "landing_test",
        "original_model_file": "random weights",
        "location": "projects/landing_project",
        "file_names": [image_name],
    }
    proj_file.write_text(json.dumps(proj_info, indent=4), encoding="utf-8")

    try:
        QtWidgets.QFileDialog.Options
    except AttributeError:
        monkeypatch.setattr(QtWidgets.QFileDialog, "Options", lambda: 0, raising=False)

    def fake_get_open_file_name(*args, **kwargs):
        return str(proj_file), ""

    monkeypatch.setattr(QtWidgets.QFileDialog, "getOpenFileName", staticmethod(fake_get_open_file_name))

    monkeypatch.setattr(main_window, "send_instruction", lambda *args, **kwargs: None)

    main_window.open_project_action.trigger()

    def nav_label_ready():
        return (
            hasattr(main_window, "graphics_view")
            and hasattr(main_window, "nav")
            and main_window.nav.nav_label.text() != ""
        )

    qtbot.waitUntil(nav_label_ready, timeout=3000)
    assert hasattr(main_window, "scene")
    assert main_window.nav.nav_label.text().startswith("1 / 1")


def test_segment_folder_action_opens_widget(main_window, qtbot):
    action = main_window.segment_folder_btn
    action.trigger()
    qtbot.waitUntil(
        lambda: hasattr(main_window, "segment_folder_widget")
        and main_window.segment_folder_widget.isVisible(),
        timeout=2000,
    )
    qtbot.addWidget(main_window.segment_folder_widget)
    assert main_window.segment_folder_widget.isVisible()
