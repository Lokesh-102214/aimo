# Install the vLLM library on your python environment
# !pip install vllm
# Import necessary libraries
from vllm import LLM, SamplingParams

# Name Copied from huggingface models : meta-llama/Llama-2-7b-hf
# gpu_memory_utilization is set to 0.8 to utilize 80% of GPU memory to not use full local GPU memory
llm = LLM("meta-llama/Llama-2-7b-hf" , gpu_memory_utilization=0.8)

# Set sampling parameters for text generation
#'temperature' : Temperature controls the randomness of predictions by scaling the logits before applying softmax.
# 'max_tokens' : Maximum number of tokens to generate in the output.
params = SamplingParams(temperature=0.7, max_tokens=256)

# Input prompt for text generation
prompt = "Once upon a time in a land far, far away,"

# Generate text based on the input prompt and sampling parameters
outputs = llm.generate([prompt], params)

# Print the generated text output
print(outputs[0].outputs[0].text)



