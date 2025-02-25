from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# 读取 API Key（从 Koyeb 环境变量）
LLM_PROXY_API_KEY = os.getenv("LLM_PROXY_API_KEY")
print(f"DEBUG: Using API Key - {LLM_PROXY_API_KEY}")

# LLMProxy API 地址
LLM_PROXY_URL = "https://a061igc186.execute-api.us-east-1.amazonaws.com/dev"

@app.post("/")
async def query(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # 确保 API Key 不是 None
    if not LLM_PROXY_API_KEY:
        return {"error": "Missing API key"}

    # 发送请求到 LLMProxy
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


    try:
        response = requests.post(LLM_PROXY_URL, json=payload, headers=headers)
        response.raise_for_status()
        llm_response = response.json().get("result", "Sorry, I couldn't process your request.")
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    return {"response": llm_response}

# 确保 Uvicorn 运行在 8000 端口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
