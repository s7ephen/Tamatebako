#!/usr/bin/perl



$str = $ARGV[0];

print "As Character: $str\n";
$num = unpack("C", $str);
print("As dec ascii val: $num\n");
$num1 = unpack("H*",$str);
print("As hex ascii val: $num1\n");
$num2 = unpack("C", pack("H*", $num1));
$num0 = unpack("C", pack("H*", 0));
print("As dec conversion of hex ascii val: $num2, $num0\n");
$big = "0x01080000";
$big = hex($big);
print $big."\n";

