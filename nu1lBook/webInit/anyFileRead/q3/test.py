from itsdangerous import URLSafeTimedSerializer

# 你的 secret_key
secret_key = 'Drmhze6EPcv0fN_81Bj-nA'

# 傳入的 session cookie
session_cookie = 'eyJuMWNvZGUiOm51bGx9.aA5-WQ.-k-f3IdqZKAYLayjRg7r75kv1KA'

# 創建一個 URLSafeTimedSerializer 實例，用來解密 session
serializer = URLSafeTimedSerializer(secret_key)

# 解密並還原 session 內容
try:
    # 這邊解碼
    data = serializer.loads(session_cookie)
    print("解密後的 session 資料:", data)
except Exception as e:
    print("解密錯誤:", e)
