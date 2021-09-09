import math
from qiskit import *
from utils import bcolors, createInputState, evolveQFTStateSub, inverseQFT

'''
qc: input quantum circuit
reg: input register to execute QFT
n: n-th qbit to apply hadamard and phase rotation
pie: pie number
'''
pie = math.pi

'''
first: first number 
second: second number to subtract
n: lenght of both number (normalized to the same binary lenght)
a: first input register, representing the first number
a: second input register, representing the second number to subtract
cl: classical register, to read the result
qc: input quantum circuit
'''
def subtract(first, second, n, a, b, cl, qc):
    # Flip the corresponding qubit in register a if a bit in the string first is a 1
    for i in range(n):
        if first[i] == "1":
            qc.x(a[n-(i+1)])
    # Flip the corresponding qubit in register b if a bit in the string second is a 1
    for i in range(n):
        if second[i] == "1":
            qc.x(b[n-(i+1)])
            
    # Compute the Fourier transform of register a
    for i in range(n+1):
        createInputState(qc, a, n-i, pie)
        
    # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    # to |F(ψ(reg_a+reg_b))>
    for i in range(n+1):
        evolveQFTStateSub(qc, a, b, n-i, pie) 
        
    # Compute the inverse Fourier transform of register a
    for i in range(n+1):
        inverseQFT(qc, a, i, pie)
