"""Qt6 compatibility shim for migrating from PyQt5 to PyQt6/PySide6.

This module exposes QtCore, QtGui, QtWidgets and a compatibility Qt object
that provides legacy-style enum/member names used throughout the codebase,
for example: Qt.KeepAspectRatio, Qt.AlignCenter, Qt.Key_Control, Qt.red, etc.

It prefers PyQt6 but falls back to PySide6. The shim resolves names by
searching in the Qt namespace and common nested enum classes so existing
code that used PyQt5-style names keeps working under Qt6.
"""

try:
    # Prefer PyQt6
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtCore import Qt as _Qt

    _BACKEND = "PyQt6"
except Exception:
    try:
        from PySide6 import QtCore, QtGui, QtWidgets
        from PySide6.QtCore import Qt as _Qt

        _BACKEND = "PySide6"
    except Exception as exc:  # pragma: no cover - import-time environment dependent
        raise ImportError("No Qt bindings found. Install PyQt6 or PySide6") from exc


class _QtCompat:
    """Compatibility object that exposes legacy Qt.* names.

    Accessing attributes on this object will try to look up the name on the
    top-level Qt enum class and on a list of commonly used nested enum classes
    (AlignmentFlag, AspectRatioMode, Key, KeyboardModifier, PenStyle, etc.).
    The shim also supports legacy underscores style names such as "Key_Control"
    by mapping them to the appropriate nested enum (Key.Control).
    """

    def __getattr__(self, name: str):
        # Direct attribute on Qt (some values are available directly)
        if hasattr(_Qt, name):
            return getattr(_Qt, name)

        # Handle legacy names like Key_Control -> Key.Control
        if "_" in name:
            parts = name.split("_", 1)
            cls_name, attr = parts[0], parts[1]
            cls = getattr(_Qt, cls_name, None)
            if cls is not None and hasattr(cls, attr):
                return getattr(cls, attr)
            # try capitalized attr
            cap = attr[0].upper() + attr[1:]
            if cls is not None and hasattr(cls, cap):
                return getattr(cls, cap)

        # Common nested enum class names to search for the attribute
        nested_names = [
            "AlignmentFlag",
            "AspectRatioMode",
            "KeyboardModifier",
            "Key",
            "PenStyle",
            "PenCapStyle",
            "PenJoinStyle",
            "BrushStyle",
            "GlobalColor",
            "CheckState",
            "FocusPolicy",
            "MouseButton",
            "WindowType",
        ]

        for nested in nested_names:
            cls = getattr(_Qt, nested, None)
            if cls is None:
                continue
            # exact match
            if hasattr(cls, name):
                return getattr(cls, name)
            # try capitalized variant (e.g. 'red' -> 'Red')
            cap = name[0].upper() + name[1:]
            if hasattr(cls, cap):
                return getattr(cls, cap)

        # Some Qt enums are present directly under QtCore.Qt in older code; try a final fallback
        # to look for uppercase variants on the top-level object
        cap = name[0].upper() + name[1:]
        if hasattr(_Qt, cap):
            return getattr(_Qt, cap)

        raise AttributeError(f"Qt enum/member '{name}' not found in {_BACKEND}")

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<QtCompat backend={_BACKEND}>"


# Export compatibility object instance as Qt (so callers can use `from qt_compat import Qt`)
Qt = _QtCompat()

__all__ = ["QtCore", "QtGui", "QtWidgets", "Qt"]
