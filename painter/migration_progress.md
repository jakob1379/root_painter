# Migration Progress

This file tracks the to-do items for restructuring the `painter` project.

## Phase 1: Directory and File Restructuring

1.  **Create new directories:**
    - [ ] `painter/src/root_painter/`
    - [ ] `painter/src/root_painter/icons/`
    - [ ] `painter/scripts/`

2.  **Move files and directories:**
    - [ ] Move `painter/src/main/python/*.py` to `painter/src/root_painter/`.
    - [ ] Create empty `painter/src/root_painter/__init__.py`.
    - [ ] Move `painter/src/build/run_pyinstaller.py` to `painter/scripts/`.
    - [ ] Move `painter/src/main/icons/export.py` to `painter/scripts/export_icons.py`.
    - [ ] Move icon files (e.g., `icon.svg`, `Icon.ico`) from `painter/src/main/icons/` to `painter/src/root_painter/icons/`.

3.  **Clean up old directories:**
    - [ ] Remove `painter/src/main/`.
    - [ ] Remove `painter/src/build/`.

## Phase 2: Code Updates

-   [ ] Update `painter/scripts/run_pyinstaller.py` to reflect new paths for the main script and icons.
-   [ ] Update `painter/scripts/export_icons.py` to correctly locate `icon.svg`.
-   [ ] Update `painter/src/root_painter/root_painter.py` to use a package-relative path for `missing.png`.
-   [ ] Search for and update any other hardcoded relative paths.

## Phase 3: Verification

-   [ ] Run the application to ensure it starts and functions correctly.
-   [ ] Run `painter/scripts/run_pyinstaller.py` to verify the build process.
-   [ ] Run `painter/scripts/export_icons.py` to verify icon exporting.
