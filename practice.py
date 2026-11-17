import dis
import sys
ctypes.CDLL("./libadd.so")

#int size in Python
"""
print(sys.getsizeof(5))
"""

#Bytecode for addition 
"""
print(dis.dis("c = a + b"))
"""

#Testing expansion
print(sys.getsizeof(2**30))
print(sys.getsizeof(2**100))

