import math
from qiskit import *
from utils import bcolors

pie = math.pi
def divide(dividend, divisor, accumulator,
           c_dividend, circ, cl_index):
    """
    Divide QuantumRegister dividend by QuantumRegister divisor, and store the
    product in QuantumRegister accumulator.
    """
    
    d = QuantumRegister(1)
    circ.add(d)
    circ.x(d[0])

    c_dividend_str = '0'

    while c_dividend_str[0] == '0':
        subtract.subtract(dividend, divisor, circ)
        add.add(accumulator, d, circ)
        for i in range(len(dividend)):
            circ.measure(dividend[i], c_dividend[i])
        result = execute(circ, backend=Aer.get_backend('qasm_simulator'),
                         shots=2).result()
        counts = result.get_counts("qc")
        c_dividend_str = list(counts.keys())[0].split()[cl_index]

    subtract.subtract(accumulator, d, circ)
    
    # Execute using the IBM remote simulator
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connecting to IBM remote simulator...' + bcolors.ENDC)
    IBMQ.load_account()
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connect!' + bcolors.ENDC)
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')
    print(bcolors.BOLD + bcolors.OKCYAN + f'Running the experiment...' + bcolors.ENDC)
    counts = execute(qc, backend, shots=100).result().get_counts()
    print(bcolors.BOLD + bcolors.OKGREEN + f'The result of the operation {first} - {second} is {counts}' + bcolors.ENDC)