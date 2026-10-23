from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import LogitsProcessorList
from logits_processor import ConstrainedLogitsProcessor

SYSTEM_PROMPT = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."

model_name = "unsloth/Qwen2.5-Coder-3B-Instruct-bnb-4bit"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

def unconstrained_inference(context, max_new_tokens=1024):
    text = tokenizer.apply_chat_template(
        context,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    prompt_len = model_inputs.input_ids.shape[1] - 1 # Hack to fix constraint starting 1 step too late

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def inference(context, fsm, max_new_tokens=1024):
    text = tokenizer.apply_chat_template(
        context,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    prompt_len = model_inputs.input_ids.shape[1] - 1 # Hack to fix constraint starting 1 step too late

    constraint_processor = ConstrainedLogitsProcessor(fsm, tokenizer, trigger_sequence_len=prompt_len)
    logits_processor_list = LogitsProcessorList([constraint_processor])

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        logits_processor = logits_processor_list
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

#if __name__ == "__main__":
#    print(code("Write a Python function to get all prime numbers below a specified value 'x'"))
