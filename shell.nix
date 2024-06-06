{ pkgs ? import <nixpkgs> { } }:
with pkgs;
mkShell {
    buildInputs = [
        (python312.withPackages (pythonPkgs: with pythonPkgs; [
            tkinter
        ]))
    ];
    
    # Workaround: make vscode's python extension read the .venv
    shellHook = ''
        venv="$(cd $(dirname $(which python)); cd ..; pwd)"
        ln -Tsf "$venv" .venv
    '';
}
