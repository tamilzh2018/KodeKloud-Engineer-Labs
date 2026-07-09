#Operators are used to perform operations on variables and values.
#Arithmetic operators are used with numeric values to perform common mathematical operations:
""" 
+	Addition	x + y	
-	Subtraction	x - y	
*	Multiplication	x * y	
/	Division(returns a float)	x / y	
%	Modulus((returns remainder)	x % y	
**	Exponentiation	x ** y	
//	Floor division(returns an integer)	x // y 
"""
#Assignment operators are used to assign values to variables:
""" 
=	x = 5	x = 5	
+=	x += 3	x = x + 3	
-=	x -= 3	x = x - 3	
*=	x *= 3	x = x * 3	
/=	x /= 3	x = x / 3	
%=	x %= 3	x = x % 3	
//=	x //= 3	x = x // 3	
**=	x **= 3	x = x ** 3	
&=	x &= 3	x = x & 3	
|=	x |= 3	x = x | 3	
^=	x ^= 3	x = x ^ 3	
>>=	x >>= 3	x = x >> 3	
<<=	x <<= 3	x = x << 3 
"""
#Comparison operators are used to compare two values:
""" 
==	Equal	x == y	
!=	Not equal	x != y	
>	Greater than	x > y	
<	Less than	x < y	
>=	Greater than or equal to	x >= y	
<=	Less than or equal to	x <= y 
"""

#Logical operators are used to combine conditional statements:
""" 
and Returns True if both statements are true	x < 5 and  x < 10	
or	Returns True if one of the statements is true	x < 5 or x < 4	
not	Reverse the result, returns False if the result is true	not(x < 5 and x < 10) 
"""

#Identity operators are used to compare the objects, not if they are equal, but if they are actually the same object, with the same memory location:
""" 
is 	Returns True if both variables are the same object	x is y	
is not	Returns True if both variables are not the same object	x is not y 
"""

#Membership operators are used to test if a sequence is presented in an object:
""" 
in 	Returns True if a sequence with the specified value is present in the object	x in y	
not in	Returns True if a sequence with the specified value is not present in the object	x not in y 
"""
#Operator precedence describes the order in which operations are performed.If two operators have the same precedence, the expression is evaluated from left to right.
"""
()	Parentheses	
**	Exponentiation	
+x  -x  ~x	Unary plus, unary minus, and bitwise NOT	
*  /  //  %	Multiplication, division, floor division, and modulus	
+  -	Addition and subtraction	
<<  >>	Bitwise left and right shifts	
&	Bitwise AND	
^	Bitwise XOR	
|	Bitwise OR	
==  !=  >  >=  <  <=  is  is not  in  not in 	Comparisons, identity, and membership operators	
not	Logical NOT	
and	AND	
or	OR


"""