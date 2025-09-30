"""
RootPainter package initializer.

Provide a lazy entrypoint helper so importing the package doesn't import
heavy GUI dependencies. Use init_root_painter() to start the UI, or run as:
    python -m root_painter
"""
from typing import Any

__all__ = ["init_root_painter"]


def init_root_painter(*args: Any, **kwargs: Any):
    """Lazily import painter.main and call its init_root_painter function.

    This avoids importing PyQt5 at package import time.
    """
    import importlib

    main = importlib.import_module('.main', package=__name__)
    func = getattr(main, 'init_root_painter', None)
    if func is None:
        raise ImportError("root_painter.main does not define init_root_painter")
    return func(*args, **kwargs)

