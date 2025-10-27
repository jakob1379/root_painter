{
  description = "RootPainter development shell providing Qt system dependencies";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        lib = pkgs.lib;
        runtimeLibs = with pkgs; [
          libGL
          libglvnd
          glib
          fontconfig
          freetype
          dbus
          xorg.libX11
          xorg.libXext
          xorg.libXfixes
          xorg.libXrender
          xorg.libXcursor
          xorg.libXi
          xorg.libXrandr
          xorg.libXinerama
          xorg.libSM
          xorg.libICE
          xorg.libxcb
          xorg.xcbutil
          xorg.xcbutilrenderutil
          xorg.xcbutilkeysyms
          xorg.xcbutilimage
          xorg.xcbutilwm
          xorg.xcbutilcursor
          libxkbcommon
          wayland
        ];
        tooling = with pkgs; [ uv pkg-config ];
      in {
        devShells.default = pkgs.mkShell {
          packages = runtimeLibs ++ tooling;
          env = {
            LD_LIBRARY_PATH = lib.makeLibraryPath runtimeLibs;
          };
        };
      }
    );
}
