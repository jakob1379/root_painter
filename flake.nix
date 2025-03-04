{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs =
    {
      self,
      nixpkgs,
      utils,
    }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
        {
          devShell = pkgs.mkShell {
            buildInputs = with pkgs; [
              uv
              pkg-config
              (python313Packages.matplotlib.override { enableQt = true; })
              libsForQt5.qt5.qtwayland
              libsForQt5.qt5.qtbase
              libsForQt5.qt5.qtx11extras
              libxkbcommon
              zlib
              libGL
              python310Packages.setuptools
              glib
              stdenv.cc.cc.lib
            ];

            LD_LIBRARY_PATH = "${
              pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc.lib
                pkgs.xorg.libX11
                pkgs.xorg.libXrender
                pkgs.libGL
                pkgs.glib
                pkgs.zlib
                pkgs.libsForQt5.qt5.qtwayland
                pkgs.libxkbcommon
              ]
            }:$LD_LIBRARY_PATH";

            QT_QPA_PLATFORM = "xcb";
            
          };
        }
    );

}
