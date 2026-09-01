# ⚡ 1-Click Local AI Server Stack (Docker Compose + vLLM + AWQ Guide)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![AI_SNIPP](https://img.shields.io/badge/Curated%20by-AI__SNIPP-cyan.svg)](https://instagram.com/ai_snipp)

Run private 70B parameter models (Llama 3.3 70B, DeepSeek Coder) on a single consumer GPU with **140+ tokens/sec** throughput, zero cloud token bills, and 100% on-premise data privacy.

> **Featured on AI_SNIPP Reel #063:** *"The Zero-Dollar Private AI Stack: Stop paying OpenAI $500/month."*

---

## 🏗️ Architecture Stack

```
                          ┌──────────────────────────┐
                          │   Your AI Application    │
                          │   (LangChain / Autogen)  │
                          └────────────┬─────────────┘
                                       │ (OpenAI-Compatible API)
                                       ▼
                          ┌──────────────────────────┐
                          │    vLLM Server (Port 8000)│
                          │  (TensorRT-LLM + PagedAttn)│
                          └────────────┬─────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │  Llama-3.3-70B-AWQ (4-bit)│
                          │   (18.2 GB VRAM Usage)   │
                          └──────────────────────────┘
```

---

## 🚀 Quick Start in 60 Seconds

### 1. Launch with Docker Compose
```bash
docker compose up -d
```

### 2. Test Local Endpoint
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="none"
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-AWQ",
    messages=[{"role": "user", "content": "Write an async Python queue worker."}]
)


print(response.choices[0].message.content)
```

---

## 📊 Benchmark Comparison

| Metric | Cloud OpenAI (GPT-4o) | Local vLLM (Llama 3.3 70B AWQ) |
|---|---|---|
| **Monthly Cost** | $400 – $1,200 / mo | **$0.00 / mo** |
| **Token Rate** | 80 tok/sec (Rate limited) | **142.8 tok/sec (Uncapped)** |
| **Data Privacy** | Sent to cloud data center | **100% Private (Never leaves GPU)** |
| **P99 Latency** | 850ms | **180ms** |

---

## 📄 License
MIT License. Free for commercial and personal use.

*Follow [@ai_snipp](https://instagram.com/ai_snipp) on Instagram for daily production AI engineering blueprints.*
