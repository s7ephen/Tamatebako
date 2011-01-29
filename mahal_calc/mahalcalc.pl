#!/usr/bin/perl 
# PDL is installed, next step is to  do matrix inversion, etc.
#[00:49:21] sundberg80: sure, you get a 1 by m matrix
#[00:49:37] sundberg80: and the way you compute the entry for observation i
#[00:50:01] sundberg80: is (x_i - mean)' * inverse(S) * (x_i - mean)
#[00:50:06] sundberg80: in vector notation
#[00:50:20] sundberg80: ' means transpose
#[00:50:35] sundberg80: basically, compute (x_i - mean)
#[00:50:50] sundberg80: which will be a n dimensional vector
#[00:51:05] sundberg80: multiply it by the n by n inverse of S
#[00:51:26] sundberg80: you get a new n dimensional vector
#[00:51:46] sundberg80: then multiply the entries pairwise with (x_i - mean)
#[00:51:48] sundberg80: sum
#[00:51:51] sundberg80: and you get a number
#[00:51:59] sa7ori: right.
#[00:52:13] sundberg80: repeat for your m observations
#[00:52:18] sundberg80: and you have your distance list

use PDL;
use PDL::Slatec;

sub get_x_matrix_params() {
	print ("\nEnter the number of features (eg (i,j) is 2; (i,j,k) is 3 ==> "); $fea=<STDIN>; chomp $fea;
	print ("\nEnter the number of observations ==> "); $obs=<STDIN>; chomp $obs;
	print ("\nOur X matrix has $fea x $obs dimensions."); 
};

sub create_x_matrix() {
	@x_matrix=();
	get_x_matrix_params();
	get_x_matrix_contents();
};

sub get_x_matrix_contents() {
        print ("\nYou will now input the actual data contained within the X Matrix.");
	my $x = my $y = 0; #counters for going through each element of the matrix along the 2 axis's
	my $numx = $fea - 1; # start from 0 so we subtract 1
	my $numy = $obs - 1; # "" 
	#print ("\n$x, $y, $numx, $numy");
	# The below nested for loops == for each y, go through all x's
        for ($y = 0; $y <= $numy; $y++) { 
                for ($x = 0; $x <= $numx; $x++) {
			#print ("\n$x, $y, $numx, $numy");
                        print ("\nX[$y, $x]? ==> "); my $input = <STDIN>; chomp $input;
			$x_matrix[$x][$y] = $input;
		};
        };
};

sub print_x_matrix_contents () {
	print ("\n\nThe contents of the X-MATRIX are as follows:\n");
	my $x = my $y = 0; # counters for going through each element of the matrix along the 2 axis's
	my $numx = $fea - 1;
	my $numy = $obs - 1;
	# The below nested for loops == for each y, go through all x's
        for ($y = 0; $y <= $numy ; $y++) {
                for ($x = 0; $x <= $numx; $x++) {
                        print ("-|$x_matrix[$x][$y]|-");
                };
		print ("\n"); # newline for next y values.
        };
};

sub calc_mean_vector() {
	@mean_vector = ();
	my $x = my $y = 0;
	my $numx = $fea - 1;
	my $numy = $obs - 1;
	# The below nested for loops == for each x, go through all y's
        for ($x = 0; $x <= $numx; $x++) {
		my $sum = 0; #clear sum variable
                for ($y = 0; $y <= $numy; $y++) {
			#print ("\n$sum + $x_matrix[$x][$y] = ");
			$sum = $sum + $x_matrix[$x][$y];
			#print ("$sum");  
                };
		$mean_vector[$x] = $sum/$obs;
        };

};

sub print_mean_vector(){
	print ("\nThe contents of the MEAN VECTOR are as follows:\n");
	my $size_of_mean_vector = @mean_vector - 1 ;
	my $n=0;
	for ($n = 0; $n <= $size_of_mean_vector; $n++) {
		print ("-|$mean_vector[$n]|-"); 
	};	
};

sub create_s_matrix() {
	@s_matrix = ();
        my $x = my $y = 0; #counters for going through each element of the matrix along the 2 axis's
        my $s_x = $fea - 1; # start from 0 so we subtract 1
        my $s_y = $s_x; 
        # summary of loop below:  Pair features (x's of x_matrix) in two's and pass to calc_c_matrix
        for ($x = 0; $x <= $s_x; $x++) {
                for ($y = 0; $y <= $s_y; $y++) {
                        $s_matrix[$x][$y] = calc_c_matrix($x, $y); 
                };
        };
}; 

sub print_s_matrix() {
        my $x = $y = 0; #counters for going through each element of the matrix along the 2 axis's
        my $s_x = $fea - 1; # start from 0 so we subtract 1
	my $s_y = $s_x;
        print ("\n\nThe contents of the S-MATRIX are as follows:\n");
        for ($x = 0; $x <= $s_x; $x++) {
                for ($y = 0; $y <= $s_y; $y++) {
                	print ("-|",$s_matrix[$x][$y],"|-");
		};
	print ("\n");
        };
};

sub create_pdl_s_matrix() {
	$pdl_s_matrix = sequence ($fea,$fea); #initialize pdl_s_matrix using pdl command 'sequence' 
					 #with dimensions $fea by $fea.
	my $tmpx, $tmpy; # temp variables for slices of pdl_s_matrix
        my $x = $y = 0; #counters for going through each element of the s_matrix along the 2 axis's
        my $s_x = $fea - 1; # start from 0 so we subtract 1
        my $s_y = $s_x; #because the S-MATRIX is always square we insure this by making sure that 
			#the dimensions match.
        print ("\n\nThe contents of the S-MATRIX are as follows:\n");
        for ($x = 0; $x <= $s_x; $x++) { 
                for ($y = 0; $y <= $s_y; $y++) {
                 #       print ("-|",$s_matrix[$x][$y],"|-");
			$tmpx = $pdl_s_matrix->slice(":,($x)"); 
			$tmpy = $tmpx->slice("($y)"); 
			$tmpy .= $s_matrix[$x][$y]; #this requires ".="
                };
        };
	print $pdl_s_matrix; #prints the PDL_ized S-matrix 

};

sub invert_s_matrix() {
#This function inverts the S-Matrix (a.k.a The variance/covariance matrix)
	create_pdl_s_matrix();
	$inv_s_matrix = zeroes($fea, $fea);
	($inv_s_matrix) = matinv($pdl_s_matrix);
	print "\n\nThe contents of the INVERTED S_MATRIX are:\n ";
	print $inv_s_matrix;
};

sub calc_c_matrix(){
	my ($c_x, $c_y) = @_; #pair of features (x's of x_matrix) we must access.
	my $c_matrix = 0;
	
	my $n = 0; my $n_sum = 0;
        my $c_n = $obs - 1;
	#print ("\n\nC($c_x, $c_y) = [");
        for ($n = 0; $n <= $c_n; $n++) {
		my $n_sum_this_iteration = 0;
		#print ("(",$x_matrix[$c_x][$n]," - ",$mean_vector[$c_x], ")");
		#print ("(",$x_matrix[$c_y][$n]," - ",$mean_vector[$c_y], ")+ "); 
		$n_sum_this_iteration = (($x_matrix[$c_x][$n] - $mean_vector[$c_x])*($x_matrix[$c_y][$n] - $mean_vector[$c_y]));
		#print("  $n_sum_this_iteration");
		$n_sum = $n_sum + $n_sum_this_iteration; #print("      $n_sum\n");
       };
	my $n_div = (1/($obs - 1)); 
	$c_matrix = ($n_sum*$n_div);
	#print("] * [1/$obs] = $c_matrix ==> C($c_x, $c_y) = $c_matrix");
	return ($c_matrix);
};

sub test_input() { #create/get data for testing
	# FEA and OBS are the dimensions of our test matrix these are held in globals.
	$fea = 3; # this GLOBAL holds the number of "features" of our matrix.
	$obs = 5; # this GLOBAL hold the number of trials/observations for our matrix
	my $input_n = 0;
	# The TEST_INPUT matrix contains the test data we use for input.
	my @test_input = (0, 579, 4,
			110, 503, 12,
			115, 579, 2,
			290, 643, 2, 
			128, 740, 5);
        my $x = my $y = 0; #counters for going through each element of the matrix along the 2 axis's
        my $numx = $fea - 1; # start from 0 so we subtract 1
        my $numy = $obs - 1; # ""
        for ($y = 0; $y <= $numy; $y++) {
                for ($x = 0; $x <= $numx; $x++) {
                        $x_matrix[$x][$y] = $test_input[$input_n]; $input_n++;
                };
        };

};
sub main() {
# skipping creation, for use of seed data.
#	create_x_matrix();
	test_input();
	print_x_matrix_contents();
	calc_mean_vector();
	print_mean_vector();
	create_s_matrix();
	print_s_matrix();
	invert_s_matrix();
};
main();
