
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"


def generate(prompt):

    # Prepare the request payload
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    # Send request to local Ollama server
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=(10, 300)
    )

    # Handle unsuccessful responses
    response.raise_for_status()

    # Extract generated answer
    result = response.json()

    return result["response"]


if __name__ == "__main__":

    answer = generate(
        "Reply with exactly: Ollama integration successful!"
    )

    print("\nModel response:")
    print(answer)

