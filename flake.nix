{
  description = "Python development environment with Qt/GUI support";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        # Python environment - empty packages list for uv management
        # pythonEnv = pkgs.python313.withPackages (ps: [ ]);

        systemLibs = with pkgs; [
          cacert
          cairo
          dbus
          fontconfig
          freetype
          glib
          krb5
          libGL
          libxkbcommon
          stdenv.cc.cc.lib
          zlib
          zstd
        ];

        # X11 libraries
        x11Libs = with pkgs.xorg; [
          libX11
          libXinerama
          libXrender
          libxcb
          xcbutilimage
          xcbutilkeysyms
          xcbutilrenderutil
          xcbutilwm
        ];

        # Determine Qt libs set (Qt6 when available, otherwise Qt5)
        qtLibs = if builtins.hasAttr "libsForQt6" pkgs then pkgs.libsForQt6.qt6 else pkgs.libsForQt5.qt5;

        # All runtime libraries
        runtimeLibs = systemLibs ++ x11Libs ++ [ qtLibs.wrapQtAppsHook qtLibs.full ];

        # Development tools
        devTools = with pkgs; [
          act
          uv
        ];

        # Build inputs
        buildLibs = with pkgs; [
          dpkg
          glib
          libGL
          libxkbcommon
          pkg-config
          python313Packages.setuptools
        ];

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = devTools ++ buildLibs;
          # Environment variables
          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath runtimeLibs}:$LD_LIBRARY_PATH";
          # UV_PYTHON = "${pythonEnv}/bin/python";
          UV_PYTHON_PREFERENCE = "only-managed";

          shellHook = ''
            echo "🐍 Python ${pkgs.python313.version} development environment"
            echo "📦 Using uv for package management"
            export UV_PUBLISH_TOKEN="$(${pkgs.python313Packages.keyring}/bin/keyring get testpypi root-painter)"
            export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
          '';
        };

        # Legacy alias for compatibility
        devShell = self.outputs.${system}.devShells.default;
      });
}
