import os
import json
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
API_KEYS = [k for k in API_KEYS if k]  # filter yang None

current_key_index = 0

def get_client():
    return OpenAI(
        api_key=API_KEYS[current_key_index],
        base_url="https://openrouter.ai/api/v1"
    )

MODELS = [
    "google/gemma-4-31b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-4-26b-a4b-it:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
]

ROUTER_PROMPT = """Kamu adalah AI router. Tugasmu HANYA menentukan skill yang harus dijalankan berdasarkan pesan user.

Tersedia skills:
- scrape_twitter: ambil tweet dari akun X. Gunakan jika user menyebut username Twitter/X atau minta cek tweet.
- web_search: cari info di internet. Gunakan jika user minta info terbaru/berita.
- chat: jawab langsung tanpa skill. Gunakan untuk pertanyaan umum atau obrolan.

Balas HANYA dengan JSON valid:
{"skill": "nama_skill", "params": {"key": "value"}}

Contoh:
- "cek tweet elonmusk" → {"skill": "scrape_twitter", "params": {"username": "elonmusk"}}
- "cari berita NFT hari ini" → {"skill": "web_search", "params": {"query": "NFT news today"}}
- "halo, apa kabar?" → {"skill": "chat", "params": {}}"""

ASSISTANT_PROMPT = """Kamu adalah Jokowi, personal assistant pribadi Tuan Magro.
Selalu awali balasan dengan "Tuan Magro," diikuti jawabanmu.
Kalau tidak mengerti: "Maaf Tuan, saya tidak mengerti. Bisa jelaskan lebih detail?"
Jawab dalam bahasa yang sama dengan user."""

def call_ai(messages: list) -> str:
    global current_key_index
    
    for model in MODELS:
        for _ in range(len(API_KEYS)):
            try:
                client = get_client()
                response = client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if "429" in str(e):
                    # Rotate ke key berikutnya
                    current_key_index = (current_key_index + 1) % len(API_KEYS)
                    time.sleep(1)
                    continue
                raise e
    
    return None
def route(user_message: str) -> dict:
    raw = call_ai([
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": user_message}
    ])
    
    print(f"[ROUTER RAW]: {raw}")  # tambah ini
    
    if not raw:
        return {"skill": "chat", "params": {}}
    
    try:
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        print(f"[ROUTER RESULT]: {result}")  # tambah ini
        return result
    except:
        return {"skill": "chat", "params": {}}

def chat(history: list) -> str:
    messages = [{"role": "system", "content": ASSISTANT_PROMPT}] + history
    result = call_ai(messages)
    return result or "Maaf Tuan, semua model sedang sibuk. Coba lagi sebentar."