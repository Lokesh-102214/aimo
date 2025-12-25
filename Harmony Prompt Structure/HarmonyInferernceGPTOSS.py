from transformers import pipeline, AutoTokenizer

# Setup
model_id = "openai/gpt-oss-20b"
tokenizer = AutoTokenizer.from_pretrained(model_id)
pipe = pipeline("text-generation", model=model_id, torch_dtype="auto", device_map="auto")

# Prepare input
messages = [{"role": "user", "content": "tell me a joke about cheese"}]
chat_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Tokenize input
input_ids = tokenizer.encode(chat_input)
print("INPUT TOKENS")
print("-" * 40)
print(f"{'Token':<20} | {'ID':<10}")
print("-" * 40)
for token_id in input_ids:
    token = tokenizer.decode([token_id])
    print(f"{repr(token):<20} | {token_id:<10}")

# Generate
outputs = pipe(messages, max_new_tokens=1024, return_full_text=True)

# Get the full generated text with special tokens
full_generated = tokenizer.apply_chat_template(outputs[0]["generated_text"], tokenize=False)
# Extract just the new part (after the input)
assistant_part = full_generated[len(chat_input):]

# Tokenize output with special tokens
output_ids = tokenizer.encode(assistant_part, add_special_tokens=False)

print("\nOUTPUT TOKENS")
print("-" * 40)
print(f"{'Token':<20} | {'ID':<10}")
print("-" * 40)
for token_id in output_ids:
    token = tokenizer.decode([token_id])
    print(f"{repr(token):<20} | {token_id:<10}")
