# Serialization Vulnerability

## Solution

可以參考: `https://jason1314zhang.github.io/blog/N1BOOK-thinkphp%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E5%88%A9%E7%94%A8%E9%93%BE/`

有按照解答的步驟操作，但是無效，懷疑環境有問題

## 概念解析

php 中存在像是 `__construct` `__destruct` 等匿名函數可以因為物件情境自動被調用。

以 `__destruct` 為例，當一個物件被銷毀時，`__destruct` 會被自動調用。如果在 `__destruct` 中存在根據某個內部變數，在 shell 中把變數當作指令執行，那就有被利用的空間。

進一步用偽代碼說明：

client code

```php
<?php
class Exploit {
    public $cmd;
}

exp = new Exploit();
exp->cmd = 'ls';
echo serialize(exp);
```

server code

```php
<?php
class Exploit {
    public $cmd;
    function __destruct() {
        system($this->cmd);
    }
}

// post request
function exploit($data) {
   $exploit = unserialize($data);
}
```

用上面的例子可以很容易理解

- server 中存在某個危險物件，會在釋放時自動根據內部變數執行任意系統命令
- 因此只要客戶端序列化該物件，並且指定內部變數的值
- 接著只要服務器在 client request 中真的反序列化該物件
- 那當 server 離開函數後自然釋放該物件時，就會根據攻擊者指定的內部變數執行系統命令。

進一步聊到漏洞挖掘

概念上就是想辦法找到危險物件，之後利用使用者可以操作的物件，一層一層影響到最後的危險物件，且控制危險物件的重要參數。
