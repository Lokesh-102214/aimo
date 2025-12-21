# Using the Hugging Face Transformers Backend (Recommended First Step) 

# Many custom models fine-tuned from existing architectures can be run in vLLM with no code changes by leveraging the built-in Transformers backend. 

# -   **Prerequisite:** Your model must be structured like a standard Hugging Face model, with a `config.json` file in its directory that properly maps to its architecture via `auto_map`.
# -   **How to use:** Simply pass the local path to your model directory when initializing the `LLM` object. 

# Example directory structure for a custom fine-tuned model:
# my_custom_model/
# ├── config.json           # Defines architecture & hyperparams
# ├── tokenizer.json        # Tokenizer definition
# ├── tokenizer_config.json # Tokenizer settings (padding, EOS, etc.)
# └── model.safetensors     # Actual weights (recommended format)


# Install the vLLM library on your python environment
# !pip install vllm

# Import necessary libraries
from vllm import LLM, SamplingParams
    
model_dir = "/path/to/your/custom_model" # Use an absolute path
llm = LLM(model=model_dir)
    
# Define sampling parameters and prompt
sampling_params = SamplingParams(temperature=0.7, top_p=0.9, max_tokens=100)
prompt = "Your custom prompt here."
    
# Generate output
outputs = llm.generate(prompt, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
    

# If this works, no further steps are needed. If it fails or you need maximum performance, you must use a dedicated vLLM model implementation.