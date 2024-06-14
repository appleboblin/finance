{
    description = "Finance application project in python, node required for database editing";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
        devenv.url = "github:cachix/devenv";
    };

    outputs = inputs @ { flake-parts, nixpkgs, ... }:
        flake-parts.lib.mkFlake { inherit inputs; } {
        imports = [ inputs.devenv.flakeModule ];
        systems = nixpkgs.lib.systems.flakeExposed;

        perSystem = { config, self', inputs', pkgs, system, ... }: {
            devenv.shells.default = {
            packages = with pkgs; [
                nodejs_20
                nodePackages.npm
                sqlite
            ];

            dotenv.disableHint = true;
            languages.javascript.enable = true;
            languages.python = {
                enable = true;
                package = pkgs.python3.withPackages (ps: with ps; [
                flake8
                black
                tkinter
                ]);
                venv.enable = true;
            };
            };
        };
    };
}
