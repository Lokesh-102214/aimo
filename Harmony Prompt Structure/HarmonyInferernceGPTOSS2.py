import json
import torch
from openai_harmony import (
    HarmonyEncodingName,
    load_harmony_encoding,
    Conversation,
    Message,
    Role,
    SystemContent,
    DeveloperContent,
    ReasoningEffort
)
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load Harmony encoding
encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)

system_message = (
    SystemContent.new()
        .with_model_identity(
            "You are ChatGPT, a large language model trained by OpenAI."
        )
        .with_reasoning_effort(ReasoningEffort.LOW)
        .with_conversation_start_date("2025-08-17")
        .with_knowledge_cutoff("2024-06")
        .with_required_channels(["final"])
)

# developer_message = (
#     DeveloperContent.new()
#         .with_instructions("You are a pirate called jolly roger, you always speak in pirate speak.")
# )

# create a conversation
convo = Conversation.from_messages([
    Message.from_role_and_content(Role.SYSTEM, system_message),
    #Message.from_role_and_content(Role.DEVELOPER, developer_message),
    Message.from_role_and_content(Role.USER, "what is 223232*232322? DO NOT USE ANALYSIS.Just provide answer")
])

# Render prompt
prefill_ids = encoding.render_conversation_for_completion(convo, Role.ASSISTANT)
stop_token_ids = encoding.stop_tokens_for_assistant_actions()

# Display input tokens
print("INPUT TOKENS")
print("-" * 40)
print(f"{'Token':<20} | {'ID':<10}")
print("-" * 40)
for token_id in prefill_ids:
    token = encoding.decode([token_id])
    print(f"{repr(token):<20} | {token_id:<10}")

# Load model
model_name = "openai/gpt-oss-20b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

# Convert to tensor and move to model's device
device = next(model.parameters()).device
input_ids = torch.tensor([prefill_ids], device=device)

# Generate
outputs = model.generate(
    input_ids=input_ids,
    max_new_tokens=1024,
    eos_token_id=stop_token_ids
)

# Parse completion tokens
completion_ids = outputs[0][len(prefill_ids):].cpu().tolist()

# Display output tokens
print("\nOUTPUT TOKENS")
print("-" * 40)
print(f"{'Token':<20} | {'ID':<10}")
print("-" * 40)

# Stop at the first stop token for display
displayed_ids = []
for token_id in completion_ids:
    if token_id in stop_token_ids:
        displayed_ids.append(token_id)
        break
    displayed_ids.append(token_id)

for token_id in displayed_ids:
    token = encoding.decode([token_id])
    print(f"{repr(token):<20} | {token_id:<10}")

# Parse messages (exclude stop token)
parse_ids = [tid for tid in displayed_ids if tid not in stop_token_ids]

try:
    entries = encoding.parse_messages_from_completion_tokens(parse_ids, Role.ASSISTANT)
    
    print("\nPARSED MESSAGES:")
    print("-" * 40)
    for message in entries:
        print(json.dumps(message.to_dict(), indent=2))
        print("-" * 40)
except Exception as e:
    print(f"\nError parsing messages: {e}")
    print("\nRaw decoded output:")
    print(encoding.decode(parse_ids))