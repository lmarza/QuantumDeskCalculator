from qiskit import *
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def createInputState(qc, reg, n, pie):
    # Computes the quantum Fourier transform of reg, one qubit a time
    # Apply one Hadamard gate to the n-th qubit of the quantum register reg, and 
    # then apply repeated phase rotations with parameters being pi divided by 
    # increasing powers of two
    
    qc.h(reg[n])    
    for i in range(0, n):
        qc.cp(pie/float(2**(i+1)), reg[n-(i+1)], reg[n])    

def evolveQFTStateSum(qc, reg_a, reg_b, n, pie):
    # Evolves the state |F(ψ(reg_a))> to |F(ψ(reg_a+reg_b))> using the quantum 
    # Fourier transform conditioned on the qubits of the reg_b.
    # Apply repeated phase rotations with parameters being pi divided by 
    # increasing powers of two.
    
    for i in range(n+1):
        qc.cp(pie/float(2**(i)), reg_b[n-i], reg_a[n])


def evolveQFTStateSub(qc, reg_a, reg_b, n, pie):
    # Evolves the state |F(ψ(reg_a))> to |F(ψ(reg_a+reg_b))> using the quantum 
    # Fourier transform conditioned on the qubits of the reg_b.
    # Apply repeated phase rotations with parameters being pi divided by 
    # increasing powers of two.
    
    for i in range(n+1):
        qc.cp(-1*pie/float(2**(i)), reg_b[n-i], reg_a[n])


def inverseQFT(qc, reg, n, pie):
    # Performs the inverse quantum Fourier transform on a register reg.
    # Apply repeated phase rotations with parameters being pi divided by 
    # decreasing powers of two, and then apply a Hadamard gate to the nth qubit
    # of the register reg.
    
    for i in range(n):
        qc.cp(-1*pie/float(2**(n-i)), reg[i], reg[n])
    qc.h(reg[n])