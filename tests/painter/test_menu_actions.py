"""Integration tests for top-level menus and actions using pytest-qt.

These tests rely on the `main_window` fixture declared in tests/conftest.py
which constructs and shows the RootPainter main window using a temporary
sync directory. Tests use qtbot to interact with QActions and wait for dialogs
or widgets to appear.
"""

from root_painter.qt_compat import QtWidgets


def test_top_level_menus_present(main_window):
    """Assert top-level menus and a few actions are present with expected text."""
    window = main_window
    menu_texts = [a.text() for a in window.menuBar().actions()]
    for expected in ("Project", "Network", "Extras", "About"):
        assert any(expected in t for t in menu_texts), (
            f"Missing menu '{expected}' in {menu_texts}"
        )

<<<<<<< HEAD
    # Check a couple of actions exist on the Project menu
    project_actions = [a.text() for a in window.project_menu.actions()]
    assert any("Open project" in t for t in project_actions)
    assert any("Create project" in t for t in project_actions)


def test_trigger_about_shows_dialog(main_window, qtbot):
    """Trigger Help/About (About RootPainter) and assert AboutWindow opens."""
    window = main_window
    # Find the about action on the About menu
    about_action = None
    for act in window.menuBar().actions():
        if act.text().strip() == "About":
            about_menu = act.menu()
            # find RootPainter action
            for sub in about_menu.actions():
                if "RootPainter" in sub.text():
                    about_action = sub
                    break
            break

    assert about_action is not None, "Could not find About -> RootPainter action"

    # Trigger and wait for window
    about_action.trigger()
    qtbot.waitUntil(lambda: hasattr(window, "about_window") and window.about_window.isVisible(),
                    timeout=2000)
    assert window.about_window.windowTitle() == "About RootPainter"
    # Close
    window.about_window.close()


def test_trigger_create_project_shows_widget(main_window, qtbot):
    window = main_window
    # find Create project action on Project menu
    create_act = None
    for act in window.project_menu.actions():
        if "Create project" in act.text():
            create_act = act
            break

    assert create_act is not None
    create_act.trigger()
    qtbot.waitUntil(lambda: hasattr(window, "create_project_widget") and window.create_project_widget.isVisible(),
                    timeout=2000)
    # Close the widget
    window.create_project_widget.close()
=======

def test_create_project_opens_dialog(main_window, qtbot):
    # Trigger the create project action and assert the CreateProjectWidget is shown
    action = main_window.create_project_action
    assert action is not None
    action.trigger()

    qtbot.waitUntil(
        lambda: hasattr(main_window, "create_project_widget")
        and main_window.create_project_widget.isVisible(),
        timeout=2000,
    )
    assert main_window.create_project_widget.isVisible()


def test_about_and_license_open(main_window, qtbot):
    # Find the About menu and its actions
    about_menu_action = next((a for a in main_window.menuBar().actions() if "About" in a.text()), None)
    assert about_menu_action is not None
    about_menu = about_menu_action.menu()

    license_action = next((a for a in about_menu.actions() if "License" in a.text()), None)
    about_action = next((a for a in about_menu.actions() if "RootPainter" in a.text() or "About" in a.text()), None)

    assert license_action is not None
    assert about_action is not None

    license_action.trigger()
    qtbot.waitUntil(lambda: hasattr(main_window, "license_window") and main_window.license_window.isVisible(), timeout=2000)
    assert main_window.license_window.isVisible()

    about_action.trigger()
    qtbot.waitUntil(lambda: hasattr(main_window, "about_window") and main_window.about_window.isVisible(), timeout=2000)
    assert main_window.about_window.isVisible()
>>>>>>> origin/test/integration/menu-actions
