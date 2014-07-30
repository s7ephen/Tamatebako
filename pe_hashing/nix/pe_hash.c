//This isnt done yet, cuz its kinda redundant and because gcc inline assembler
//is shyt.



#include <sys/stat.h>
#include <sys/mman.h>
//#include <unistd.h>
//#include <inttypes.h>
#include <string.h>

unsigned int make_hash(char *string) {
	unsigned int result;
__asm__ (
	"pushad\n\t"
    "movl string,%eax\n\t"
	"movl %eax,%esi\n\t"
	"xor %ecx,%ecx\n\t"
	"movl %ecx,%edx\n\t"
	"movl %ecx,%eax\n\t"
	"dec %ecx\n\t"
"Hash2_loop:\n\t"
	"lodsb\n\t"
	"ror $0x0d, %edx\n\t"
	"add %eax, %edx\n\t"
	"test %eax,%eax\n\t"
	"jnz Hash2_loop\n\t"
	"movl %edx,result\n\t"
	"popad\n\t"
	);
        return result;
}

int main(int argc, char **argv) {
    int i, max;
	print
}
