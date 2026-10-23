client = require("libqwenclient")
json = require("user.qwenclient.json")
require("user.qwenclient.utils")

-- Function to read content from a file
local function read_file(filename)
	local file = io.open(filename, "r")
	if not file then
		print("Error opening file:", filename)
		return nil
	end
	local content = file:read("*all")
	file:close()
	return content
end

-- Read SERVER_ADDR from a file
local home_folder = os.getenv("HOME")
local server_addr_file = home_folder.."/.config/nvim/lua/user/qwenclient/server_address.txt"
SERVER_ADDR = strip_newlines(read_file(server_addr_file))

if SERVER_ADDR == nil then
	print("Failed to read SERVER_ADDR from file.")
	return
end

function get_server_response(mode, payload)
	if type(payload) ~= "table" then
		print("error: payload must be table")
		return
	end

	local payload_str = json.encode(payload)
	local response = client.process(payload_str, mode, SERVER_ADDR)

	if (check_error(output)) then
		return -1
	end

	return json.decode(response)["response"]
end
