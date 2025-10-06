"""Simple compatibility test for the qt_compat shim.

Ensures that QtWidgets can be imported through the shim and a basic QWidget
can be created and shown using pytest-qt's qtbot fixture.
"""


def test_dummy_window(qtbot, qapp):
    from root_painter.qt_compat import QtWidgets

    w = QtWidgets.QWidget()
    qtbot.addWidget(w)
    w.setWindowTitle("Dummy")
    w.show()
    # allow the windowing system to map and show the widget
    qtbot.waitExposed(w, timeout=2000)
    assert w.isVisible()
    w.close()
