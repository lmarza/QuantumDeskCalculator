from qiskit import *
from operations import addition, subtraction, multiplication, division
from utils import bcolors, selectOperator, checkOperation, printResult
import math


if __name__ == "__main__":
    print(bcolors.OKGREEN + '##########################################' + bcolors.ENDC)
    print(bcolors.OKGREEN + '#######  Quantum Desk Calculator  ########' + bcolors.ENDC)
    print(bcolors.OKGREEN + '##########################################'+ bcolors.ENDC)

    # take the operator and check
    operator = selectOperator()
    

    input1 = int(input(bcolors.WARNING + "Enter a first positive integer between 0 and 2047:\n" + bcolors.ENDC))
    input2 = int(input(bcolors.WARNING + "Enter a second positive integer between 0 and 2047:\n" + bcolors.ENDC))


    # check the inputs
    while (input1 < 0 or input1 > 2047) or (input2 < 0 or input2 > 2047):
        if input1 < 0 or input1 > 2047:
            print(bcolors.FAIL + "Invalid first input number" + bcolors.ENDC)
            input1 = int(input(bcolors.WARNING + "Enter a first positive integer between 0 and 2047:\n" + bcolors.ENDC))

        if input2 < 0 or input2 > 2047:
            print(bcolors.FAIL + "Invalid second input number" + bcolors.ENDC)
            input2 = int(input(bcolors.WARNING + "Enter a second positive integer between 0 and 2047:\n" + bcolors.ENDC))

    #check if the operation is valid
    checkOperation(input1, input2, operator)


    first = '{0:{fill}3b}'.format(input1, fill='0')
    second = '{0:{fill}3b}'.format(input2, fill='0')
    # for multiplication
    firstDec = input1
    secondDec = input2

    l1 = len(first)
    l2 = len(second)

    # Making sure that 'first' and 'second' are of the same length 
    # by padding the smaller string with zeros

    if operator == '+' or operator == '-' or operator == '/':
        if l2>l1:
            first,second = second, first
            l2, l1 = l1, l2
        second = ("0")*(l1-l2) + second
        n = l1

    elif operator == '*' :
        # Padding 'first' the same lenght of 'result'
        # since result can have at max len(first) + len(second) bits when multiplying
        first = ("0")*(l2) + first
        n = l1+l2


    print()
    print(bcolors.OKCYAN + '#'*150 + bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + 'You want to perform the following operation:'+ bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + f'{input1} {operator} {input2} --> {first} {operator} {second} = ...' + bcolors.ENDC)


    # create the register based on the operation choosen
    if operator == '+' or operator == '-' or operator == '*':
        a = QuantumRegister(n+1, "a") 
        b = QuantumRegister(n+1, "b")     
        cl = ClassicalRegister(n+1, "cl") 
        qc = QuantumCircuit(a, b, cl, name="qc")

        # Flip the corresponding qubit in register a if a bit in the string first is a 1
        for i in range(n):
            if first[i] == "1":
                qc.x(a[n-(i+1)])

        if operator != '*':
            # Flip the corresponding qubit in register b if a bit in the string second is a 1
            for i in range(n):
                if second[i] == "1":
                    qc.x(b[n-(i+1)])

        if operator == '+':
            addition.add(a,b,qc)
            printResult(first, second, qc,a, cl, n, operator)
        
        elif operator == '-':
            subtraction.sub(a,b,qc)
            printResult(first, second, qc,a, cl, n, operator)
        elif operator == '*':
            multiplication.multiply(a,secondDec,b,qc)
            printResult(first, second, qc, b, cl, n,operator)

    elif operator == '/':
        n = l1
        dividend = QuantumRegister(n+1, "dividend") 
        divisor = QuantumRegister(n+1, "divisor")
        accumulator = QuantumRegister(n+1, "accumulator")
        c_dividend = ClassicalRegister(n+1, "c_dividend") 
        circ = QuantumCircuit(dividend, divisor, accumulator, c_dividend, name="qc")

        # Flip the corresponding qubit in register a if a bit in the string first is a 1
        for i in range(n):
            if first[i] == "1":
                circ.x(dividend[n-(i+1)])

        # Flip the corresponding qubit in register b if a bit in the string second is a 1
        for i in range(n):
            if second[i] == "1":
                circ.x(divisor[n-(i+1)])

    
        division.div(dividend, divisor, accumulator,c_dividend, circ, 0)
        printResult(first, second, circ, accumulator, c_dividend, n,operator)



    print(bcolors.OKCYAN + '#'*150 + bcolors.ENDC)