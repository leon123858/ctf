# crypto shell

題目不完整，所以僅提供解答，這本書的這兩題似乎沒處理好，這題按照網路的資訊不足以解開(難度過高)

## concept

利用 PaddingOracle 完成 RCE

## PaddingOracle

🎯 攻擊原理說明
我們來一步步拆解 Padding Oracle 攻擊的 核心流程。

假設：
有一組密文：IV | C1

解密公式：P1 = D(C1) ⊕ IV

我們希望知道 P1 的內容（明文）

方法：
準備一個假的 IV'（隨便改 IV）

將 IV' | C1 傳給 oracle，伺服器會嘗試解密並檢查 padding。

你調整 IV' 的最後一個 byte，直到 padding 為合法（比如 0x01）時，oracle 回應「成功」。

此時你知道 D(C1)[-1] ⊕ IV'[-1] == 0x01，你就可以反推出 D(C1)[-1] = IV'[-1] ⊕ 0x01。

有了 D(C1)，只要 XOR 上真正的 IV，就可以算出明文 P1。

✅ 重複這個過程 16 次，你就能還原整個明文 block！

所以 IV 的重要性堪比 private key !!!
