from openai_harmony import (
    Author,
    Conversation,
    DeveloperContent,
    HarmonyEncodingName,
    Message,
    Role,
    SystemContent,
    ToolDescription,
    load_harmony_encoding,
    ReasoningEffort
)

encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)

system_message = (
    SystemContent.new()
        .with_model_identity(
            "You are ChatGPT, a large language model trained by OpenAI."
        )
        .with_reasoning_effort(ReasoningEffort.MEDIUM)
        .with_conversation_start_date("2025-08-17")
        .with_knowledge_cutoff("2024-06")
        .with_required_channels(["analysis", "commentary", "final"])
)

# create a conversation
convo = Conversation.from_messages([
    Message.from_role_and_content(Role.SYSTEM, system_message),
    Message.from_role_and_content(Role.USER, "tell me a joke about cheese")
])

# tokens
tokens = encoding.render_conversation_for_completion(convo, Role.ASSISTANT)

# print the tokens
print(tokens) 