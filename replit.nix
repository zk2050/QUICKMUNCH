{ pkgs }: {
  deps = [
    pkgs.sqlite.bin
    pkgs.nodePackages.vscode-langservers-extracted
    pkgs.nodePackages.typescript-language-server  
  ];
}