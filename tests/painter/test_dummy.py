from PyQt5 import QtCore, QtWidgets
from time import sleep

def test_dummy_button_closes_window(qtbot):
    # Create a simple window with a label and a button
    window = QtWidgets.QWidget()
    window.setWindowTitle("Dummy Window")
    layout = QtWidgets.QVBoxLayout(window)

    label = QtWidgets.QLabel("Not clicked", parent=window)
    button = QtWidgets.QPushButton("Click me", parent=window)

    layout.addWidget(label)
    layout.addWidget(button)

    # Button action: update label and close the window (simulate exiting app UI)
    def on_clicked():
        label.setText("Clicked")
        window.close()

    button.clicked.connect(on_clicked)

    # Show window and register it with qtbot for cleanup
    qtbot.addWidget(window)
    window.show()

    sleep(5)
    assert window.isVisible()

    # Click the button
    qtbot.mouseClick(button, QtCore.Qt.LeftButton)

    # Verify that button worked (label updated) and window closed
    qtbot.waitUntil(lambda: not window.isVisible(), timeout=3000)
    assert label.text() == "Clicked"
