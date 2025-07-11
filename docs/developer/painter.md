# Painter (Client) Developer Documentation

This document provides instructions for developers working on the Painter (client) component of RootPainter. For user-facing documentation, please refer to the main project `README.md` and the `docs` directory.

Installers for OSX, Windows and Debian based linux distributions are available from the [releases page](https://github.com/Abe404/root_painter/releases), which is recommended for most users.
The instructions below are for building the painter from source.

The server (trainer) must be running for the client to function.

## Install dependencies
It is recommended to use a virtual environment.

    pip install -r painter/requirements.txt

### Windows Build Dependencies

For generating an executable on Windows, ensure that the following are installed and available in your system's PATH:
- [NSIS tools](https://nsis.sourceforge.io/Main_Page)
- [C++ Redistributable for Visual Studio 2012](https://www.microsoft.com/en-us/download/details.aspx?id=30679)
- [Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk)

## Running from source

    python painter/root_painter/main.py

## Building the application

To build the application for your current platform, run:

    python painter/scripts/run_pyinstaller.py

The output will be in the `dist/` directory.

## Building Installers

Installers must be created on the target platform (e.g., a Windows installer must be built on Windows).

### Windows (.exe)

    makensis painter/scripts/assets/Installer.nsi

### macOS (.pkg)

    pkgbuild --component dist/RootPainter.app --install-location /Applications dist/RootPainter.pkg

### Debian/Ubuntu (.deb)

    bash painter/scripts/make_deb_file

The output installer will be located at `dist/RootPainter.deb`. To install it:

    sudo dpkg -i dist/RootPainter.deb
