# Author: Jose G. Perez <jperez50@miners.utep.edu>
# Last Date Modified: October 21, 2020
import numpy as np
import scipy.interpolate as interpolate

C = 2**100

#%% Interpolation
lerp1 = interpolate.interp1d(np.array([2**16, 2**32], dtype=np.float), np.array([0.9, 0.8], dtype=np.float), "linear")
lerp2 = interpolate.interp1d(np.array([2**32, 2**64], dtype=np.float), np.array([0.8, 0.7], dtype=np.float), "linear")
lerp3 = interpolate.interp1d(np.array([2**64, C], dtype=np.float), np.array([0.7, 0], dtype=np.float), "linear")


class ExperimentFunction:
    def __init__(self, t, desc):
        self.t = t
        self.desc = desc


def R(n):
    if n < 0:
        return 0
    elif n == 0:
        return 1
    elif 0 < n < 2**16:
        return 0.99
    elif n == 2**16:
        return 0.9
    elif 2**16 < n < 2**32:
        return lerp1(np.array([n], dtype=np.float))[0]
    elif n == 2**32:
        return 0.8
    elif 2**32 < n < 2**64:
        return lerp2(np.array([n], dtype=np.float))[0]
    elif n == 2**64:
        return 0.7
    elif 2**64 < n < C:
        return lerp3(np.array([n], dtype=np.float))[0]
    else:
        return 0


def D(n0, t):
    if n0 > 1:
        t1 = R(t(n0-1))
        t2 = 1 - R(n0)
        return min(t1, t2)
    else:
        return 1 - R(1)


def bisection(t):
    a = 0
    b = C
    prev_n = 0
    best_n = 0
    while True:
        n = ((a + b) / 2)
        if n <= 0 or abs(a-b) <= 1 or abs(n-prev_n) <= 0:
            #print(f"c1={n<=0} | c2={abs(a-b)<=1} | c3={abs(n-prev_n)<=0}")
            break

        lhs = R(t(n))
        rhs = 1 - R(n)

        #print(f"n={n:.3f}, lhs={lhs:.3f}, rhs={rhs:.3f}, D={D(n, t):.3f}")
        #print(f"D(t)={D(n,t):.20f}")
        if lhs <= rhs:
            #print(f"*** n0={n:.3f}")
            best_n = n
            b = n
        else:
            a = n

        prev_n = n
    return int(best_n)


print("========== Results ==========")

all_t = [
    ExperimentFunction(lambda n: 1, "Constant (1)"),
    ExperimentFunction(lambda n: 2**100, "Constant (2^100)"),
    ExperimentFunction(lambda n: n, "n"),
    ExperimentFunction(lambda n: n**2, "n^2"),
    ExperimentFunction(lambda n: 1/n, "1/n"),
    ExperimentFunction(lambda n: 1/(n**2), "1/(n^2)"),
    ExperimentFunction(lambda n: (10**12)*(n**2), "(10^12)n^2"),
]

for func in all_t:
    print(f"Function: t(n)={func.desc}")
    n0 = bisection(func.t)
    degree = D(n0, func.t)
    print(f"n0={n0}")
    print(f"Degree that t(n) is reasonable is {degree:.2f}={degree*100:.2f}%")
    print()