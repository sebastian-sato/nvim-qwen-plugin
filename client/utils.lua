function check_error(output)
	if type(output) == "string" then
		if output:sub(0,2) == "E:" then
			print(output:sub(0,-1))
			return true
		end
	end
	return false
end

--function split_newlines(str)
--  -- function for splitting on fake "\\n" newlines the server is sending me for some reason
--  -- NOTE: this problem was fixed
--	local n = string.byte("n")
--	local backslash = string.byte("\\")
--	local current_block = ""
--	local lines = {}
--	local backslash_inarow = 0
--	local backslash_append_queue = 0 -- Note: this should never be more than 1
--
--	local function handle_backslash_queue()
--		if (backslash_append_queue >= 1) then
--			current_block = current_block .. "\\"
--			backslash_append_queue = 0
--		end
--	end
--
--	for idx = 1, #str do
--		if str:byte(idx) == backslash then
--			handle_backslash_queue()
--			backslash_inarow = backslash_inarow + 1
--			backslash_append_queue = backslash_append_queue + 1
--		elseif str:byte(idx) == n then
--			if backslash_inarow % 2 == 0 then
--				-- not a newline
--				handle_backslash_queue()
--				current_block = current_block .. "n"
--				backslash_inarow = 0
--			else
--				-- newline
--				-- this is the situation where we DONT want to append the queued backslash
--				backslash_append_queue = 0
--				table.insert(lines, current_block)
--				current_block = ""
--				backslash_inarow = 0
--			end
--		else
--			-- any other character
--			handle_backslash_queue()
--			current_block = current_block .. str:sub(idx, idx)
--			backslash_inarow = 0
--		end
--	end
--
--	return lines
--end

function split_newlines(str)
	local result = {};
	for line in string.gmatch(str .. "\n", "(.-)\n") do
		table.insert(result, line);
	end
	return result
end

function join_lines(line_table)
	local output_string = ""
	local idx = 1
	while line_table[idx] ~= nil do
		output_string = output_string .. "\n" .. line_table[idx]
		idx = idx + 1
	end
	return output_string
end

function all_whitespace(line) 
	local all_whitespace = true
	for idx = 1, #line do
		local char = line:sub(idx, idx)
		if char == " " or char == "\n" or char == "\t" then
			goto continue
		end
		all_whitespace = false
		::continue::
	end
	return all_whitespace
end

function strip_newlines(input_string)
    return input_string:gsub("\n", "")
end
