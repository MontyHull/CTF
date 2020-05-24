# OverFlow1

You beat the first overflow challenge. Now overflow the buffer and change the return address to the flag function in this program? You can find it in /problems/overflow-1_3_f08d494c74b95dae41bff71c2a6cf389 on the shell server.

## TODO

- [x] Create python script to complete challenge
- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

This is the most basic of buffer overflow problems. Here the program is using gets() to fill a buffer with user input. The length of the input for gets is not checked, so you can overflow your buffer and begin to rewrite items on your stack. Since the return address for the function you are in is written on the stack, we should be able to write enough to the stack to return to the flag function instead of main.

### How are we going to exploit it?

When we initially run this code we get this output:
```
./vuln
Give me a string and lets see what happens:
Hello, World!
Woah, were jumping to 0x8048705 !
```

Now if we run this program with a cyclic string in the pwntools library to determine how much we need to overwrite we get this output before a segfault:
```
./vuln
Give me a string and lets see what happens:
ABCD....
Woah, were jumping to 0x61616174 !
```
If we then open up python and run cyclic_find(0x61616174) we find that our offset is 76 characters, so our payload should be 76 bytes plus the address for the flag function. To get the flag function address you can use objdump, gdb, pwntools, or r2. I choose pwntools, because it is just too easy.

### The exploit

With our known offset, we can then set up a payload in pwntools with a few lines of code:
```
payload = "A"*76
flag_address = elf.symbols['flag']
payload += p32(flag_address)
```
Now we need to send the payload and we will have the flag.
