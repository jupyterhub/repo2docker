let
  # Pinning nixpkgs to specific release
  # To get sha256 use "nix-prefetch-git <url> --rev <commit>"
  commitRev="5574b6a152b1b3ae5f93ba37c4ffd1981f62bf5a";
  nixpkgs = builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/${commitRev}.tar.gz";
    sha256 = "1pqdddp4aiz726c7qs1dwyfzixi14shp0mbzi1jhapl9hrajfsjg";
  };
  pkgs = import nixpkgs { config = { allowUnfree = true; }; };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python36Packages.notebook
  ];

  shellHook = ''
    export NIX_PATH="nixpkgs=${nixpkgs}:."
  '';
}
