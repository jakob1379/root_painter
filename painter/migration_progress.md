# Migration Progress

This file tracks the to-do items for restructuring the `painter` project.

## Phase 1: Directory and File Restructuring

1.  **Create new directories:**
    - [x] `painter/src/root_painter/`
    - [x] `painter/src/root_painter/icons/`
    - [x] `painter/scripts/`

2.  **Move files and directories:**
    - [x] Move `painter/src/main/python/*.py` to `painter/src/root_painter/`.
    - [x] Create empty `painter/src/root_painter/__init__.py`.
    - [x] Move `painter/src/build/run_pyinstaller.py` to `painter/scripts/`.
    - [x] Move `painter/src/main/icons/export.py` to `painter/scripts/export_icons.py`.
    - [x] Move icon files (e.g., `icon.svg`, `Icon.ico`) from `painter/src/main/icons/` to `painter/src/root_painter/icons/`.

3.  **Clean up old directories:**
    - [x] Remove `painter/src/main/`.
    - [x] Remove `painter/src/build/`.

## Phase 2: Code Updates

-   [x] Update `painter/scripts/run_pyinstaller.py` to reflect new paths for the main script and icons.
-   [x] Update `painter/scripts/export_icons.py` to correctly locate `icon.svg`.
-   [x] Update `painter/src/root_painter/root_painter.py` to use a package-relative path for `missing.png`.
-   [x] Search for and update any other hardcoded relative paths.

## Phase 3: Verification

-   [x] Run the application to ensure it starts and functions correctly.
-   [x] Run `painter/scripts/run_pyinstaller.py` to verify the build process.
-   [x] Run `painter/scripts/export_icons.py` to verify icon exporting.
