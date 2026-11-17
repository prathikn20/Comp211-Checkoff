import ctypes
import time

import numpy as np

lib = ctypes.CDLL("./libsum.so")
N = 1_000_000

lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.sum_array.restype = ctypes.c_longlong

nums = list(range(N))

start = time.perf_counter()
total = 0
for x in nums:
    total += x
py_time = time.perf_counter() - start

start = time.perf_counter()
arr = (ctypes.c_int * N)(*nums)
build_time = time.perf_counter() - start

start = time.perf_counter()
result = lib.sum_array(arr, N)
c_time = time.perf_counter() - start

a = np.arange(N, dtype=np.int32)

np_times = []
for i in range(5):
    start = time.perf_counter()
    np_result = np.sum(a)
    np_times.append(time.perf_counter() - start)

print(f"pure Python loop:    {py_time:.4f} s  (sum = {total})")
print(f"build ctypes array:  {build_time:.4f} s")
print(f"lib.sum_array call:  {c_time:.4f} s  (sum = {result})")
for i, t in enumerate(np_times, start=1):
    print(f"np.sum call {i}:       {t:.6f} s  (sum = {np_result})")

d = np.arange(12, dtype=np.int32).reshape(3, 4)
print(d.dtype, d.shape, d.strides)