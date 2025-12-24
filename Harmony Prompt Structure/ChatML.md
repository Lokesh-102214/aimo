
# ChatML (Chat Markup Language)

**ChatML**is a structured message exchange format developed by OpenAI to standardize conversations with large language models (LLMs). It helps models understand who is speaking (e.g., system, user, assistant) and the boundaries between messages, which improves consistency, steerability, and security. 

## How ChatML Works ?

Instead of sending a single, unstructured text prompt, developers format the input as a list of message objects. Each object specifies a `role` and `content`: 

```json
    [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"},
      {"role": "assistant", "content": "The capital of France is Paris."}
    ]
```

When sent to the model, this structured data is converted into a token sequence using special tokens (like `<|im_start|>` and `<|im_end|>`) to explicitly mark message boundaries and roles. 
## Example
## ChatML Example Code

Below is a ChatML example JSON file with the roles defined of `system`, `user` and `assistant`.

```json
[{"role": "system",  
"content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\\nKnowledge cutoff: 2021-09-01\\nCurrent date: 2023-03-02"},  
{"role": "user",  
"content" : "How are you?"},  
{"role": "assistant",  
"content" : "I am doing well"},  
{"role": "user",  
"content" : "What is the mission of the company OpenAI?"}]
```
And the working Python code snippet:
```python
pip install openai  
  
import os  
import openai  
openai.api\_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  
  
completion = openai.ChatCompletion.create(  
  model="gpt-3.5-turbo",   
  messages = \[{"role": "system", "content" : "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\\nKnowledge cutoff: 2021-09-01\\nCurrent date: 2023-03-02"},  
{"role": "user", "content" : "How are you?"},  
{"role": "assistant", "content" : "I am doing well"},  
{"role": "user", "content" : "What is the mission of the company OpenAI?"}\]  
)  
#print(completion)  
print(completion)
```
With the output below, notice the role which is defined, the model detail which is `gpt-3.5-turbo-0301` and other detail.
```json
{  
  "choices": [  
    {  
      "finish_reason": "stop",  
      "index": 0,  
      "message": {  
        "content": "The mission of OpenAI is to ensure that artificial intelligence (AI) benefits humanity as a whole, by developing and promoting friendly AI for everyone, researching and mitigating risks associated with AI, and helping shape the policy and discourse around AI.",  
        "role": "assistant"  
      }  
    }  
  ],  
  "created": 1677751157,  
  "id": "chatcmpl-6pa0TlU1OFiTKpSrTRBbiGYFIl0x3",  
  "model": "gpt-3.5-turbo-0301",  
  "object": "chat.completion",  
  "usage": {  
    "completion_tokens": 50,  
    "prompt_tokens": 84,  
    "total_tokens": 134  
  }  
}
```
## Key Roles 

-   **System**: Provides initial instructions and high-level context to guide the AI's overall behavior and personality.
-   **User**: Represents the human user's input, queries, or instructions.
-   **Assistant**: Represents the AI's responses within the conversation history.
-   **Tool**: Used for function calls and integrating external tools or data sources, enabling the AI to perform specific actions.

## Benefits 

-   **Improved Consistency**: Provides a deterministic input format, leading to more predictable and reliable model performance.
-   **Enhanced Control**: Allows developers to clearly define system behavior and conversation flow, transforming prompting into a more precise engineering discipline.
-   **Prompt Injection Mitigation**: By separating user input from system instructions with explicit boundaries, ChatML helps protect against prompt injection attacks, where malicious prompts might override the original system rules.

## Ref : [ChatMl Article by Cobus Greyling](https://cobusgreyling.medium.com/the-introduction-of-chat-markup-language-chatml-is-important-for-a-number-of-reasons-5061f6fe2a85)