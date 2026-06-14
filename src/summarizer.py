import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEYS = [
    os.getenv("OPENROUTER_API_KEY_1"),
    os.getenv("OPENROUTER_API_KEY_2"),
    os.getenv("OPENROUTER_API_KEY_3"),
    os.getenv("OPENROUTER_API_KEY_4"),
    os.getenv("OPENROUTER_API_KEY_5"),
]
API_KEYS = [k for k in API_KEYS if k]

current_key_index = 0

MODELS = [
    "google/gemma-4-31b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-4-26b-a4b-it:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
]

def summarize(text: str, context: str = "crypto/NFT/Web3") -> str:
    global current_key_index
    
    prompt = f"""Kamu adalah crypto research assistant.
Summarize konten berikut dalam bahasa Indonesia, maksimal 3 kalimat.
Fokus pada informasi penting tentang {context}.

Konten:
{text}"""

    for model in MODELS:
        for _ in range(len(API_KEYS)):
            try:
                client = OpenAI(
                    api_key=API_KEYS[current_key_index],
                    base_url="https://openrouter.ai/api/v1"
                )
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e):
                    current_key_index = (current_key_index + 1) % len(API_KEYS)
                    time.sleep(1)
                    continue
                raise e
    
    return "⚠️ Semua model dan key sedang rate-limited."