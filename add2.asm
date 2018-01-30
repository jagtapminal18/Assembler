
section .data
	a dd 4
	b dd 3
	msg db "%d",10,0

section .bss
	c resd 1

section .text
	global main
	extern printf

main:
	mov edx,3
	add eax,2
	add ebx,edx
	mov eax,dword[a]
	mov ebx,dword[b]
	add eax,ebx
	mov ecx,eax
	push ecx
	push msg
	call printf
	add esp,8
