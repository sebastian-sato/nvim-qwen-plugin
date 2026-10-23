import fsm

class TokenResolver():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    def __call__(self, text):     
        try:
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            if len(tokens) == 1:
               return tokens[0]
            else:
               #print("Warning: Can only operate on single tokens")
               return None
        except Exception as e:
            #print(f"Error encoding '{text}': {e}")
            return None

def init_yn_fsm(tokenizer, allow_uncertain=False):
    '''
    This FSM constrains the output to be either "Yes" or "No" and, optionally, "Unsure"
    '''
    tokenize = TokenResolver(tokenizer)

    WILDCARD = fsm.WILDCARD
    EOS = tokenizer.eos_token
    YES = tokenize("Yes")
    NO = tokenize("No")
    UNSURE = tokenize("Unsure")

    reg = fsm.FSM()
    reg.add_transition(0, 1, YES)
    reg.add_transition(0, 1, NO)
    if allow_uncertain:
        reg.add_transition(0, 1, UNSURE)
    reg.add_transition(1, 2, EOS)

def init_decision_fsm(tokenizer, options):
    options[-1] = options[-1].replace("?","")
    tokenize = TokenResolver(tokenizer)

    WILDCARD = fsm.WILDCARD
    EOS = tokenize(tokenizer.eos_token)
    SPACE = tokenize(' ')

    reg = fsm.FSM()

    state_n = 1
    for option in options:
        # Tokenize
        tokens = []
        
        for word in option.lower().split(" "):
            tokens.append(tokenize(word))
            tokens.append(SPACE)

        # Create FSM path
        reg.add_transition(0, state_n, tokens[0])
        for t in tokens[1:]:
            reg.add_transition(state_n, state_n+1, t)
            state_n += 1
        reg.add_transition(state_n, -1, EOS)
        state_n += 2

    return reg

def init_code_fsm(tokenizer):
    '''
    This FSM forces the model to only output code surrounded by ```, without any commentary or anything.
    '''
    tokenize = TokenResolver(tokenizer)

    WILDCARD = fsm.WILDCARD
    EOS = tokenize(tokenizer.eos_token)
    CODE = tokenize("```")
    TICK = tokenize("`")
    DOUBLETICK = tokenize("``")

    reg = fsm.FSM()
    reg.add_transition(0, 1, CODE)
    reg.add_transition(1, 1, WILDCARD)
    reg.add_transition(1, 2, CODE)
    reg.add_transition(2, 3, EOS)

    reg.add_transition(1, 8, DOUBLETICK)
    reg.add_transition(8, 9, TICK)
    reg.add_transition(9, 10, EOS)

    reg.add_transition(1,4, TICK)
    reg.add_transition(4,1, WILDCARD)

    reg.add_transition(4, 11, DOUBLETICK)
    reg.add_transition(11, 12, EOS)

    reg.add_transition(4,5, TICK)
    reg.add_transition(5,1, WILDCARD)

    reg.add_transition(5, 6, TICK)
    reg.add_transition(6, 7, EOS)

    return reg

'''def init_fsm(tokenizer):
    # Tokens to be used in the regular language
    SPACE = get_token_id(" ", tokenizer)
    NEWLINE = get_token_id("\n", tokenizer)
    TAB = get_token_id("\t", tokenizer)
    RUN = get_token_id("run", tokenizer)
    COMMANDS = get_token_id("commands", tokenizer)
    SCRIPT = get_token_id("script", tokenizer)
    CREATE = get_token_id("create", tokenizer)
    DIRECTORIES = get_token_id("directories", tokenizer)
    WRITE = get_token_id("write", tokenizer)
    TO = get_token_id("to", tokenizer)
    FILE = get_token_id("file", tokenizer)
    CODE = get_token_id("```", tokenizer)
    PLAINTEXT = get_token_id("plaintext", tokenizer)
    BASH = get_token_id("bash", tokenizer)
    SLASH = get_token_id("/", tokenizer)
    DONE = get_token_id("done", tokenizer)
    #START_OF_MODEL_TURN = get_token_id()
    
    WILDCARD = "WILDCARD"#-999
    EOS = tokenizer.eos_token

    # FSM initialization
    reg = fsm.FSM()
    #reg.add_transition(0, -1, START_OF_MODEL_TURN)
    reg.add_transition(0, 27, RUN)
    reg.add_transition(27, 1, SPACE)
    reg.add_transition(1, 2, COMMANDS)
    reg.add_transition(2, 3, NEWLINE)
   
    reg.add_transition(3, 4, RUN)
    reg.add_transition(4, 28, SPACE)
    reg.add_transition(28, 5, SCRIPT)
    reg.add_transition(5, 6, NEWLINE)
    reg.add_transition(6, 7, CODE)
    reg.add_transition(7, 9, BASH)
    reg.add_transition(9, 9, WILDCARD)
    reg.add_transition(9, 10, CODE) # Hopefully opening and ending ``` are considered the same token? Will probably want to test that
                                    # or change it to make explicit start of script and end of script tags
    reg.add_transition(10, 11, NEWLINE)
    reg.add_transition(11, 25, DONE)

    reg.add_transition(3, 12, WRITE)
    reg.add_transition(12, 29, SPACE)
    reg.add_transition(29, 30, TO)
    reg.add_transition(30, 13, SPACE)
    reg.add_transition(13, 14, FILE)

    reg.add_transition(14, 32, SPACE)
    reg.add_transition(32, 33, SLASH)
    reg.add_transition(33, 33, WILDCARD)
    reg.add_transition(33, 15, NEWLINE)

    reg.add_transition(15, 16, CODE)
    reg.add_transition(16, 16, WILDCARD)
    reg.add_transition(16, 17, CODE)
    reg.add_transition(17, 18, NEWLINE)
    reg.add_transition(18, 25, DONE)
    
    reg.add_transition(3, 31, CREATE)
    reg.add_transition(31, 19, SPACE)
    reg.add_transition(19, 20, DIRECTORIES)
    reg.add_transition(20, 21, NEWLINE)
    reg.add_transition(21, 22, TAB)
    reg.add_transition(22, 23, SLASH)
    reg.add_transition(23, 23, WILDCARD)
    reg.add_transition(23, 21, NEWLINE)
    reg.add_transition(21, 23, SLASH)
    reg.add_transition(21, 24, NEWLINE)
    reg.add_transition(24, 25, DONE)

    reg.add_transition(25, 26, EOS)

    return reg'''
