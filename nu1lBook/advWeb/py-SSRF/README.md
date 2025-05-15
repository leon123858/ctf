# python Vulnerable 1

## Description

尝试访问到容器内部的 `8000` 端口和 url path `/api/internal/secret` 即可获取 flag

## Solution

按照提示輸入網址 `http://localhost:8000/api/internal/secret` 被拒絕，顯示 `your ip 172.18.0.1 is not allowed`

表示該系統是使用 IP 白名單進行限制的，大膽猜測這是一個 SSRF 漏洞，可能存在方法可以 access 外部資源。

在首頁 `http://localhost:8000/` 按照提示 `url parameter is required`，嘗試輸入合法 url 到 query parameter 中，例如：`http://localhost:8000/?url=http://google.com`，結果成功跳轉到 google 網站。

直接試試用 SSRF 打目標內部路由 `http://localhost:8000/?url=http://localhost:8000/api/internal/secret` 很自然地失敗了，得到 `127.0.0.1 is forbidden` 的錯誤信息，不然就太簡單了。

接著嘗試各種 python 可能的 SSRF 攻擊方式，看看能不能成功繞過對 localhost 的限制。

### 首先嘗試 `CRLF` injection：

原始內容

```
http://google.com HTTP/1.1
TEST: localhost:8000/api/internal/secret
```

可以 encode 成: `http://google.com%20HTTP%2F1.1%20%0ATEST%3A%20localhost%3A8000%2Fapi%2Finternal%2Fsecret`

可以發現換行，並未觸發，可以理解有方法製換了危險符號。

### 改成嘗試白名單漏洞

看看阻擋 127.0.0.1 是否有包含所有別名。

在 linux 中常見可以使用 `0.0.0.0` 來代替 `127.0.0.1`

呼叫 `http://localhost:8000/?url=http://0.0.0.0:8000/api/internal/secret`

成功得到 flag。
