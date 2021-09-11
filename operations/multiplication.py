import math
from qiskit import *
from utils import bcolors, createInputState, evolveQFTStateSum, inverseQFT

pie = math.pi


def multiply(a, secondDec, result, qc):
    
    n = len(a) -1
    # Compute the Fourier transform of register 'result'
    for i in range(n+1):
        createInputState(qc, result, n-i, pie)
    
    # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    # to |F(ψ((second * reg_a))>, where we loop on the sum as many times as 'second' says, 
    # doing incremental sums
    for j in range(secondDec):
        for i in range(n+1):
            evolveQFTStateSum(qc, result, a, n-i, pie)

    # Compute the inverse Fourier transform of register a
    for i in range(n+1):
        inverseQFT(qc, result, i, pie)

   