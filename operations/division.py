import math
from qiskit import *
from utils import bcolors, createInputState, evolveQFTStateSum, inverseQFT
from operations import addition, subtraction

pie = math.pi



def div(dividend, divisor, accumulator,c_dividend, circ, cl_index):
    d = QuantumRegister(1)
    circ.add_register(d)
    circ.x(d[0])

    c_dividend_str = '0'

    while c_dividend_str[0] == '0':
        subtraction.sub(dividend, divisor, circ)
        addition.add(accumulator, d, circ)

        for i in range(len(dividend)):
            circ.measure(dividend[i], c_dividend[i])

        result = execute(circ, backend=Aer.get_backend('qasm_simulator'),
                         shots=10).result()
 
        counts = result.get_counts("qc")
        #print(counts)
        c_dividend_str = list(counts.keys())[0] #.split()[0]
     

    subtraction.sub(accumulator, d, circ)