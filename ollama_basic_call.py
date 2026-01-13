import requests
import json

#simple example
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "tinyllama", "prompt": "Hello there!"}
)

for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))

#complex example
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "tinyllama",
        "prompt": "What is the capital of France?",
        "stream": False
    }
)

data = response.json()
print(data["response"])

#streaming example
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France? Answer in one sentence."}
]

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "tinyllama",
        "messages": messages,
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line)
        if "message" in data and "content" in data["message"]:
            print(data["message"]["content"], end="", flush=True)
print()  # New line at the end