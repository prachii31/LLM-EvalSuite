
import requests

from config.config import (
    GEMINI_API_KEY,
    LLM_MODEL,
    validate_config
)


def test_gemini_connection():

    # Step 1: Validate configuration
    validate_config()

    # Step 2: Prepare Gemini API endpoint
    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{LLM_MODEL}:generateContent"
    )

    # Step 3: Prepare request headers
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    # Step 4: Prepare request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Reply with exactly: "
                            "Gemini connection successful!"
                        )
                    }
                ]
            }
        ]
    }

    print("\nTesting direct Gemini API connection...")

    try:
        # Step 5: Send request to Gemini
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=(10, 120)
        )

        print("\nHTTP Status:", response.status_code)

        # Step 6: Handle unsuccessful responses
        if not response.ok:
            print("\nGemini error details:")
            print(response.text)
            return

        # Step 7: Extract the response
        result = response.json()

        candidates = result.get("candidates", [])

        if not candidates:
            print("\nGemini returned no candidates.")
            print(result)
            return

        parts = candidates[0].get("content", {}).get("parts", [])

        if not parts or "text" not in parts[0]:
            print("\nGemini response did not contain text.")
            print(result)
            return

        answer = parts[0]["text"]

        print("\nGemini response:")
        print(answer)

    except requests.exceptions.Timeout:
        print("\nError: Gemini API request timed out.")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to Gemini API.")

    except requests.exceptions.RequestException as error:
        print("\nRequest error:", error)

    except (ValueError, KeyError, IndexError) as error:
        print("\nResponse parsing error:", error)


if __name__ == "__main__":
    test_gemini_connection()
