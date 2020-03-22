# slippery-shellcode

This program is a little bit more tricky. Can you spawn a shell and use that to read the flag.txt? You can find the program in /problems/slippery-shellcode_0_7440dd178b8f0686410008ac1268d808 on the shell server

## TODO

- [x] Create python script to complete challenge
- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

This challenge is a lot like the handy shellcode problem solved earlier. The main difference is that they now are executing the code you give them starting at a random posistion from within your buffer. So we have to find a way to get the code to execute our code that we give it directely.

### How are we going to exploit it?

We are going to be using what's called a NOP sled for this problem. A NOP is a No Operation instruction. Basically, when these instructions are met we just move to the next instruction and try to execute it. Since this challenge starts executing from some random point in our buffer, if it starts executing at a NOP instruction then it will continue to move to the next instruction until it hits something it can actually run.

### The exploit

We will fill 300 spots of our buffer with NOPs then our shellcode. Somewhere within the first 256 bytes we will hit a NOP, then slide until we hit our shellcode and then execute. I have copied most of my code from the handy shellcode challenge and have given three different but similar approaches to this challenge.
