from flask import Flask, request, jsonify
import sqlite3
import jwt
import bcrypt
import datetime
import html
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# 初始化数据库（本地 SQLite）
def init_db():
    conn = sqlite3.connect('lab1.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password BLOB)''')
    conn.commit()
    conn.close()

init_db()

# 接口 3：注册 (POST /api/register) —— 老师要求自己想的第三个方法
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # 安全措施：使用 bcrypt 哈希密码 (防明文存储)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # 安全措施：参数化查询 (防 SQLi)
        conn = sqlite3.connect('lab1.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "User already exists"}), 400

# 接口 1：登录 (POST /auth/login)
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('lab1.db')
    c = conn.cursor()
    # 安全措施：参数化查询 (防 SQLi)
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_hashed_pw = result[0]
        # 验证密码哈希
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw):
            # 安全措施：签发 JWT 令牌 (防 Broken Auth)
            token = jwt.encode({
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            
            return jsonify({"token": token}), 200
            
    return jsonify({"error": "Invalid credentials"}), 401

# 接口 2：获取数据 (GET /api/data) —— 受保护接口
@app.route('/api/data', methods=['GET'])
def get_data():
    # 获取请求头中的 Authorization
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]

    try:
        # 验证 JWT 令牌
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    # 安全措施：对返回的数据进行转义 (防 XSS)
    # 模拟一些数据
    mock_data = [
        {"id": 1, "post": "Hello World <script>alert(1)</script>"},
        {"id": 2, "post": "Flask is fun!"}
    ]
    
    safe_data = []
    for item in mock_data:
        safe_item = {k: html.escape(str(v)) for k, v in item.items()}
        safe_data.append(safe_item)

    return jsonify({
        "message": f"Welcome {decoded['user']}!",
        "data": safe_data
    }), 200

if __name__ == '__main__':
    app.run(port=5000)