{
    description = "Finance application project in python, node required for database editing";

    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
    };

    outputs = { self , nixpkgs ,... }: let
        system = "x86_64-linux";
        # system = "x86_64-darwin";
    in {
        devShells."${system}".default = let
        pkgs = import nixpkgs {
            inherit system;
        };
        in pkgs.mkShell {
            # create an environment with both Node.js and Python
            packages = with pkgs; [
            nodejs_20
            nodePackages.npm
            sqlite
            (python312.withPackages (pythonPkgs: with pythonPkgs; [
                tkinter
            ]))
            ];

            shellHook = ''
            echo "node `${pkgs.nodejs}/bin/node --version`"
            venv="$(cd $(dirname $(which python)); cd ..; pwd)"
            ln -Tsf "$venv" .venv
        '';
        };
    };
}