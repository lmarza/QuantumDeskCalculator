import math
from qiskit import *
from utils import bcolors, createInputState, evolveQFTStateSub, inverseQFT

pie = math.pi

def sub(a, b, qc):
    
    n = len(a) 

    #Compute the Fourier transform of register a
    for i in range(0, n):
        createInputState(qc, a, n-(i+1), pie)
    #Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    #to |F(ψ(reg_a-reg_b))>
    for i in range(0, n):
        evolveQFTStateSub(qc, a, b, n-(i+1), pie) 
    #Compute the inverse Fourier transform of register a
    for i in range(0, n):
        inverseQFT(qc, a, i, pie)