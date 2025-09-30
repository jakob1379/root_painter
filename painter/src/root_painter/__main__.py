"""Package run entrypoint for root_painter.

This delegates to the lazy init_root_painter defined in the package
__init__.py so importing the package still avoids pulling in heavy GUI
dependencies until the UI is actually started.
"""

from typing import Any


def main(*args: Any, **kwargs: Any) -> Any:
    """Start the RootPainter UI.

    This simply delegates to root_painter.init_root_painter().
    """
    # Import lazily from the package so we don't import PyQt5 at module
    # import time.
    from . import init_root_painter

    return init_root_painter(*args, **kwargs)


if __name__ == "__main__":
    main()
