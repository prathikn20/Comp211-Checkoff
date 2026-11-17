# Comp211-Checkoff
Exploring calling C functions from Python with ctypes to see when C can optimize Python code. 

## What's in here

- `add.c`: Library function that adds two integers.
- `sum.c`: Library function that sums n integers.
- `call_add.py`: Tests difference in time between regular Python addition and calling add with C.
- `bench_sum.py`: Benchmarked the time differences in looping and summing between regular Python, building a C array, and summing a NumPy array. 
- `fail_restype.py`: It doesn't define a result type to show truncation due to lost bits. 
- `fail_oob.py`: Shows that a try except can't catch errors stemming from the C function.  
- `practice.py`: Determining why C operations might be much faster than Python and looking at how Python ints are stored. 

## What I found

Numbers are from running Python 3.14 on Mac M4.

### Calling C in a loop
- Pure Python: 0.021 s
- ctypes `add`: 0.110 s (~5x slower)
- Why: The time difference is because ctypes needs to unwrap each Python object before it operates, making it take much longer even if the actual operation takes less time. 

### Summing a whole array
- Python loop: 0.0274 s
- Building the ctypes array: 0.0487 s
- `sum_array` call: 0.0002 s
- `np.sum`: ~0.00016 s
- Takeaway: Even though the C call is so much faster, it takes such a long time to build the ctypes array because it needs to get the int value from each of the 1,000,000 pointers. It's worth calling C only when each call does a lot of work and the data is either already converted or is already in C memory. 
- Why NumPy wins: NumPy writes directly into the buffer and so doesn't pay the same time cost as ctypes for a similar operation. The (16, 4) strides are evidence of this: each element is 4 bytes and each row is 16 bytes, all in one contiguous buffer, just like a C array.

### Missing `restype`
- Expected: 499,999,500,000
- Got: 1,783,293,664
- Why: This is because if you don't set a restype, ctypes assumes the function returns a 32-bit C int while the actual sum is too big for 32 bits. The C function returns a 64-bit long long; Python only reads the bottom 32 bits. 

### Out-of-bounds read
- Result: segfault, exit code 139
- `except` never runs
- Why: C doesn't do any bounds check, so the function sum_array trusts the n it gets and keeps reading past the size of the array into memory the process doesn't own. The operating system kills the process with a segmentation fault. The `except` doesn't stop it because Python exceptions exist inside the interpreter, but the crash happens in C, so the `except` never fires. 

## Running it

- Requirements: C compiler (Apple clang 21), Python 3.14, NumPy 2.4 (`pip install numpy`)
- Build:
  - `cc -shared -fPIC -o libadd.so add.c`
  - `cc -shared -fPIC -o libsum.so sum.c`
- Run:
  - `python3 call_add.py`
  - `python3 bench_sum.py`
  - `python3 fail_restype.py`
  - `python3 fail_oob.py` (segfaults on purpose; run `echo $?` after to see exit code 139)

## Stack

- NumPy, ctypes, sys, dis, time.perf_counter
