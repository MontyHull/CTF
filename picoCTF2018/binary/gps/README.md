# gps

You got really lost in the wilderness, with nothing but your trusty gps [1] . Can you find your way back to a shell and get the flag? Connect with nc 2018shell.picoctf.com 58896.

## TODO

- [ ] Create python script to complete challenge
- [ ] What is the exploitable piece of code?  
- [ ] How are we going to exploit it?
- [ ] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

rand is never seeded so you will always get the same value from it.

before we get the offset rand is called 3 times so on the fourth time rand should equal:

1804289383
846930886
1681692777
1714636915

so in the problem offset is equal to 1714636915 % 1337 - (1337 / 2), which is equal to 597. So now all i need to know is what this difference is between the address of my buffer and the character stk. 


### How are we going to exploit it?

### The exploit
