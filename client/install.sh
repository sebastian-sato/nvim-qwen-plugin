#!/bin/bash

# Check if Neovim is installed
if ! command -v nvim &> /dev/null && ! command -v vim &> /dev/null; then
    echo "Error: Neovim not installed"
    exit 1
fi

echo "Compiling shared library"
bash ./build.sh

echo "Creating directories"
mkdir -p ~/.config/nvim/
mkdir -p ~/.config/nvim/lua
mkdir -p ~/.config/nvim/lua/user
mkdir -p ~/.config/nvim/lua/user/qwenclient
touch ~/.config/nvim/lua/user/qwenclient/server_address.txt

echo "Copying to nvim config"
cp ./libqwenclient.so ~/.config/nvim/lua/
cp ./client.lua  ~/.config/nvim/lua/user/qwenclient/
cp ./init.lua ~/.config/nvim/lua/user/qwenclient/
cp ./json.lua ~/.config/nvim/lua/user/qwenclient/
cp ./utils.lua ~/.config/nvim/lua/user/qwenclient/

# Check if the line require("user.qwenclient") exists in init.lua
if ! grep -q 'require("user.qwenclient")' ~/.config/nvim/init.lua; then
    echo "" >> ~/.config/nvim/init.lua
    echo "------" >> ~/.config/nvim/init.lua
    echo "-- NVIM QWEN PLUGIN" >> ~/.config/nvim/init.lua
    echo "require(\"user.qwenclient\")" >> ~/.config/nvim/init.lua
    echo "------" >> ~/.config/nvim/init.lua
fi

echo "Done"
