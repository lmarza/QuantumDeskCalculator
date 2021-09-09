import math
from qiskit import *
from utils import bcolors, createInputState, evolveQFTStateSum, inverseQFT

'''
qc: input quantum circuit
reg: input register to execute QFT
n: n-th qbit to apply hadamard and phase rotation
pie: pie number
'''
pie = math.pi
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
        evolveQFTStateSum(qc, a, b, n-i, pie) 
        
    # Compute the inverse Fourier transform of register a
    for i in range(n+1):
        inverseQFT(qc, a, i, pie)
        
    # Measure qubits
    for i in range(n+1):
        qc.measure(a[i], cl[i])
    
    # Execute using the local simulator
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connecting to local simulator...' + bcolors.ENDC)
    # Set chosen backend and execute job
    num_shots = 100 #Setting the number of times to repeat measurement
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connect!' + bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + f'Running the experiment on {num_shots} shots...' + bcolors.ENDC)
    job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=num_shots)
    # Get results of program
    job_stats = job.result().get_counts()
    print(bcolors.BOLD + bcolors.OKGREEN + f'The result of the operation {first} + {second} is {job_stats}' + bcolors.ENDC)
    
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
    '''