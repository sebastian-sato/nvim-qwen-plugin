import llm
from constraints import *

persistent_context = [{"role":"system","content":llm.SYSTEM_PROMPT}]

def chat(payload):
    prompt = payload["prompt"]
    if "code" in payload:
        #print("###\n\nCODE IN PAYLOAD\n\n###")
        code = payload["code"]
        full_prompt = "```\n{}\n```\n\n{}".format(code, prompt)
    else:
        #print("###\n\nCODE NOT IN PAYLOAD\n\n###")
        full_prompt = prompt
    done = False
    persistent_context.append({"role":"user","content":full_prompt})
    attempts = 0
    while not done:
        try:
            response_text = llm.unconstrained_inference(persistent_context)
            done = True
        except:
            #persistent_context = [persistent_context[0]] + persistent_context[-2:]
            del(persistent_context[1])
            del(persistent_context[1])
            attempts += 1
            if attempts > 4:
                reset_context()
                return "out of memory error, flushing context"
    persistent_context.append({"role":"assistant","content":response_text})
    return response_text

def reset_context():
    #print("###\n\nCHAT RESET\n\n###")
    global persistent_context
    persistent_context = [{"role":"system","content":llm.SYSTEM_PROMPT}]

def impl_code(prompt, context=None):
    context = construct_context(prompt, context)
    return '\n'.join(llm.inference(context, init_code_fsm(llm.tokenizer)).replace("```","").strip().split("# Example usage")[0].split('\n')[1:])

def make_decision(example, query, options, context=None):
    prompt = "```\n{}\n```\n\n{}\n\n**Options:**\n{}".format(example, query, '- '+'\n- '.join(options))
    # DEBUG
    #print("Decision prompt:",prompt)
    context = construct_context(prompt, context)
    # DEBUG
    #print("Decision context:",context)
    return llm.inference(context, init_decision_fsm(llm.tokenizer, options))

def edit_code(payload):
    code = payload["code"]
    instruction = payload["prompt"]
    prompt = "```\n{}\n``` Edit the code to meet the given specifications: \n\n\"{}\"".format(code, instruction)
    edited_code = impl_code(prompt)
    # DEBUG
    
    def within_10_and_bigger_than_40(a, b):
        if a > 40 and b > 40:
            if abs(a - b) < 10:
                return True
        elif a > 10 and b > 10 and abs(a - b) < 3:
            return True
        return False

    if within_10_and_bigger_than_40(len(edited_code.split('\n')), len(code.split('\n'))):
        return edited_code
    else:
        #print("Edited code:",edited_code)
        context = [{"role":"user","content":prompt},{"role":"assistant","content":edited_code}]
        d = make_decision(edited_code, "Is this a code snippet or the full program? Answer \"code snippet\" if you supplied a code snippet that needs to be reinserted back into the main program, and \"full program\" if I can use the code you have provided directly as is.", [
            "code snippet",
            "full program"
        ])
        # DEBUG
        #print("Selected option:",d)
        
        if "full program" in d:
            return edited_code
        elif "code snippet" in d:
            return impl_code("This is an incomplete code snippet, please rewrite as the whole program, incorporating the requested change.", context)
            
        return "placeholdertext lorum ipsum"

def construct_context(prompt, context):
    if context == None:
        context = _construct_one_shot_context(prompt)
    else:
        if context[-1]["role"] == "user":
            raise Exception("can't have last entry be user response when making decision with context")
        context = context.append({"role":"user","content":prompt})
    return context

def _construct_one_shot_context(prompt):
    context = [
            {"role":"system", "content":llm.SYSTEM_PROMPT},
            {"role":"user", "content":prompt}
    ]
    return context


#def handle_decision(payload): # This should probably be brought into its own module since it may need to be used internally
#    payload_as_dict = eval(payload) # Horrible idea to blindly evaluate client defined text, but who am I to judge
#    data = payload_as_dict["data"]
#    query = payload_as_dict["query"]
#    decision_options = payload_as_dict["options"]
#    llm.decide(data, query, decision_options)

