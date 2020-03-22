# OverFlow0

This should be easy. Overflow the correct buffer in this program and get a flag. Its also found in /problems/overflow-0_3_dc6e55b8358f1c82f03ddd018a5549e0 on the shell server.

## TODO

- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

This program will print the flag when it encounters a segfault signal. So we must create a segfault

### How are we going to exploit it?

This program takes the first command line argument and puts it into a buffer. So we must give it an input that is too large for the buffer so that we can create a segfault.

### The exploit

I gave the program 200 bytes of "A" and we segfaulted and received the flag.
