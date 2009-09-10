/***************************************************************
This calculates pehash based on the function name.
	

***************************************************************/
#include <stdio.h>
#include <windows.h>

unsigned int make_hash(char *string) {
// stolen from allens mc_tinyimporter.cpp
	unsigned int result;
	_asm {
		pushad
		mov eax, string
		mov esi,eax
		xor ecx,ecx
		mov edx,ecx
		mov eax,ecx
		dec ecx
	Hash2_loop:
		lodsb
		ror edx, 0Dh
		add edx, eax
		test eax,eax
		jnz Hash2_loop
		mov result, edx
		popad
	}
	return result;
}

int main(int argc, char **argv) {
	unsigned int val; int n;
	if (argc <= 1){printf("\n\tUsage:\n\t\t./%s <FunctionName> <FunctionName2>\n", argv[0]);
		printf("\n\n\t***Note*** Function names are case sensitive for hash calculation!\n");
	}
	else {
        printf("\n[+]\tCalculated Hashes below:\n");
		for (n=1;n<argc;n++){	
			val = make_hash(argv[n]);
			printf("\n\t0x%x", val);
		};
		printf("\n\n[+]\t***Note*** Function names are case sensitive for hash calculation!\n");
	};
}
