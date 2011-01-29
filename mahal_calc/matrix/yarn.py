# yarn.py - Yet Another Rational Number module
# Written by Lanny Ripple (8 February 1996).
#
# Use it, abuse it, make it write bad checks.  Just don't say
# you wrote it (or hold me responsible for the bad checks). -ljr
#
# Look at yarn.__doc__ and yarn.Rat.__doc__ for documentation.

"""Provide support for Rational numbers.

Imports:
	import math
	import types

Functions:
	sign(a)		Return `a' < 0 ? -1 : 1

	gcd(a, b)	Return GCD of `a' and `b'.

	rcon(s, f, n, d)
			Return ratio given a fraction.

	rext(n, d)	Return fraction given `num' and `den'.

	rff(n, p)	Return ratio that approximates float `n' to `p'
			decimals.  `P' defaults to Rat.Precision.

	ril(x)		Return `x' as integer if possible, long otherwise.

	ratrepr(n, d, mode)
			Return repr() of rational given `mode' information.
			Represents fraction when `mode'=TRUE, ratio otherwise.

	ratstr(n, d, mode)
			Return str() of rational given `mode' information.
			Represents fraction when `mode'=TRUE, ratio otherwise.

Classes:
	class Rat	Provide interface to Rational numbers.
"""

import math
import types

ZeroDenominator = 'denominator == 0'

#
# Support functions for class Rat.
#

def sign(a):
	"""Return -1 if ARG < 0, 1 otherwise.
	"""
	return a < 0 and -1 or 1

def gcd(a, b):
	"""Return GCD of two numbers.  Duh!
	"""
	while b:
		a, b = b, a % b
	return a

def rcon(s, f, n, d):
	"""Return ratio given fraction.
	"""
	# Impossible
	if d == 0: raise ZeroDivisionError, ZeroDenominator
	# Calculate
	f, n, d = long(f), long(n), long(d)
	g = gcd(n, d)
	n, d = n / g, d / g
	return s * (f*d + n), d

def rext(n, d):
	"""Return fraction given ratio.
	"""
	# Impossible
	if d == 0: raise ZeroDivisionError, ZeroDenominator
	# Calculate
	n, d = long(n), long(d)
	g = gcd(n, d)
	n, d = n / g, d / g
	s, n = sign(n), abs(n)
	return s, n / d, n % d, d

def rff(n, p = 0):
	"""Return rational approximation of ARG1 to ARG2 decimal precision.
	"""
	if p == 0: p = Rat.Precision
	s, n = sign(n), math.fabs(n)
	r, q = math.modf(n)
	f, p = r, math.pow(10, -p) * 0.5
	a, b = 1L, 0L
	while abs(math.floor(r*a+0.5)-r*a) >= p*a:
		f, i = math.modf(1.0/f)
		a, b = long(i) * a + b, a
	return s * (long(q) * a + long(math.floor(r*a+0.5))), a

def ril(x):
	"""Return int(ARG) if possible, ARG otherwise.

	ril = _R_epresent _I_nteger or _L_ong
	"""
	try:
		return int(x)
	except OverflowError:
		return x

def ratrepr(sn, sd, mode):
	"""Return repr(Rat) based on mode.
	"""
	s, f, n, d = rext(sn, sd)
	sn, sd = ril(abs(sn)), ril(sd)
	s = s < 0 and "-" or ""
	if mode or f == 0L and sd != 1:
		return "%sRat(%s, %s)" % (s, sn, sd)
	if sd == 1:
		return "%sRat(%s)" % (s, sn)
	f, n, d = ril(f), ril(n), ril(d)
	return "%sRat(%s, %s, %s)" % (s, f, n, d)

def ratstr(sn, sd, mode):
	"""Return str(Rat) based on mode.
	"""
	s, f, n, d = rext(sn, sd)
	sn, sd = ril(sn), ril(sd)
	if mode or f == 0L and sd != 1:
		return "%s/%s" % (sn, sd)
	if sd == 1:
		return str(sn)
	f, n, d = ril(f), ril(n), ril(d)
	if s < 0:
		return "-(%s+%s/%s)" % (f, n, d)
	return "%s+%s/%s" % (f, n, d)

#
# Do something to make above functions useful.
#

class Rat:
	"""Implement rational numbers.

	Expected Usage:
		from yarn import Rat

	Class Attributes:
		Private
		-------
				None.

		Public
		------
		Precision	Default decimal precision when approximating
				floating point values. (Default: 6)

		RatioRepr	Boolean value determining how to display the
				class with repr() or str().  If TRUE the class
				will be displayed using format: num/den.
				If FALSE then display is as a fraction of the
				form: factor+num/den.  (Default: 0)

	Instance Attributes:
		Private
		-------
		n		Numerator as a long.

		d		Denominator as a long.

		Public
		------
		ratio_repr	Takes precedence over Rat.RatioRepr in
				determining display format.  (To restore
				precedence of Rat.RatioRepr del ratio_repr
				from instance.)

	Methods:
		Private (Implemented in module namespace.)
		-------
		See yarn.__doc__

		Public (Instance methods)
		------
		*special*	All special methods that make sense are defined.
				(Note: Some special methods are only defined
				when the instance represents an integral value.)

		Constructor:	Instance represents:
		Rat()		0
		Rat(i)		i
		Rat(i, j)	i / j
		Rat(i, j, k)	i*k+j / k	(The fraction: i + j / k)
		Rat(x)		Approx of `x' to `Rat.Precision' decimals.
		Rat(x, n)	Approx of `x' to `n' decimals.

		modf()		Return "float" and "integer" parts of instance.

		frac(func)	Represent instance as a fraction.  `Func' may be
				repr or str (defaults to repr) and calls the
				appropriate method to provide the return value. 

		ratio(func)	Represent instance as a ratio.  `Func' has same
				meaning as in frac().

				Example:
					x = Rat(5, 2) (also: Rat(2, 1, 2))
					x             --> 'Rat(2, 1, 2)'
					str(x)        --> '2+1/2'
					x.ratio()     --> 'Rat(5, 2)'
					x.ratio(str)  --> '5/2'

	Notes, Suprises, Bugs:
		The sign of Rat(f, n, d) is sign(f)*sign(n)*sign*(d).  This is
		probably at odds with the definition that f, n, d represents
		f + n/d.

		Many of the special methods that depend on a binary represent-
		ation (e.g., &, >>, hex(), etc.) will raise TypeError exceptions
		if the args do not represent integral values (i.e., self.d != 1)

		This implementation depends on long() math being efficient.  My 
		first implementation used a fractional representation but was
		not as clean as using num/den.  It did have the nice property
		that 0 <= num < den for any simplified fraction. (This becomes
		more important (IMHO) when long() math is not available.)

		Python does not use a Public/Private encapsulation scheme for
		classes.  In this document public/private refer to expected
		(read "expected by me", not necessarily by a user) usage.
	"""

	Precision = 6
	RatioRepr = 0

	def __init__(self, *args):
		"""Instantiate based on arguments.

		Rat()             = 0/1
		Rat(i)            = i/1
		Rat(i,j)          = i/j
		Rat(i,j,k)        = (i*k + j)/k
		Rat(x) = Rat(x,6) = approx of x to Rat.Precision decimals
		Rat(x,n)          = approx of x to n decimals
		"""
		c = len(args)
		if c == 0:
			self.n, self.d = 0L, 1L
		elif type(args[0]) == types.FloatType:
			self.n, self.d = apply(rff, args)
		elif c == 1:
			self.n, self.d = long(args[0]), 1L
		elif c == 2:
			n, d = long(args[0]), long(args[1])
			if not d:
				raise ZeroDivisionError, ZeroDenominator
			g = gcd(n, d)
			self.n, self.d = n / g, d / g
		elif c == 3:
			s = reduce(lambda n,m: n*m,
				   map(lambda n: sign(n), args), 1)
			[f, n, d] = map(lambda n: abs(n), args)
			self.n, self.d = rcon(s, f, n, d)
		else:
			raise TypeError, "too many arguments"

	def __hash__(self):
		return hash((self.n, self.d))

	def __coerce__(self, other):
		t = type(other)
		if (t == types.FloatType or t == types.LongType or
		    t == types.IntType):
			return self, Rat(other)
		if (t == types.InstanceType and
		    self.__class__ == other.__class__):
			return self, other
		raise TypeError, 'Rat.__coerce__: bad other arg'

	def __cmp__(self, other):
		a = self.n  * other.d
		b = other.n * self.d
		if a < b: return -1
		if a > b: return 1
		return 0

	#
	# Display
	#
	def __repr__(self):
		try:
			mode = self.ratio_repr
		except:
			mode = Rat.RatioRepr
		return ratrepr(self.n, self.d, mode)

	def __str__(self):
		try:
			mode = self.ratio_repr
		except:
			mode = Rat.RatioRepr
		return ratstr(self.n, self.d, mode)

	#
	# Casts
	#
	def __int__(self):
		return int(float(self))

	def __long__(self):
		return long(float(self))

	def __float__(self):
		# Done this way to get (possibly) smaller n.
		# (Seems to be faster than num / den too.)
		s, f, n, d = rext(self.n, self.d)
		return s * (f + float(n) / d)

	#
	# Math
	#
	def __pos__(self):
		return self

	def __neg__(self):
		return Rat(-self.n, self.d)

	def __abs__(self):
		return Rat(abs(self.n), self.d)

	def __add__(self, other):
		return Rat(self.n * other.d + other.n * self.d,
			   self.d * other.d)

	def __sub__(self, other):
		return Rat(self.n * other.d - other.n * self.d,
			   self.d * other.d)

	def __mul__(self, other):
		return Rat(self.n * other.n, self.d * other.d)


	def __div__(self, other):
		if other.n == 0L:
			raise ZeroDivisionError, "rational division or modulo"
		return Rat(self.n * other.d, self.d * other.n)


	def __divmod__(self, other):
		a = self.__div__(other)
		r, q = a.modf()
		if r < 0:
			r = r + 1
			q = q - 1
		return q, r.__mul__(other)

	def __mod__(self, other):
		q, r = self.__divmod__(other)
		return r

	def __pow__(self, other):
		if other.d != 1L:
			return Rat(math.pow(float(self), float(other)))
		s, n = sign(other.n), abs(other.n)
		if s < 0:
			return Rat(pow(self.d, n), pow(self.n, n))
		return Rat(pow(self.n, n), pow(self.d, n))

	#
	# Rhs math (unfortunately not all operators are commutative)
	#
	__radd__ = __add__
	__rmul__ = __mul__
	def __rsub__(self, other):
		return other.__sub__(self)
	def __rdiv__(self, other):
		return other.__div__(self)
	def __rmod__(self, other):
		return other.__mod__(self)
	def __rdivmod__(self, other):
		return other.__divmod__(self)
	def __rpow__(self, other):
		return other.__pow__(self)

	#
	# Boolean testing.
	#
	def __nonzero__(self):
		if self.n: return 1
		return 0

	#
	# Methods dealing with binary representation.
	#
	def __oct__(self):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L:
			return oct(self.n)
		else: 
		    raise TypeError, "oct() argument can't be converted to oct"

	def __hex__(self):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L:
			return hex(self.n)
		else: 
		    raise TypeError, "hex() argument can't be converted to hex"

	def __invert__(self):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L:
			return Rat(~ self.n)
		else:
			raise TypeError, "bad operand type(s) for unary ~"

	def __and__(self, other):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L and other.d == 1L:
			return Rat(self.n & other.n)
		else:
			raise TypeError, "bad operand type(s) for &"

	def __or__(self, other):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L and other.d == 1L:
			return Rat(self.n | other.n)
		else:
			raise TypeError, "bad operand type(s) for |"

	def __xor__(self, other):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L and other.d == 1L:
			return Rat(self.n ^ other.n)
		else:
			raise TypeError, "bad operand type(s) for ^"

	def __lshift__(self, other):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L and other.d == 1L:
			return Rat(self.n << other.n)
		else:
			raise TypeError, "bad operand type(s) for <<"

	def __rshift__(self, other):
		"""Only defined if arguments represent integral types.
		"""
		if self.d == 1L and other.d == 1L:
			return Rat(self.n >> other.n)
		else:
			raise TypeError, "bad operand type(s) for <<"

	#
	# Rhs binary (unfortunately not all operators are commutative)
	#
	__rand__ = __and__
	__ror__  = __or__
	__rxor__ = __xor__
	def __rlshift__(self, other):
		return other.__lshift__(self)
	def __rrshift__(self, other):
		return other.__rshift__(self)

	#
	# Generate a type error on calling these.
	#
	def __call__(self, *args):
		raise TypeError, "call of non-function"
	def __len__(self):
		raise TypeError, "len() of unsized object"
	def __getitem__(self, i):
		raise TypeError, "unsubscriptable object"
	def __setitem__(self, i, v):
		raise TypeError, "can't assign to this subscripted object"
	def __delitem__(s, i):
		raise TypeError, "can't assign to this subscripted object"
	def __getslice__(s, i, j):
		raise TypeError, "only sequences can be sliced"
	def __setslice__(s, i, j, seq):
		raise TypeError, "assign to slice of non-sequence"
	def __delslice__(s, i, j):
		raise TypeError, "assign to slice of non-sequence"

	#
	# Public methods.
	#
	def modf(self):
		"""Return "float" and "integer" parts.
		"""
		# math.modf() = tuple(map(lambda n: float(n), self.modf()))
		s, f, n, d = rext(self.n, self.d)
		return Rat(n, s * d), Rat(s * f)

	def frac(self, mode=repr):
		"""Display Rat as a fraction: factor+num/den.
		"""
		# Code like this is why comments were invented.
		# Save ratio_repr, assign new value, get str, if ratio_repr
		# didn't exist then del, otherwise restore value.
		try:
			try:
				old_val = self.ratio_repr
			finally:
				self.ratio_repr = 0
				str = mode(self)
		except AttributeError:
			del self.ratio_repr
		else:
			self.ratio_repr = old_val
		return str

	def ratio(self, mode=repr):
		"""Display rat as a ratio: num/den.
		"""
		# Code like this is why comments were invented.
		# Save ratio_repr, assign new value, get str, if ratio_repr
		# didn't exist then del, otherwise restore value.
		try:
			try:
				old_val = self.ratio_repr
			finally:
				self.ratio_repr = 1
				str = mode(self)
		except AttributeError:
			del self.ratio_repr
		else:
			self.ratio_repr = old_val
		return str
