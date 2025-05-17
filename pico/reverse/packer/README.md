# packer

ref: https://play.picoctf.org/practice/challenge/421

## Solution

- base a the name of this game, use `pwndbg` to check exe file

```bash
pwndbg> checksec
File: /home/leon/桌面/out
Arch: amd64
RELRO: No RELRO
Stack: No canary found
NX: NX enabled
PIE: No PIE (0x400000)
Packer: Packed with UPX
```

- the point is `Packer: Packed with UPX`, this is a compress algorithm
- 下載 UPX 工具: https://github.com/upx/upx
- use command `upx -d out` to decompress
- use disassemble tool `Ghidra` to open the file `out`
- get the `main` function and trace code
- get instruction below

```cpp
puts(
  "Password correct, please see flag: 7069636f4354467b5539585f556e5034636b314e365f42316e345269 33535f65313930633366337d"
);
```

- use `https://www.rapidtables.com/convert/number/hex-to-ascii.html` convert
- get flag `picoCTF{U9X_UnP4ck1N6_B1n4Ri3S_e190c3f3}`
