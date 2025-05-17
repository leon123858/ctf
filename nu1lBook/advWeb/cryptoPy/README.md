# Encrypted Flask

## description

跟你说了客户端 session 不安全, 你还硬要用. 没关系, 我加了密呀.

## concept

在传统 PHP 开发中，$\_SESSION 变量的内容默认会被保存在服务端的一个文件中，通过一个叫 `PHPSESSID`的 Cookie 来区分用户。这类 session 是`服务端 session`，用户看到的只是 session 的名称（一个随机字符串），其内容保存在服务端。

然而，并不是所有语言都有默认的 session 存储机制，也不是任何情况下我们都可以向服务器写入文件。所以，很多 Web 框架都会另辟蹊径，比如 Django 默认将 session 存储在数据库中，而对于 flask 这里并不包含数据库操作的框架，就只能将 session 存储在 cookie 中。

因为 cookie 实际上是存储在客户端（浏览器）中的，所以称之为`客户端 session`

ref: [link](https://github.com/Jason1314Zhang/BUUCTF-WP/blob/main/N1BOOK/%5B%E7%AC%AC%E4%B8%89%E7%AB%A0%20web%E8%BF%9B%E9%98%B6%5DEncrypted%20Flask.md)

## Solutions

隨意嘗試帳號密碼註冊

嘗試註冊帳號: `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`

得到 session 如下:

- 8795dacaa9d3ee1b4af3d37bbd301fc6
- fa85a45f5450e20117b729998e66301c
- a6c2d509a9d65fdd7efe6c70930e0635
- a6c2d509a9d65fdd7efe6c70930e0635
- a6c2d509a9d65fdd7efe6c70930e0635
- a6c2d509a9d65fdd7efe6c70930e0635
- f22a02463529abfdba6f75850cc37f34

get same part: `a6c2d509a9d65fdd7efe6c70930e0635`, have same part is => ECB mode.

CBC mode will not have the same part because of the random initialization vector.

so => `a6c2d509a9d65fdd7efe6c70930e0635` is someFormatFunc(`AAAAAAAAAAAAAAAA`)

接著嘗試用加減長度，得到推論，user name 可以控制 session 中間的變化，前後有各自的內容，username 不可控。

所以 session 明文格式類似 `someFormatFunc(key+username+someExtInfo)`

此時按照解答利用 ECB 特性差一位暴力嘗試，應該有解，但實測無效。

以下簡述做法概念:

明文: 不可控內容 A + 可控內容 B + 不可控內容 C

把 A 填充到 block size, 可控內容 B 保持在 2 個相同 block, C 維持。

接著依照原理，CBC 中相同明文會產生相同密文，所以把 B 前 一個 block 當作猜測，15*8 用相同字符，最後一個 8 暴力嘗試，目標是後一個 block 保持 15*8 用相同字符，最後一個 8 會是不可控內容的 C 的前 8 。

範例如下: `username = b'|RS(#@LgP<\\dXXXXXXXXXXXXXXX\x00XXXXXXXXXXXXXXX'`

- `XXXXXXXXXXXXXXX\x00` 是 B 的猜測段，長度為 16，最後一個字節是 `\x00`，表示 B 結束。
- `XXXXXXXXXXXXXXX` 是 B 的目標段，長度為 15，最後一個字節會在 session key 中被補上 C 的前第一個字節。

猜測段和目標段在猜中後於加密結果中應該要相同

猜中後不斷填充已知的字符，直到完整試出所有 C 的字符。

但解答無法復現，略。
