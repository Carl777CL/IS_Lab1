import requests

# 1. 测试注册
print("--- 1. Test registration (POST /api/register) ---")
res = requests.post('http://127.0.0.1:5000/api/register', json={'username': 'admin', 'password': 'Password123'})
print(f"Status code: {res.status_code}")
print(f"Response: {res.text}\n")

# 2. 测试登录
print("--- 2. Test login to obtain a Token (POST /auth/login) ---")
res = requests.post('http://127.0.0.1:5000/auth/login', json={'username': 'admin', 'password': 'Password123'})
print(f"Status code: {res.status_code}")
print(f"Response: {res.text}\n")

# 提取 token
token = res.json().get('token')

# 3. 测试不带 Token 访问（预期被拒绝）
print("--- 3. Test accessing a protected endpoint without a Token (GET /api/data) ---")
res = requests.get('http://127.0.0.1:5000/api/data')
print(f"Status code: {res.status_code}")
print(f"Response: {res.text}\n")

# 4. 测试带 Token 访问
print("--- 4. Test accessing with a Token (GET /api/data) ---")
headers = {'Authorization': f'Bearer {token}'}
res = requests.get('http://127.0.0.1:5000/api/data', headers=headers)
print(f"Status code: {res.status_code}")
print(f"Response: {res.text}\n")