## vLLM

vLLM (Virtual Large Language Model) is
an open-source library and high-performance inference and serving engine designed to make running large language models (LLMs) faster, more efficient, and better suited for production environments. It achieves this by optimizing GPU memory usage and maximizing the number of tokens processed per second (throughput) through innovative techniques, most notably **PagedAttention**. 

## How vLLM Works: Key Innovations 

The primary challenge in serving LLMs is efficiently managing the **KV cache** (Key-Value cache), which stores the short-term memory of a model during text generation and can consume significant GPU memory, leading to fragmentation and slow performance. 

### vLLM addresses this using several techniques: 

-   **PagedAttention Algorithm**: This is vLLM's core innovation, inspired by the virtual memory and paging systems in operating systems. It breaks the continuous KV cache into fixed-size "blocks" that can be stored in non-contiguous physical GPU memory. This eliminates memory fragmentation and allows for more efficient memory sharing, resulting in up to 24 times higher throughput than traditional methods.
-   **Continuous Batching (Dynamic Batching)**: Traditional systems wait for an entire batch of requests to finish before starting new ones, which leads to idle GPU time. vLLM uses continuous batching, which dynamically adds new requests to the GPU as soon as previous ones complete their token generation, keeping the GPU consistently busy and reducing latency.
-   **Optimized CUDA Kernels**: vLLM incorporates highly optimized code for the GPU, including integrations with libraries like FlashAttention and FlashInfer, to ensure maximum performance for specific hardware.
-   **Automatic Prefix Caching and Copy-on-Write**: For requests that share a common prompt prefix (like shared system prompts), vLLM reuses the already computed KV cache blocks, reducing redundant computation. The "copy-on-write" mechanism efficiently handles cases where sequences diverge. 

## Benefits of Using vLLM 

-   **Faster Response Times**: By maximizing efficiency, vLLM significantly reduces the time it takes to get the first and subsequent tokens.
-   **Cost Efficiency**: Better use of existing hardware means fewer GPUs are needed to handle high-volume workloads, which lowers operational costs.
-   **Scalability**: The architecture supports seamless scaling from a single GPU to distributed, multi-node deployments with minimal code changes.
-   **Ease of Use**: It provides a user-friendly Python interface and an OpenAI-compatible API server for easy integration into existing applications.

## Example directory structure for a custom fine-tuned model:
```python
my_custom_model/
├── config.json           # Defines architecture & hyperparams
├── tokenizer.json        # Tokenizer definition
├── tokenizer_config.json # Tokenizer settings (padding, EOS, etc.)
└── model.safetensors     # Actual weights (recommended format)
```

## Reference and Explanation Video 
[vLLM : Easily Deploying & Serving LLMs](https://www.youtube.com/watch?v=q5IF2PHA5SA)