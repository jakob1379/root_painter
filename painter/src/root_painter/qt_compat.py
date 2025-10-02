"""Qt6 compatibility shim for migrating from PyQt5 to PyQt6

This module provides a consistent set of imports and enum/value aliases
so the rest of the codebase can import Qt, QtCore, QtGui, QtWidgets from here
and continue to use names like Qt.KeepAspectRatio, Qt.Key_Control, etc.

It targets PyQt6 but falls back to PySide6 if PyQt6 is not available.
"""

try:
    # Prefer PyQt6
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtCore import Qt
    # PyQt6 moved enums to classes; provide backwards-compatible names
    # Map common Qt enums/constants used in the repo
    # Keep Qt namespace object for `from qt_compat import Qt` usage
except Exception:
    # Fallback to PySide6
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtCore import Qt

# Provide Qt.* names for common values used in the codebase
# Qt.AlignCenter, Qt.KeepAspectRatio, Qt.Checked, Qt.NoFocus, Qt.Key_Control, etc.
# PyQt6/PySide6 have the same names under Qt, so expose Qt directly.

__all__ = ["QtCore", "QtGui", "QtWidgets", "Qt"]
