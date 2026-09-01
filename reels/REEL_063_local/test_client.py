from openai import OpenAI
import time

client = OpenAI(base_url="http://localhost:8000/v1", api_key="local-token")

print("Pinging local vLLM 70B model...")
t0 = time.time()
resp = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-AWQ",
    messages=[{"role": "user", "content": "Explain async generator in 2 sentences."}]
)
elapsed = time.time() - t0

print(f"\nResponse ({elapsed:.2f}s):\n{resp.choices[0].message.content}")
