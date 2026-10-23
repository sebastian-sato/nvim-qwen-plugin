import actions

def execute_request(query_type, payload):
    print(query_type)
    if query_type == "impl_code":
        return actions.impl_code(payload["prompt"])
    if query_type == "decide":
        return actions.make_decision(payload)
    if query_type == "edit_code":
        return actions.edit_code(payload)
    if query_type == "chat":
        return actions.chat(payload)
    if query_type == "chat_reset":
        return actions.reset_context()
