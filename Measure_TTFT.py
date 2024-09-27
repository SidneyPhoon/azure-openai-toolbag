#This script measures the time to first token (TTFT) and the total time taken to get the full response from the Azure OpenAI API.

from openai import AzureOpenAI
import os
import json
import time

# Declare client
client = AzureOpenAI(api_key = "AZURE_OPENAI_KEY",
                     azure_endpoint = "AZURE_OPENAI_ENDPOINT",
                     api_version = '2024-02-01')

system_prompt = 'Your system prompt'
user_prompt = 'Your user prompt'
start_time = time.time()


response = client.chat.completions.create(
    model = 'gpt-4-0125',
    messages = [
         {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature = 0,
    stream = True
)

chunk_count = 0
full_response = ""
for chunk in response:
    if chunk.id != '':
        if chunk_count == 0:
            time_to_first_token = time.time() - start_time  # calculate the time to first token
        try: 
            full_response += chunk.choices[0].delta.content
        except:
            pass
        chunk_count += 1

total_time_response = time.time() - start_time
print(f"Full conversation received: {full_response}, TTFT: {time_to_first_token}, Total Time: {total_time_response}")