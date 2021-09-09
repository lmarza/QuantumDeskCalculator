import math
from qiskit import *
from utils import bcolors, createInputState, inverseQFT
from multiplication import evolveState

pie = math.pi
def pow(first, firstDec, second, n, a, result, cl, qc):
    # Flip the corresponding qubit in register a if a bit in the string first is a 1
    for i in range(n):
        if first[i] == "1":
            qc.x(a[n-(i+1)])

    if second != 0:
        # Compute the Fourier transform of register 'result'
        for i in range(n+1):
            createInputState(qc, result, n-i, pie)
        
        # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
        # to |F(ψ((second ** reg_a))>, where we loop on the sum as many times as 'second' says, 
        # doing incremental sums
        s = second
        for _ in range(s):
            evolveState(second,)

        # Compute the inverse Fourier transform of register a
        for i in range(n+1):
            inverseQFT(qc, result, i, pie)

        # Measure qubits
        for i in range(n+1):
            qc.measure(result[i], cl[i])
            
    else:
        qc.x(result[n-1])
    
    # Execute using the IBM remote simulator
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connecting to IBM remote simulator...' + bcolors.ENDC)
    IBMQ.load_account()
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connect!' + bcolors.ENDC)
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')
    print(bcolors.BOLD + bcolors.OKCYAN + f'Running the experiment...' + bcolors.ENDC)
    counts = execute(qc, backend, shots=100).result().get_counts()
    second = '{0:{fill}3b}'.format(second, fill='0')
    print(bcolors.BOLD + bcolors.OKGREEN + f'The result of the operation {first} ** {second} is {counts}' + bcolors.ENDC)