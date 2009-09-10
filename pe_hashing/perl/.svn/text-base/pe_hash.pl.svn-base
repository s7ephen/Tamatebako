#!/usr/bin/perl
#unsigned int make_hash(char *string) {
#// stolen from allens mc_tinyimporter.cpp
#        unsigned int result;
#        _asm {
#                pushad   //save all general purpose registers on the stack
#                mov eax, string //move the address of string into eax.
#                mov esi,eax //move the address of string into esi for lodsb later
#                xor ecx,ecx //zero out ecx
#                mov edx,ecx //zero out edx
#                mov eax,ecx //zero out eax
#                dec ecx     //ecx negative 1
#        Hash2_loop:
#                lodsb //puts byte into AL
#                ror edx, 0Dh //rotate edx right 13 times
#                add edx, eax //add our byte to edx aka edx+=eax
#                test eax,eax //AND eax to eax
#                jnz Hash2_loop //if its not zero then loop again. I assume that this can only be the case if
#                               //eax was null to begin with, in which case we are at the end of the string
#                mov result, edx //put edx into C variable result.
#                popad //restore all registers.
#        }
#        return result;
#}
#
#00401015 ac               lodsb                                ds:002f0f9e=52
#00401016 c1ca0d           ror     edx,0xd
#00401019 03d0             add     edx,eax
#0040101b 85c0             test    eax,eax
#0040101d 75f6             jnz     image00400000+0x1015 (00401015)
$str = $ARGV[0];
$tot = 0;
$rot = 0xd;

print "Hashing $str\n";

@chars = split("",$str);
@chars[length($str)] = "\x00";

foreach $byte (@chars) {
	$tot = &ror($tot, $rot);
	$num = unpack("C", $byte);
	$tot+=$num;
}

printf("got: 0x%.8x\n",$tot);

sub ror {
	$val = shift;
	$bits = shift;
	$mask = 0xffffffff >> (32 - $bits);
	printf("0x%.08x\n",$mask);
	$saved = $val & $mask;
	$res = $val >> $bits;
	$res |= ($saved << (32-$bits));
	return($res);
}
