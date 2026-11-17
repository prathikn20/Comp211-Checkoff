import ctypes

lib = ctypes.CDLL("./libsum.so")
lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
# restype deliberately missing: ctypes assumes the C function returns a 32-bit int

N = 1_000_000
arr = (ctypes.c_int * N)(*range(N))
print("expected 499999500000, got:", lib.sum_array(arr, N))