import ctypes
import time

lib = ctypes.CDLL("./libadd.so")
N = 1_000_000

start = time.perf_counter()
for i in range(N):
    x = i + 1
py_time = time.perf_counter() - start

start = time.perf_counter()
for i in range(N):
    x = lib.add(i, 1)
c_time = time.perf_counter() - start

print(f"pure Python: {py_time:.3f} s")
print(f"ctypes C:    {c_time:.3f} s")
print(f"ratio:       {c_time / py_time:.1f}x")