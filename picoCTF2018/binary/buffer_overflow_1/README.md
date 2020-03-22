# buffer overflow 1

## TODO

- [x] Create python script to complete challenge
- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

When the program is run we see that we are given:
```
./vuln
Please enter your string:
A
Okay, time to return... Fingers Crossed... Jumping to 0x80486b3
```

If we look at our code we see that in the vuln() function we have a character buffer of size 32 and then we use gets to fill it with user input. Since gets does not check the size of the buffer that it is writing to we are able to overflow said buffer.

### How are we going to exploit it?

We are going to try to overwrite the address that vuln will return to once we hit the end of that function. Since our input is not limited with gets, and our buffer can only hold 32 bytes, we know that we can write to the stack and write instructions where we want them. If you use r2, gdb, the pwn library, or any other number of tools to dissassemble the binary we can find win()'s address.

### The exploit

Since we know we can write to the stack, we first have to know how to get there. The easiest way to do this is to use a cyclic string to determine where our eip is pointing when we segfault. There is an example and explanation for this in the solution.py file. However, if we wish to do this by hand we see that our buffer can only hold 32 bytes so we must first write 32 bytes to fill it. Then we must write 12 more bytes to skip over the other values that are in between the saved eip and the end of the buffer. I'm not positive what 8 of the bytes are, but I'm pretty sure it is the compiler aligning the stack for us, because in GDB the extra 8 bytes are included with the initialization of the buffer. But after those 8 bytes you have 4 more bytes for the EBP, then you can write to the saved EIP whatever you want. If you write the return address to the win() function then this challenge is solved.
