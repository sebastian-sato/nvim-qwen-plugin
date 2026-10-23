# NVIM Qwen Plugin

After making that incredibly simplistic "software scaffolsing LLM", I wanted to try my hand at making something a little more useful. This is an implementation of a coding assistant for Neovim that, while still incredibly rudimentary (no agentic/autonomous code editing, no multi-file context, etc.), is a major step up from my previous attempt at the idea. 

I've found it to be somewhat useful for my own work since I'm not particularly inclined to pay for a subscription to a model provider. I still don't think anyone else would want to use this since it's still incredibly limited in its capabilities compared to the plethora of open source options available, but it was fun to make :)

**Client installation instructions**
Simply clone the repo, go into `client` and run `bash ./install.sh` and the neccessary files in your nvim configuration will automatically be created. 

**Setup**
1. Once installed, open neovim, press ':' and type 'Qwen', then press Tab.
2. You should see several options appear, choose QwenSetHTTPServerURL, and press enter.
3. Finally, type in a URL of the format: ```http://<server-ip>/server```, replacing <server-ip> with the IP of the machine running the local LLM server contained within this repository (instructions for setting that up will come next)
4. Available commands are Qwen, QwenChat, QwenChatNSC, QwenChatClear, QwenChatShow, QwenInsert, and QwenEdit
   - **Qwen** and **QwenEdit**: these are aliases of each other, this is for general usage. Tell Qwen what changes you want it to make to the file and it will do it (or try to do it anyways)
   - **QwenChat**: Chat with Qwen without making changes to your code, your current code will be given to it as context.
   - **QwenChatNSC**: Same as QwenChat but only your message is given to Qwen, your code is kept hidden, good for asking general questions.
   - **QwenChatClear**: Takes no arguments, resets the chat history. Memory errors should automatically be handled on the server side, so you shouldn't *need* to use this, but it can still be useful if Qwen is misbehaving or getting confused because of previous context.
   - **QwenInsert**: Will insert the requested code directly at your cursor location, very rudimentary and currently takes no context from chat history or the surrounding code. Good for writing individual functions or code snippets.

For the most part, **Qwen** and maybe **QwenChat** would probably be the only commands you'd need to use on a regular basis.

**Server installation instructions**
On your LLM capable hardware, clone the repo and this time go into `server` and run `run.sh`.

This will automatically install the needed dependencies upon first execution.

On linux, you can use ```hostname -I``` to get the local IP you need to connect to. If you're not on the same network as the server, you'll need to use a VPN like Tailscale, or use port forwarding (not recommended if the server is publicly hosted, since there is currently no authentication mechanism, that's on the TODO list :P)

**NOTE:**
If you're running the client on the same machine as the server, connect to the server from neovim using ```QwenSetHTTPServerURL http://localhost/server``` instead of the ip.
