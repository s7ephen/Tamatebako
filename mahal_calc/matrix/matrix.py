# -*- Mode: Python; tab-width: 4 -*-
#
#	Author: Sam Rushing <rushing@nightmare.com>
#
# One goal is to work with any object type that supports the numeric
# protocol.  (i.e., classes for rationals, complex or even matrices)
#
# Algorithms are from
# Cormen, Leiserson & Rivest, <Introduction to Algorithms>, Ch. 31
#
# Warning: ItoA thinks a[i,j] == a[row,column], whereas I
# think a[i,j] == a[column, row].  beware of arbitrary-seeming
# index-reversals!

# Note: I made a small change to yarn.py, in order to better accomodate
# this sort of thing:  yarn.Rat (Rat(1,3), Rat(1,4))
#
# 252c252,256
# <                       n, d = long(args[0]), long(args[1])
# ---
# >                       if ((type(args[0]) != types.InstanceType)
# >                           or self.__class__ != args[0].__class__):
# >                           n, d = long(args[0]), long(args[1])
# >                       else:
# >                           n, d = args[0], args[1]



class matrix:

	def __init__ (self, size=(3,3)):
		if (type(size) == type([])):
			# another option for creation
			self.v = size
		else:
			c, r = size
			rows = range(r)
			for i in range(r):
				rows[i] = [0]*c
			self.v = rows

	# --------------------------------------------------
	# mutation
	# --------------------------------------------------

	def size (self):
		"returns (columns, rows)"
		return len(self.v[0]), len(self.v)

	def __setitem__ (self, (x,y), v):
		self.v[y][x] = v

	set = __setitem__


	def __getitem__ (self, (x,y)):
		return self.v[y][x]

	get = __getitem__


	# --------------------------------------------------
	# iteration
	# --------------------------------------------------

	def iterate (self, f):
		nc, nr = self.size()
		for r in range(nr):
			for c in range(nc):
				f(c,r,self[c,r])

	def map (self, f):
		"self[c,r] = f (c,r,value)"
		nc, nr = self.size()
		for r in range(nr):
			for c in range(nc):
				self[c,r] = f(c,r,self[c,r])

	# --------------------------------------------------
	# properties
	# --------------------------------------------------

	def square (self):
		c,r = self.size()
		return c == r

	def _square_check (self):
		c,r = self.size()
		if (c != r):
			raise ValueError, "matrix must be square"

	def symmetric (self):
		return self == self.transpose()

	# must be square
	def determinant (self):
		c, r = self.size()
		self._square_check()
		if c == 2:
			try:
				return (self[0,0] * self[1,1]) - (self[0,1] * self[1,0])
			except OverflowError:
				return (long(self[0,0]) * self[1,1]) - (long(self[0,1]) * self[1,0])
		else:
			sum = 0
			f = 1
			for i in range(c):
				try:
					sum = sum + ((self[i,0]) * self.minor((i,0)).determinant() * f)
				except OverflowError:
					sum = sum + ((long(self[i,0]) * self.minor((i,0)).determinant() * f))
				f = -f
			return sum

	def singular (self):
		return not self.determinant()

	# --------------------------------------------------
	# operations
	# --------------------------------------------------

	def transpose (self):
		r,c = self.size()
		n = matrix ((c,r))
		self.iterate (
			lambda r,c,v,n=n: n.set ((c,r),v)
			)
		return n

	def __cmp__ (self, other):
		ss = self.size()
		os = other.size()
		if (ss != os):
			return 1
		else:
			# this does a 'deep' compare
			return not (self.v == other.v)

	def __neg__ (self):
		n = matrix(self.size())
		n.map (lambda c,r,v: -v)
		return n

	def __add__ (self, other):
		if (self.size() != other.size()):
			raise ValueError, "dimensions do not match"
		new = matrix (self.size())

		def adder (c,r,v,s=self,o=other,n=new):
			n[c,r] = v + o[c,r]

		self.iterate (adder)
		return new

	def __sub__ (self, other):
		return self + (-other)

	def __mul__ (self, other):
		ss = self.size()
		os = other.size()
		if (ss[0] != os[1]):
			raise ValueError, "dimensions do not match"
		new = matrix ((os[0],ss[1]))
		for i in range(os[0]):
			for j in range(ss[1]):
				sum = 0
				for k in range (ss[0]):
					sum = sum + (self[k,j] * other[i,k])
				new[i,j] = sum
		return new

	def scalar_multiply (self, factor):
		new = matrix (self.size())
		def multiplier (c,r,v,n=new,f=factor):
			n[c,r] = v * f

		self.iterate (multiplier)
		return new

	def copy (self):
		v = []
		for row in self.v:
			v.append (row[:])
		return matrix (v)

	def minor (self, (i,j)):
		nc,nr = self.size()
		n = self.copy()
		for nj in range(nr):
			row = n.v[nj]
			for ni in range(nc):
				if ni == i:
					del row[i]
		del n.v[j]
		return n

	def inverse (self):
		return inverse (self)

	# --------------------------------------------------
	# protocol
	# --------------------------------------------------

	def __repr__ (self):
		c,r = self.size()
		m = 0
		# find the fattest element
		for r in self.v:
			for c in r:
				#l = len(repr(c))
				l = len(str(c))
				if l > m:
					m = l
		f = '%%%ds' % (m+1)
		s = '<matrix'
		for r in self.v:
			s = s + '\n'
			for c in r:
				#s = s + (f % repr(c))
				s = s + (f % str(c))
		s = s + '>'
		return s

def vector (init):
	if type(init) == type(1):
		return matrix ((init,1))
	else:
		return matrix ([init])

def identity (n=3):
	new = matrix ((n,n))
	for i in range(n):
		new[i,i] = 1
	return new

def zero (r=3,c=3):
	return matrix ((r,c))

class piper:
	def __getattr__ (self, name):
		if name == 'Rat':
			import yarn
			return yarn.Rat
		else:
			raise AttributeError, name

# pretends to be a module
Rat = piper()

# --------------------------------------------------
# generate various types of matrices
# --------------------------------------------------

def hilbert (n=3):
	new = matrix ((n,n))
	new.map (lambda i,j,v: Rat.Rat(1,i+1+j))
	return new

def complex_index (n=3):
	new = matrix ((n,n))
	new.map (lambda c,r,v: complex(c,r))
	return new

def random_square (n=3,w=10):
	import random
	new = matrix((n,n))
	new.map (lambda c,r,v,w=w: random.randint (1,w))
	return new

def meta_random_square (n=3,w=10):
	new = matrix((n,n))
	new.map (lambda c,r,v,n=n,w=w: random_square (n,w))
	return new

# --------------------------------------------------
# solving simultaneous linear equations
# --------------------------------------------------

# l,u,p must be square, and the same size
# p is a permutation 'array', not really a matrix.
# [should we make it one for consistency?]

def lup_solve (l, u, p, b):
	n = l.size()[0]
	y = b.copy()
	# forward
	for i in range(n):
		sum = b[p[i],0]
		for j in range (i):
			sum = sum - (l[j,i] * y[j,0])
		y[i,0] = sum
	# backward
	x = vector(n)
	for i in range(n-1,-1,-1):
		sum = y[i,0]
		for j in range (i+1,n):
			sum = sum - (u[j,i] * x[j,0])
		x[i,0] = sum / u[i,i]
	return x

def test_lup_solve():
	a = matrix([[1,2,0],[3,5,4],[5,6,3]])
	l = matrix([[1,0,0],[0.6,1,0],[.2,0.571,1]])
	u = matrix([[5,6,3],[0,1.4,2.2],[0,0,-1.856]])
	p = [2,1,0]
	b = vector([0.1, 12.5, 10.3])
	# p*a == l*u
	print lup_solve (l,u,p,b)
	
# Gaussian elimintation, without pivoting.
def lu_decomposition (a, use_rational=1):
	a = a.copy()
	n = a.size()[0]
	u = identity (n)
	l = identity (n)
	for k in range(n):
		u[k,k] = a[k,k]
		for i in range (k+1,n):
			if use_rational:
				l[k,i] = Rat.Rat (a[k,i],u[k,k])
			else:
				l[k,i] = float(a[k,i]) / u[k,k]
			u[i,k] = a[i,k]
		for i in range (k+1,n):
			for j in range (k+1,n):
				a[j,i] = a[j,i] - (l[k,i] * u[j,k])
	return l,u,range(n)

# With pivoting.  [this is supposed to be more numerically stable,
# won't matter so much if you're using rationals]

def lup_decomposition (a, use_rational=1):
	a = a.copy()
	n = a.size()[0]
	# identity permutation
	p = range(n)
	for k in range(n-1):
		q = 0
		for i in range (k,n):
			aa = abs(a[k,i])
			if aa > q:
				q = aa
				k2 = i
		if not q:
			raise ValueError, "singular matrix"
		# swap rows
		p[k], p[k2] = p[k2], p[k]
		for i in range (n):
			a[i,k], a[i,k2] = a[i,k2], a[i,k]
		# divide by pivot
		for i in range (k+1,n):
			# use rats?
			if use_rational:
				a[k,i] = Rat.Rat(a[k,i],a[k,k])
			else:
				a[k,i] = float(a[k,i]) / a[k,k]
			for j in range (k+1,n):
				a[j,i] = a[j,i] - (a[k,i] * a[j,k])
	# create l and u from a
	l = identity (n)
	u = matrix ((n,n))
	for i in range(n):
		for j in range(n):
			if j > i:
				l[i,j] = a[i,j]				
			else:
				u[i,j] = a[i,j]
	return l,u,p

# example on pp. 753
# a = matrix([[1,2,0],[3,5,4],[5,6,3]])

# example on pp. 760
#a = matrix([[2,0,2,.6],[3,3,4,-2],[5,5,4,2],[-1,-2,3.4,-1]])


def solve (a,b,pivot=1):
	"return x such that Ax = b"
	if pivot:
		l,u,p = lup_decomposition (a)
	else:
		l,u,p = lu_decomposition (a)
	return lup_solve (l,u,p,b)

def lup_inverse (l,u,p):
	n = l.size()[0]
	new = matrix ((n,n))
	for j in range(n):
		# solve for each row, one at a time
		v = vector(n)
		v[j,0] = 1
		r = lup_solve (l,u,p,v)
		for i in range(n):
			new[j,i] = r[i,0]
	return new
		
def inverse (a):
	# for some reason this doesn't seem
	# to work right if I use lup_decomposition
	l,u,p = lu_decomposition(a)
	return lup_inverse (l,u,p)

