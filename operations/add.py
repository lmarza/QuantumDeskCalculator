import math
from qiskit import *
from utils import bcolors

'''
qc: input quantum circuit
reg: input register to execute QFT
n: n-th qbit to apply hadamard and phase rotation
pie: pie number
'''
pie = math.pi

def createInputState(qc, reg, n, pie):
    # Computes the quantum Fourier transform of reg, one qubit a time
    # Apply one Hadamard gate to the n-th qubit of the quantum register reg, and 
    # then apply repeated phase rotations with parameters being pi divided by 
    # increasing powers of two
    
    qc.h(reg[n])    
    for i in range(0, n):
        qc.cp(pie/float(2**(i+1)), reg[n-(i+1)], reg[n])    

'''
qc: input quantum circuit
reg_a: first input register to execute QFT
reg_b: second input register to execute QFT
n: n-th qbit to apply hadamard and phase rotation
pie: pie number
'''
def evolveQFTState(qc, reg_a, reg_b, n, pie):
    # Evolves the state |F(ψ(reg_a))> to |F(ψ(reg_a+reg_b))> using the quantum 
    # Fourier transform conditioned on the qubits of the reg_b.
    # Apply repeated phase rotations with parameters being pi divided by 
    # increasing powers of two.
    
    for i in range(n+1):
        qc.cp(pie/float(2**(i)), reg_b[n-i], reg_a[n])

'''
qc: input quantum circuit
reg: input register to execute QFT
n: n-th qbit to apply hadamard and phase rotation
pie: pie number
'''        
def inverseQFT(qc, reg, n, pie):
    # Performs the inverse quantum Fourier transform on a register reg.
    # Apply repeated phase rotations with parameters being pi divided by 
    # decreasing powers of two, and then apply a Hadamard gate to the nth qubit
    # of the register reg.
    
    for i in range(n):
        qc.cp(-1*pie/float(2**(n-i)), reg[i], reg[n])
    qc.h(reg[n])
    
'''
first: first number to add
second: second number to add
n: lenght of both number (normalized to the same binary lenght)
a: first input register, representing the first number to add
a: second input register, representing the second number to add
cl: classical register, to read the result
qc: input quantum circuit
'''
def add(first, second, n, a, b, cl, qc):
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
        evolveQFTState(qc, a, b, n-i, pie) 
        
    # Compute the inverse Fourier transform of register a
    for i in range(n+1):
        inverseQFT(qc, a, i, pie)
        
    # Measure qubits
    for i in range(n+1):
        qc.measure(a[i], cl[i])
    
    # Execute using the local simulator
    '''
    # Set chosen backend and execute job
    num_shots = 100 #Setting the number of times to repeat measurement
    job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=num_shots)
    # Get results of program
    job_stats = job.result().get_counts()
    print(job_stats)
    '''

    # Execute using the IBM remote simulator
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connecting to IBM remote simulator...' + bcolors.ENDC)
    IBMQ.load_account()
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connect!' + bcolors.ENDC)
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')
    print(bcolors.BOLD + bcolors.OKCYAN + f'Running the experiment...' + bcolors.ENDC)
    counts = execute(qc, backend, shots=100).result().get_counts()
    print(bcolors.BOLD + bcolors.OKGREEN + f'The result of the operation {first} + {second} is {counts}' + bcolors.ENDC)