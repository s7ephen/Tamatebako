# yarn.tests.py - Yet Another Rational Number module Tester
# Written by Lanny Ripple (8 February 1996).
#
# Code in tests_from_ratpy and tests_from_surdpy are from
# Rat.py and surd.py respectively.  These files may be
# found at ftp.python.org:/pub/python/...
#
# A test suite for yarn.py

from yarn import Rat
import math
import time

#
# Try to run tests that follow every control flow.
#
def tests_for_yarnpy():
	# I find it easier to type 'rat'.
	rat = Rat

	def killrat(val):
		raise 'DeadRat', val

	# Lot of conversion and testing going on in this test itself.
	def t(r, v, eps = 0):
		def killrat(val):
			raise 'DeadRat', val
		delta = abs(r - v)
		# For integers abs(r - v) is always >= 0.
		if eps:
			if delta >= eps: killrat(`delta`+" < "+`eps`)
		else:
			if delta > eps: killrat(`delta`+" <= "+`eps`)

	#
	# Instantiation
	#

	# No args.
	t(rat(), 0)

	# 1 arg.
	t(rat(1), 1)
	t(rat(-1), -1)

	# 2 args
	v = 2.5
	t(rat(2, 5), 2.0/5)
	t(rat(5, 2), v)
	t(rat(-5, 2), -v)
	t(rat(5, -2), -v)
	t(rat(-5, -2), v)

	# 2 args - testing simplification
	t(rat(9, 24), 3.0/8)
	t(rat(12, 2), 6)

	# 3 args
	v = 1 + 2.0/3
	t(rat(1, 2, 3), v)
	t(rat(1, 2, -3), -v)
	t(rat(1, -2, 3), -v)
	t(rat(1, -2, -3), v)
	t(rat(-1, 2, 3), -v)
	t(rat(-1, 2, -3), v)
	t(rat(-1, -2, 3), v)
	t(rat(-1, -2, -3), -v)

	# Floating values
	t(rat(math.pi), math.pi, 1e-6)
	t(rat(math.e, 2), math.e, 1e-2)

	#
	# Casts
	#
	t(int(rat(22, 7)), 3)
	t(long(rat(8297634872364823L, 2)), 4148817436182411L)
	t(float(rat(math.e)), math.e, 1e-6)

	#
	# Math
	#
	r0 = rat(0)
	r1 = rat(1)
	r2 = rat(2)
	r3 = rat(3)
	r4 = rat(4)
	r5 = rat(5)
	r6 = rat(6)
	r7 = rat(7)
	r8 = rat(8)
	r9 = rat(9)
	a = rat(int(r5), int(r7))

	# rat vs. rat
	t(+r2, 2)
	t(-r2, -2)
	t(-(-r2), 2)
	t(abs(r2), 2)
	t(abs(-r2), 2)

	t(r2 + r5, 7)
	t(r5 - r7, -2)
	t(r2 * r7, 14)
	t(r5 / -r7, -5.0/7)

	q, r = divmod(r7, r5)
	t(q, 1)
	t(r, 2)
	q, r = divmod(-r7, r5)
	t(q, -2)
	t(r, 3)
	q, r = divmod(r7, -r5)
	t(q, -2)
	t(r, -3)
	q, r = divmod(-r7, -r5)
	t(q, 1)
	t(r, -2)

	r4p = rat(4.75)
	r3p = rat(3.25)
	q, r = divmod(r4p, r3p)
	t(q, 1.0)
	t(r, 1.5)
	q, r = divmod(-r4p, r3p)
	t(q, -2.0)
	t(r, 1.75)
	q, r = divmod(r4p, -r3p)
	t(q, -2.0)
	t(r, -1.75)
	q, r = divmod(-r4p, -r3p)
	t(q, 1.0)
	t(r, -1.5)

	# Not testing mod (%) since it calls divmod to do it's work.

	t(pow(r2, r2), 4)
	t(pow(-r2, r2), 4)
	t(pow(r2, -r2), 0.25)
	t(pow(-r2, -r2), 0.25)
	t(pow(r2, r5), 32)
	t(pow(-r2, r5), -32)
	t(pow(r2, -r5), 1.0/32)
	t(pow(-r2, -r5), -1.0/32)
	t(pow(r4, rat(5, 2)), 32)
	t(pow(r4, -rat(5, 2)), 1.0/32)
	t(pow(r4, rat(2, 5)), pow(4, 2.0/5), 1e-6)
	t(pow(r4, -rat(2, 5)), pow(4, -2.0/5), 1e-6)

	# This is getting boring...

	# Following operators: ~ & | ^ << >> oct() hex()
	# Are correct by inspection of code.

	# __hash__ = hash((self.n, self.d)) is correct by inspection.

	# __coerce__ is correct by inspection and thus
	# __rop__ == __op__ for op in (add, mull, and, or, xor)
	# are correct as well.

	# A subtle error creeps in (you can see it in surd.py)
	# when the non-commutative operators: - / divmod() % pow()
	# are defined as __rop__ = __op__

	t(r5 - 2, 5 - r2)
	t(r5 / 2, 5 / r2)
	q, r = divmod(r7, 5)
	rq, rr = divmod(7, r5)
	t(q, rq)
	t(r, rr)
	t(pow(r5, 2), pow(5, r2))

	# Same thing happens with << and >> but that code
	# is correct by inspection.

	#
	# Comparison
	#
	a = rat(3, 4)
	b = -a
	c = rat(1, 3)
	if not b < c < a: killrat('not '+`b`+' < '+`c`+' < '+`a`)
	if a == b: killrat(`a`+' == '+`b`)
	if a == c: killrat(`a`+' == '+`c`)
	if a != a: killrat(`a`+' == '+`a`)
	if a < a: killrat(`a`+' < '+`a`)
	if a < b: killrat(`a`+' < '+`b`)
	if a < c: killrat(`a`+' < '+`c`)
	if a > a: killrat(`a`+' > '+`a`)
	if b > c: killrat(`b`+' > '+`c`)
	if a <= b: killrat(`a`+' <= '+`b`)
	if a <= c: killrat(`a`+' <= '+`c`)
	if b >= c: killrat(`b`+' >= '+`c`)

	#
	# Representation
	#
	def r(a, b):
		if a != b:
			raise 'DeadRat', a+" != "+b

	ra = rat(1, 2)
	rb = rat(1, 2, 3)
	r(r0.frac(), 'Rat(0)')
	r(r0.frac(str), '0')
	r(r0.ratio(), 'Rat(0, 1)')
	r(r0.ratio(str), '0/1')
	r((-r0).frac(), 'Rat(0)')
	r((-r0).frac(str), '0')
	r((-r0).ratio(), 'Rat(0, 1)')
	r((-r0).ratio(str), '0/1')
	
	r(r3.frac(), 'Rat(3)')
	r(r3.frac(str), '3')
	r(r3.ratio(), 'Rat(3, 1)')
	r(r3.ratio(str), '3/1')
	r((-r3).frac(), '-Rat(3)')
	r((-r3).frac(str), '-3')
	r((-r3).ratio(), '-Rat(3, 1)')
	r((-r3).ratio(str), '-3/1')

	r(ra.frac(), 'Rat(1, 2)')
	r(ra.frac(str), '1/2')
	r(ra.ratio(), 'Rat(1, 2)')
	r(ra.ratio(str), '1/2')
	r((-ra).frac(), '-Rat(1, 2)')
	r((-ra).frac(str), '-1/2')
	r((-ra).ratio(), '-Rat(1, 2)')
	r((-ra).ratio(str), '-1/2')

	r(rb.frac(), 'Rat(1, 2, 3)')
	r(rb.frac(str), '1+2/3')
	r(rb.ratio(), 'Rat(5, 3)')
	r(rb.ratio(str), '5/3')
	r((-rb).frac(), '-Rat(1, 2, 3)')
	r((-rb).frac(str), '-(1+2/3)')
	r((-rb).ratio(), '-Rat(5, 3)')
	r((-rb).ratio(str), '-5/3')

	print 'OK'

#
# These other tests taken from other Rational modules.
#

# These tests were taken from Rat.py.
def tests_from_ratpy():
        print Rat(-1L, 1)
        print Rat(1, -1)
        a = Rat(1, 10)
        print int(a), long(a), float(a)
        b = Rat(2, 5)
        l = [a+b, a-b, a*b, a/b]
        print l
        l.sort()
        print l
        print Rat(0, 1)
        print a+1
        print a+1L
        print a+1.0
        try:
                print Rat(1, 0)
                raise SystemError, 'should have been ZeroDivisionError'
        except ZeroDivisionError:
                print 'OK'


# These were taken from surd.py.  Minor modification on float arguments
# to constructor and hash tests.  Surd has hash = hash(`surd`) while
# Rat has hash = hash((num, den)).  Also get TypeError on __call__ and
# float approximation is handled differently.

surd = Rat

def tests_from_surdpy():
	SurdTestError = 'SurdTestError'

	def test_error ():
		raise SurdTestError

	def test_driver ():
		
		print 'testing surd ...'

		# Instantiation tests.
		a = surd () # Create without arguments
		if a != 0: test_error ()
		b = surd(10) # Create with just numerator.
		if b != 10: test_error ()
		c = surd (145, 15) # Create with explicit num & denom
		if c != surd (145, 15): test_error ()

		ra = surd (3.2)
		if ra != surd (32, 10): test_error ()
		rb = surd (12.0) / surd(2)
		if rb != surd (6, 1): test_error ()
		rc = surd (1045.2) / surd(2.5)
		if rc != surd (10452, 25): test_error ()
		rd = surd (12000) / surd(.05)
		if rd != surd (240000): test_error ()

		# Test GCD reduction.
		if (a + surd (29, 3)) != c: test_error ()

		# Arithmetic tests.
		r = b + c
		if r != surd (59, 3): test_error ()
		r = b * c
		if r != surd (290, 3): test_error ()
		r = b - c
		if r != surd (1, 3): test_error ()
		r = b / c
		if r != surd (30, 29): test_error ()
		r = -c
		if r != surd (-29, 3): test_error ()

		if c + 4 != surd (41, 3): test_error ()
		if c * 3 != surd (87, 3): test_error ()
		if c - 24 != surd (-43, 3): test_error ()
		if c / 13 != surd (29, 39): test_error ()

		# Comparison tests.
		if a == b: test_error ()
		if b < c: test_error ()
		if c < a: test_error ()
		if b == c: test_error ()
		if c != surd (290, 30): test_error ()
		if -b >= a: test_error ()
		
		# Sanity (div by zero) tests.
		try:
			z = surd (4, 0)
		except ZeroDivisionError:
			pass
		else:
			test_error ()

		try:
			z1 = surd (4)
			z2 = surd () # 0/1
			z = z1 / z2
		except ZeroDivisionError:
			pass
		else:
			test_error ()

		# Hash tests

		if hash (a) != hash ((0L,1L)): test_error ()
		if hash (b) != hash ((10L,1L)): test_error ()
		if hash (c) != hash ((29L,3L)): test_error ()
		if hash (c) == hash (b): test_error ()
		if hash (c) == hash (a): test_error ()
		if hash (c) == hash (-c): test_error ()
		# Sign should always go on numerator ...
		if hash (surd (4, -3)) != hash ((-4L,3L)): test_error ()
		if hash (surd (-14, -3)) != hash ((14L,3L)): test_error ()

		# Not defined for Rat. -ljr
		# Call tests.
		#if a(): test_error ()
		#if b(): test_error ()
		#if c(): test_error ()

		# Math function tests. (Not by any means exhausive, but I 
		# believe representative.
		m = surd (pow (13.2, 2.5))
		if abs(float(m) - math.pow (13.2, 2.5)) > 1e-6 : test_error ()
		m = surd (math.sin (30))
		if abs(float(m) - math.sin (30)) > 1e-6: test_error ()

		# If we made it here we passed every test.
		print 'all surd tests passed.'

		# B E N C H M A R K S
		print 'timing tests...'

		# Addition.
		start_time = time.time ()
		a = surd ()
		for i in range (0, 1000):
			a = a + surd (4, 3)
		print '1000 additions in ', time.time () - \
			start_time, 'seconds'

		# Subtraction.
		start_time = time.time ()
		a = surd (10)
		for i in range (0, 1000):
			a = a - surd (4, 3)
		print '1000 subtractions in ', time.time () - \
			start_time, 'seconds'

		# Multiplication.
		start_time = time.time ()
		a = surd (3.2)
		b = surd (2.1)
		for i in range (0, 1000):
			c = a * b
		print '1000 multiplications in ', time.time () - \
			start_time, 'seconds'

		# Division.
		start_time = time.time ()
		a = surd (4.2)
		b = surd (2.1)
		for i in range (0, 1000):
			c = a / b
		print '1000 divisions in ', time.time () - \
			start_time, 'seconds'

	# Call surd.py's tests.
	test_driver()


#
# Call the tests.
#
print "Testing yarn.Rat"
tests_for_yarnpy()

print
print "Running Rat.py's tests."
tests_from_ratpy()

print
print "Running surd.py's tests."
tests_from_surdpy()
