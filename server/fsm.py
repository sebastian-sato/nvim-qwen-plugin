WILDCARD = -999

class FSM():
    def __init__(self):
        self.transitions = {0:{}}
        self.initial_state = 0
        self.current_state = self.initial_state

    def add_transition(self, state_a, state_b, transition_value):
        '''
        state_a is an already existing state
        state_b can be an already existing state, or a new state
        '''
        try:
            self.transitions[state_a][transition_value] = state_b
        except KeyError:
            self.transitions[state_a] = {}
            self.transitions[state_a][transition_value] = state_b

    def run(self, value):
        try:
            new_state = self.transitions[self.current_state][value]
            self.current_state = new_state
            #print("Advanced to state",self.current_state)
            return self.current_state
        except KeyError:
            # Check if there is a wildcard transition, and if so, take that transition
            for v in self.transitions[self.current_state]:
                if v == WILDCARD:
                    new_state = self.transitions[self.current_state][WILDCARD]
                    self.current_state = new_state
                    #print("Wildcard, advanced to state",self.current_state)
                    return self.current_state
            # Otherwise, return nothing
            #print("Invalid transition",'"'+str(value)+'"')
            return None

    def reset(self):
        self.current_state = self.initial_state

    def get_available_transitions(self):
        try:
            available_transitions = list(self.transitions[self.current_state].keys())
            for transition in available_transitions:
                if transition == WILDCARD:
                    return [WILDCARD]
            return available_transitions
        except KeyError:
            return []
