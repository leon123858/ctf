# monkey2

目標, 取得 shell 控制權

## concept

可以用 `objdump -d monkey` 取得組語 `system` 函數的 位置

也可以用以下指令查看該外部連結函式庫跳轉位置

```
readelf -a test > elf_info.txt
readelf -w test > dwarf_info.txt
```

目標都是希望直接跳轉去執行 `system` 外部連結函數
