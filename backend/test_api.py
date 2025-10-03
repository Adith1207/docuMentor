import requests

BASE = "http://127.0.0.1:8000"

# 1. Health check
print("Ping:", requests.get(f"{BASE}/ping").json())

# 2. Ask endpoint
resp = requests.post(f"{BASE}/ask", json={"question": "What does the greet function in sample.txt do?"})
print("Ask:", resp.json())

# 3. Comment-text endpoint (JSON input)
resp = requests.post(f"{BASE}/comment-text", json={"code": "def add(a,b): return a+b"})
print("Comment-text:", resp.json())

# 4. Comment-file endpoint (upload a Python file)
with open("sample.py", "w") as f:
    f.write("def multiply(x, y):\n    return x * y")

with open("sample.py", "rb") as f:
    resp = requests.post(f"{BASE}/comment-file", files={"file": f})
    print("Comment-file:", resp.json())
