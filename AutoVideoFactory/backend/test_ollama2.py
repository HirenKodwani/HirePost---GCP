import subprocess, json, os, time, sys

# Write the JSON payload to a temp file
payload = json.dumps({
    "model": "llama3.2:3b",
    "prompt": "Say hello in 3 words",
    "stream": False,
    "options": {"num_predict": 10},
})
req_path = os.path.join(os.environ["TEMP"], "ollama_req2.json")
with open(req_path, "w") as f:
    f.write(payload)

print(f"Payload: {payload}", flush=True)
print(f"Sending request...", flush=True)
start = time.time()

try:
    result = subprocess.run(
        ["curl.exe", "-s", "-X", "POST", "http://localhost:11434/api/generate",
         "-d", f"@{req_path}"],
        capture_output=True, text=True, timeout=300,
    )
    elapsed = time.time() - start
    print(f"Time: {elapsed:.1f}s", flush=True)
    print(f"stdout: {result.stdout[:500]}", flush=True)
    if result.stderr:
        print(f"stderr: {result.stderr[:500]}", flush=True)
except subprocess.TimeoutExpired:
    print(f"TIMEOUT after {time.time()-start:.1f}s", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)

os.remove(req_path)
