vLLM (Virtual Large Language Model) is a high-throughput, memory-efficient open-source library designed for fast inference and serving of Large Language Models (LLMs). Originally developed at UC Berkeley's Sky Computing Lab, it is now a hosted project under the PyTorch Foundation as of May 2025


Example directory structure for a custom fine-tuned model:
my_custom_model/
├── config.json           # Defines architecture & hyperparams
├── tokenizer.json        # Tokenizer definition
├── tokenizer_config.json # Tokenizer settings (padding, EOS, etc.)
└── model.safetensors     # Actual weights (recommended format)