import math
from qiskit import *
from utils import bcolors, createInputState, evolveQFTStateSum, inverseQFT

pie = math.pi

def evolveState(second,n,qc,result,a):
    # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    # to |F(ψ((second * reg_a))>, where we loop on the sum as many times as 'second' says, 
    # doing incremental sums
    for j in range(second):
        for i in range(n+1):
            evolveQFTStateSum(qc, result, a, n-i, pie)

def multiply(first, second, n, a, result, cl, qc):
    # Flip the corresponding qubit in register a if a bit in the string first is a 1
    for i in range(n):
        if first[i] == "1":
            qc.x(a[n-(i+1)])

    # Compute the Fourier transform of register 'result'
    for i in range(n+1):
        createInputState(qc, result, n-i, pie)
    
    evolveState(second,n,qc,result,a)

    # Compute the inverse Fourier transform of register a
    for i in range(n+1):
        inverseQFT(qc, result, i, pie)

   