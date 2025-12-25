## Harmony Prompt Format
The **Harmony prompt format** is a structured messaging protocol used specifically with OpenAI's `gpt-oss` open-weight models to standardize how conversations, reasoning, and tool calls are handled. It uses special tokens and roles to provide fine-grained control over the model's output. 

## Key Components of the Harmony Format 

The format uses control tokens like `<|start|>`, `<|end|>`, and `<|message|>` to delineate different parts of a conversation. Key components include: 

### Roles:
 The format defines explicit roles for different participants in the interaction, with a clear hierarchy for resolving instructional conflicts.
-   `system`: Provides general, immutable metadata about the model (e.g., knowledge cutoff date, identity).
-   `developer`: This acts as the primary "system prompt," containing specific instructions, constraints, and tool definitions for the current task. These instructions take priority over the `system` message.
-   `user`: The user's input or question.
-   `assistant`: The model's response.
### Channels

 The assistant's output can be separated into different channels for different purposes, offering transparency into its process.
-   `analysis`: Contains the model's internal chain-of-thought reasoning, which is typically hidden from the end-user.
-   `commentary`: Used for preambles and formatting related to tool or function calls.
-   `final`: The user-facing response, which is the only part displayed to the user. 
### Special tokens (how turns are framed)

Harmony introduces a small set of structural tokens that act as markers:

-   `<|start|> … <|message|> … <|end|>` – a complete message envelope
-   `<|channel|>` – sets the channel for a message
-   `<|constrain|>` – declares the tool argument type (commonly `json`)
-   `<|call|>` – **stop now** and run the tool you just saw
-   `<|return|>` – **stop now**, the assistant’s turn is finished

### The key idea

**Message boundaries are not the same as turn boundaries.**  
A single assistant turn may contain several messages: some `analysis`, maybe a `commentary` plan, then either a `call` or a `return`. `<|end|>` simply means “this message is finished.” `<|call|>` or `<|return|>` tell your runtime how to handle the end of the _turn_.

This format enables better multi-turn use cases, which are important for long-running agentic tasks (such as coding).

## Diagram
![Harmony Prompt Diagram](1_SV1lUHidhpMqQUxGj5JJKQ.png)
[Source](https://www.google.com/url?sa=i&url=https%3A%2F%2Fai.plainenglish.io%2Fgpt-oss-wont-work-without-this-harmony-guide-c35c070c217b&psig=AOvVaw3adpBkxT742P5uCiFVR2QB&ust=1766734465103000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCKCGv_6c2JEDFQAAAAAdAAAAABAE)
## Example of a Harmony Formatted Prompt 

A raw Harmony-formatted prompt for training or fine-tuning might look like this, ensuring the model understands the context and expected output style: 

You can find an example of a Harmony formatted prompt for fine-tuning on a dermatology dataset, including developer and user messages with specific instructions, at [firecrawl.dev](https://www.firecrawl.dev/blog/fine_tune_openai_gpt_oss). 

How to Use It 

-   **For developers:** Building inference solutions requires using tools like the `openai-harmony` library to correctly format inputs and parse outputs according to the expected token structure. You can find implementation guidance in the [OpenAI Cookbook](https://cookbook.openai.com/articles/openai-harmony).
-   **For general users:** When using platforms like Hugging Face or Ollama, the underlying system usually handles the Harmony formatting automatically. This allows users to interact using standard chat message inputs without needing to manage the specific tokens.

Ref : [OpenAI Hidden Formatting: Harmony vs. ChatML by Minhajul Hoque](https://medium.com/data-science-collective/openai-secret-formatting-harmony-vs-chatml-e9a893396e53)

Video Explanation : [GPT‑OSS Harmony Prompt Format Explained by 
Chris Hay](https://www.youtube.com/watch?v=g8P7oiZkR_w)