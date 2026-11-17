import ctypes

lib = ctypes.CDLL("./libsum.so")
lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.sum_array.restype = ctypes.c_longlong

N = 1_000_000
arr = (ctypes.c_int * N)(*range(N))
try:
    print(lib.sum_array(arr, 100_000_000))  # n is 100x the real length
except Exception as e:
    print("caught:", e)
print("this line runs after the call")