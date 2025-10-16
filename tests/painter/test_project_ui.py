"""Integration tests for the RootPainter UI when a project is loaded."""

from pathlib import Path

from root_painter.qt_compat import Qt, QtCore, QtWidgets


def test_window_enters_project_mode(project_window):
    assert isinstance(project_window.centralWidget(), QtWidgets.QWidget)
    assert hasattr(project_window, "graphics_view")
    assert hasattr(project_window, "scene")
    assert project_window.nav.nav_label.text().startswith("1 / 3")


def test_visibility_toggles(project_window, qtbot):
    widget = project_window.vis_widget

    assert project_window.image_visible
    project_window.show_hide_image()
    qtbot.waitUntil(lambda: not project_window.image_visible, timeout=1000)
    assert not widget.im_checkbox.isChecked()
    project_window.show_hide_image()
    QtWidgets.QApplication.processEvents()

    assert not project_window.seg_visible
    project_window.seg_pixmap_holder.setPixmap(project_window.seg_pixmap)
    project_window.seg_visible = True
    project_window.show_hide_seg()
    QtWidgets.QApplication.processEvents()
    project_window.show_hide_seg()
    qtbot.waitUntil(lambda: not project_window.seg_visible, timeout=1000)

    assert project_window.annot_visible
    project_window.show_hide_annot()
    qtbot.waitUntil(lambda: not project_window.annot_visible, timeout=1000)
    project_window.show_hide_annot()


def test_brush_color_actions(project_window):
    scene = project_window.scene
    original_color = scene.brush_color
    project_window.set_background_color(None)
    assert scene.brush_color == scene.background_color
    project_window.set_eraser_color(None)
    assert scene.brush_color == scene.eraser_color
    project_window.set_foreground_color(None)
    assert scene.brush_color == scene.foreground_color


def test_navigation_buttons_cycle_images(project_window, qtbot):
    nav = project_window.nav
    initial_path = project_window.image_path
    qtbot.mouseClick(nav.next_image_button, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: project_window.image_path != initial_path, timeout=2000)
    moved_path = project_window.image_path
    qtbot.mouseClick(nav.prev_image_button, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: project_window.image_path == initial_path, timeout=2000)
    assert project_window.image_path == initial_path
    assert moved_path != initial_path


def test_zoom_shortcuts_change_zoom(project_window):
    view = project_window.graphics_view
    initial_zoom = view.zoom
    project_window.graphics_view.fit_to_view()
    assert view.zoom != initial_zoom
    project_window.graphics_view.show_actual_size()
    assert view.zoom == 1


def test_options_dialog_changes_brush_size(project_window, monkeypatch):
    def fake_get_int(*args, **kwargs):
        return 42, True

    monkeypatch.setattr(QtWidgets.QInputDialog, "getInt", staticmethod(fake_get_int))
    project_window.show_brush_size_edit()
    assert project_window.scene.brush_size == 42


def test_contrast_toggle(project_window, monkeypatch):
    sequence = iter([("Enabled", True), ("Disabled", True)])

    def fake_get_item(*args, **kwargs):
        return next(sequence)

    monkeypatch.setattr(QtWidgets.QInputDialog, "getItem", staticmethod(fake_get_item))
    monkeypatch.setattr(
        QtWidgets.QApplication,
        "keyboardModifiers",
        staticmethod(lambda: Qt.KeyboardModifier.NoModifier),
    )
    monkeypatch.setattr(QtCore.Qt, "ControlModifier", Qt.KeyboardModifier.NoModifier, raising=False)
    project_window.open_contrast_enhance_dialog()
    assert project_window.contrast_enhance_enabled
    project_window.open_contrast_enhance_dialog()
    assert not project_window.contrast_enhance_enabled


def test_start_stop_training_send_instruction(project_window, monkeypatch):
    captured = []

    def fake_send_instruction(name, payload):
        captured.append((name, payload))

    monkeypatch.setattr(project_window, "send_instruction", fake_send_instruction)
    project_window.start_training()
    project_window.stop_training()
    assert captured[0][0] == "start_training"
    assert captured[1][0] == "stop_training"


def test_segment_folder_action(project_window, qtbot):
    action = None
    for menu_action in project_window.menuBar().actions():
        if menu_action.text() == "Network":
            for act in menu_action.menu().actions():
                if act.text() == "Segment folder":
                    action = act
                    break
        if action:
            break
    assert action is not None
    action.trigger()
    qtbot.waitUntil(
        lambda: hasattr(project_window, "segment_folder_widget")
        and project_window.segment_folder_widget.isVisible(),
        timeout=2000,
    )
    qtbot.addWidget(project_window.segment_folder_widget)
    assert project_window.segment_folder_widget.isVisible()


def test_metrics_plot_widgets(project_window, qtbot, monkeypatch):
    action = None
    for menu_action in project_window.menuBar().actions():
        if menu_action.text() == "Extras":
            for act in menu_action.menu().actions():
                if act.text() == "Show metrics plot":
                    action = act
                    break
        if action:
            break

    assert action is not None

    captured_navigation = []

    def fake_create_plot(proj_file, navigate, current_image):
        captured_navigation.append((proj_file, current_image))
        navigate(Path(current_image).name)

    monkeypatch.setattr(project_window.metrics_plot, "create_metrics_plot", fake_create_plot)

    action.trigger()
    assert captured_navigation
    assert captured_navigation[0][0] == project_window.proj_file_path
