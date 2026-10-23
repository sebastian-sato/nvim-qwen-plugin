from transformers import LogitsProcessor
import torch
import fsm

# Defined constrained LogitsProcessor (from github.com/colesmcintosh/logit-control)
class ConstrainedLogitsProcessor(LogitsProcessor):
    def __init__(self, fsm, tokenizer, trigger_sequence_len):
        #assert isinstance(allowed_token_ids, list)
        #self.allowed_token_ids = allowed_token_ids
        self.tokenizer = tokenizer
        self.trigger_sequence_len = trigger_sequence_len
        self.original_logits = None
        self.modified_logits = None
        self.applied_constraint = False
        self.vocab_size = tokenizer.vocab_size
        self.fsm = fsm#fsm_initializer_func(tokenizer)#init_fsm(tokenizer)
        self.verbose = False

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        current_length = input_ids.shape[1]

        if current_length > self.trigger_sequence_len: #and not self.applied_constraint:
            # This seems to make it so it only applies the constraint once at the specific sequence (the start of generation)
            self.applied_constraint = True
            if self.verbose:
                pass#print(f"\n--- Applying constraint at step {current_length} ---")

            self.original_logits = scores[0].clone().cpu().numpy() # For visualization, not needed

            previous_token = int(input_ids[0, -1].clone().cpu().numpy()) # Print the previous token
            
            self.fsm.run(previous_token)
            allowed_tokens = self.fsm.get_available_transitions()

            if self.verbose:
                pass#print("Previous token:", self.tokenizer.decode(previous_token) )
                pass#print("Allowed tokens:", allowed_tokens)

            # If wildcard, don't do masking
            if fsm.WILDCARD not in allowed_tokens:
                mask = torch.full_like(scores, -float("Inf"))
                valid_allowed_ids = []
                for token_id in allowed_tokens:#self.allowed_token_ids:
                    if type(token_id) == str:
                        pass#print("WTF:",token_id)
                    if 0 <= token_id < self.vocab_size:
                        mask[:, token_id] = 0
                        valid_allowed_ids.append(token_id)
                    else:
                        if self.verbose:
                            pass#print(f"Warning: Allowed token ID {token_id} is out of vocab bounds ({self.vocab_size}). Skipping.")
            
                if not valid_allowed_ids:
                    if self.verbose:
                        pass#print("Warning: No valid allowed token IDs found. Constraint will not be applied effectively.")
                    return scores
            else:
                return scores

            scores = scores + mask

            self.modified_logits = scores[0].clone().cpu().numpy()

            allowed_tokens_str = ", ".join([f"'{self.tokenizer.decode([t])}' ({t})" for t in valid_allowed_ids])
            if self.verbose:
                pass#print(f"Constraining next token to: {allowed_tokens_str}")
        
        return scores

    def update_fsm(self, chosen_token):
        self.fsm.run(chosen_token)
