from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# 读取 Koyeb Secrets 里的 API Key
LLM_PROXY_API_KEY = os.getenv("comp150-cdr-2025s-kAQPJchYTEkAkv8vNuSnRUSiTogxnYWBO97JvNTO")

LLM_PROXY_URL = "https://a061igc186.execute-api.us-east-1.amazonaws.com/dev"

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # 调用 BridgeLLM (LLMProxy)
    headers = {
        "Authorization": f"Bearer {LLM_PROXY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "4o-mini",
        "system": "You are a helpful chatbot answering user queries.",
        "query": user_message,
        "temperature": 0.7,
        "lastk": 3,
        "session_id": "RocketChatSession",
        "rag_usage": False
    }

    response = requests.post(LLM_PROXY_URL, json=payload, headers=headers)
    llm_response = response.json().get("result", "Sorry, I couldn't process your request.")

    return {"response": llm_response}
