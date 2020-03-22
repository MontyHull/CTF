What does asm3(0xcdc485c1,0xd6bd5e88,0xe4c1548d) return?

ebp+0x08 = 0xcdc485c1
ebp+0x0c = 0xd6bd5e88
ebp+0x10 = 0xe4c1548d

asm3:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	xor    eax,eax
	<+5>:	mov    ah,BYTE PTR [ebp+0x8]
	<+8>:	shl    ax,0x10
	<+12>:	sub    al,BYTE PTR [ebp+0xe]
	<+15>:	add    ah,BYTE PTR [ebp+0xc]
	<+18>:	xor    ax,WORD PTR [ebp+0x10]
	<+22>:	nop
	<+23>:	pop    ebp
	<+24>:	ret
