# vLLM can be deployed as a server that mimics the OpenAI API protocol, allowing it to serve as a drop-in replacement for existing applications.
# To localhost the model for inference using vLLM Install the vLLM library on your python environment
# !pip install vllm, then run the following command in your terminal to start the server:
#  first run this in terminal : vLLM serve --model <model_name> --apikey <your_api_key> --gpu_memory_utilization 0.9
#  then run this script to interact with the model
# For custom fine tuned model replace <model_name> with your model path and <your_api_key> with your desired API key.
# You can also get open ai type responses from the model using vLLM serve
#pip install openai

# Import the OpenAI library
from openai import OpenAI

# Initialize the OpenAI client to point to the local vLLM server
client = OpenAI(api_base="http://localhost:8000/v1", api_key="your_api_key")

# Define a prompt to send to the model
prompt = "Write a short story about a robot learning to love."

# Send a completion request to the local vLLM server
response = client.chat.completions.create(
    model="your_model_name",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=200,
    temperature=0.7
) 

# Print the response from the model
print(response.choices[0].message.content)


