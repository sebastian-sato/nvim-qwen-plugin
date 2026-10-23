require("user.qwenclient.client")

chat_last = ""

function qinsert(opts)
	local payload = {
		["prompt"] = opts.fargs[1]
	}
	local response = get_server_response("impl_code", payload)
	local lines = split_newlines(response)
	vim.api.nvim_put(lines, "l", false, true)
end

function qedit(opts)
	local payload = {
		["code"] = join_lines(vim.api.nvim_buf_get_lines(0, 0, -1, false)),
		["prompt"] = opts.fargs[1]
	}
	local response = get_server_response("edit_code", payload)
	local lines = split_newlines(response)
	vim.api.nvim_buf_set_lines(0, 0, -1, false, lines)
end

vim.api.nvim_create_user_command(
	"QwenInsert",
	qinsert,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"QwenEdit",
	qedit,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"Qwen",
	function(opts)
		local num_lines = 0
		local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)
		for k, v in pairs(lines) do
			if not all_whitespace(v) then
				qedit(opts)
				goto done_lbl
			else
				qinsert(opts)
				goto done_lbl
			end
		end
		::done_lbl::
	end,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"QwenChat",
	function(opts)
		local payload = {
			["code"] = join_lines(vim.api.nvim_buf_get_lines(0, 0, -1, false)),
			["prompt"] = opts.fargs[1]
		}
		local response = get_server_response("chat", payload)
		print(response)
		chat_last = response
	end,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"QwenChatShareCode",
	function(opts)
		local payload = {
			["code"] = join_lines(vim.api.nvim_buf_get_lines(0, 0, -1, false)),
			["prompt"] = opts.fargs[1]
		}
		local response = get_server_response("chat", payload)
		print(response)
		chat_last = response
	end,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"QwenChatNoShareCode",
	function(opts)
		local payload = {
			["prompt"] = opts.fargs[1]
		}
		local response = get_server_response("chat", payload)
		print(response)
		chat_last = response
	end,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"QwenChatNSC",
	function(opts)
		local payload = {
			["prompt"] = opts.fargs[1]
		}
		local response = get_server_response("chat", payload)
		print(response)
		chat_last = response
	end,
	{ nargs = 1 }
)

vim.api.nvim_create_user_command(
	"QwenChatClear",
	function(opts)
		local payload = {
			["prompt"] = "n/a"
		}
		get_server_response("chat_reset", payload)
	end,
	{ nargs = 0 }
)

vim.api.nvim_create_user_command(
	"QwenChatShow",
	function(opts)
		print(chat_last)
	end,
	{ nargs = 0 }
)

vim.api.nvim_create_user_command(
	"QwenSetHTTPServerURL",
	function(opts)
		-- Get the first argument passed to the command
		local new_server_addr = opts.fargs[1]
		-- Construct the full path to the server address file
		local file_path = os.getenv("HOME") .. "/.config/nvim/lua/user/qwenclient/server_address.txt"
		-- Open the file in write mode
		local file = io.open(file_path, "w")
		if not file then
			print("Error: Unable to open file for writing:", file_path)
			return
		end
		-- Write the new server address to the file
		file:write(new_server_addr)
		-- Close the file
		file:close()
		-- Print confirmation message
		print("Server address updated successfully.")
	end,
	{ nargs = 1 }
)

