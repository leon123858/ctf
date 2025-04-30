# SSRF

## hints

- web 容器中存在一个 flag

goto `http://localhost:8233`

## fast solution

直接在文字框嘗試輸入 `http://localhost:80/static/style.css` 就順利讀取到網頁的 CSS

這看起來直接就是任意檔案讀取，按照提示瞄準目標檔案 `http://localhost:80/flag.php`

![alt text](image.png)

順利讀到 flag，但這應該是題目設計問題，PHP 有些標準函數，可能在 docker-compose 環境中失效了，所以才那麼簡單。

## Solution

進入網頁後，按下連結可以看到，背後的原始碼，是一種提示

```php
<?php
highlight_file(__FILE__);
function check_inner_ip($url)
{
    $match_result=preg_match('/^(http|https)?:\/\/.*(\/)?.*$/',$url);
    if (!$match_result)
    {
        die('url fomat error');
    }
    try
    {
        $url_parse=parse_url($url);
    }
    catch(Exception $e)
    {
        die('url fomat error');
        return false;
    }
    $hostname=$url_parse['host'];
    $ip=gethostbyname($hostname);
    $int_ip=ip2long($ip);
    return ip2long('127.0.0.0')>>24 == $int_ip>>24 || ip2long('10.0.0.0')>>24 == $int_ip>>24 || ip2long('172.16.0.0')>>20 == $int_ip>>20 || ip2long('192.168.0.0')>>16 == $int_ip>>16;
}

function safe_request_url($url)
{

    if (check_inner_ip($url))
    {
        echo $url.' is inner ip';
    }
    else
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $output = curl_exec($ch);
        $result_info = curl_getinfo($ch);
        if ($result_info['redirect_url'])
        {
            safe_request_url($result_info['redirect_url']);
        }
        curl_close($ch);
        var_dump($output);
    }

}

$url = $_GET['url'];
if(!empty($url)){
    safe_request_url($url);
}

?>
```

發現該後端服務:

- 若前端傳入的網址為內網 IP，則會不動作，原地 echo 該網址是內網 IP。
- 若前端傳入的網址為外網 IP，則會進行 `curl` 請求，並將結果回傳給前端 (支援轉址)。

可以推敲攻擊方向是 SSRF (跨站請求偽造)，要想辦法使目標後端對不安全的 URI 做請求，因此間接讀取目標後端任意檔案。

更明確說，該 URI 需要被 `check_inner_ip` 檢查為外網 IP，但被 `curl_exec` 當作本機地址呼叫。

接著就是審計上述程式碼的安全漏洞，並嘗試利用該漏洞進行攻擊。

- `'/^(http|https)?:\/\/.*(\/)?.*$/'` 這段正則表達式不需要繞過，只要確保使用 / 或是 . 分隔多段英文或數字即可
- `parse_url` 提出的 host 會被 `gethostbyname` 檢查是否為外網，所以我們要給他一個外網的 domain name
  - parse_url 是個有漏洞的方法，他僅會把最後一個斜線前面特殊符號@後面的字串解讀為 domain name
  - 但實際上 `curl_exec` 是從前面往後解析遇到的第一個 domain name
  - 綜合起來，我們的 URI 前半段要是內網 IP，中間用特殊符號@分隔，後半段隨便挑一個外網域名，如下:
  - `http://fakeUser:fakePasswd@127.0.0.1:80@google.com/flag.php`

核心概念是給出一個其實是非法的 URI，

- 但因為檢查是否合法的函數(parse_url)有漏洞, 只會從後半段往前檢查是否合法, 這段會讀到 `google.com` 當作 domain name, 並嘗試用 gethostbyname 解析它。
- 而 curl_exec 會從前往後解析到 `fakeUser:fakePasswd@127.0.0.1:80` 當作 domain name，並嘗試連接到它，即使後半段的格式明顯非法，也不會造成問題。

總之利用: `http://fakeUser:fakePasswd@127.0.0.1:80@google.com/flag.php` 可以順利讀取到 flag。
