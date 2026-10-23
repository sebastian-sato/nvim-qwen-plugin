#!/bin/bash

# Check if Neovim is installed
if ! command -v nvim &> /dev/null && ! command -v vim &> /dev/null; then
    echo "Error: Neovim not installed"
    exit 1
fi

# Check if the line require("user.qwenclient") exists in init.lua
if grep -q 'require("user.qwenclient")' ~/.config/nvim/init.lua; then
    # Remove the line require("user.qwenclient")
    sed -i '/-- NVIM QWEN PLUGIN/,/-- NVIM QWEN PLUGIN/d' ~/.config/nvim/init.lua
fi

# Delete the qwenclient directory and its contents
rm -rf ~/.config/nvim/lua/user/qwenclient

# Delete the libqwenclient shared library in the lua folder
rm ~/.config/nvim/lua/libqwenclient.so

echo "Qwen Neovim client has been uninstalled."
