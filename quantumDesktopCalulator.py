from qiskit import *
from operations import add, sub
from utils import bcolors
import math

def selectOperator():
    valid_operators = ["+", "-", "*", "/", "**"]
    operator = input(bcolors.WARNING + "\nSelect one operator[+ addition, - subtraction, * multiplication, / division, ** power]:  " + bcolors.ENDC)
    
    # Check valid operator
    if not(operator in valid_operators):
        print(bcolors.FAIL + f"Invalid operator, you can choose between these: {valid_operators}" + bcolors.ENDC)
        quit()

    return operator


def checkOperation(input1, input2, operator):
    if operator == '-' and input1 < input2:
        print(bcolors.FAIL + f"Invalid operation, you are trying to subtract a larger number from a smaller one" + bcolors.ENDC)
        quit()
    
    if operator == '/' and input2 == 0:
        print(bcolors.FAIL + f"Invalid operation, division by 0 is not allowed" + bcolors.ENDC)
        quit()



if __name__ == "__main__":
    print(bcolors.OKGREEN + '##########################################' + bcolors.ENDC)
    print(bcolors.OKGREEN + '####### Quantum Desktop Calculator #######' + bcolors.ENDC)
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

    print()
    print(bcolors.OKCYAN + '#'*150 + bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + 'You want to perform the following operation:'+ bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + f'{input1} {operator} {input2} --> {first} {operator} {second} = ...' + bcolors.ENDC)
    

    l1 = len(first)
    l2 = len(second)

    # Making sure that 'first' and 'second' are of the same length 
    # by padding the smaller string with zeros
    if l2>l1:
        first,second = second, first
        l2, l1 = l1, l2
    second = ("0")*(l1-l2) + second
    n = l1

    # create the register based on the operation choosen
    pie = math.pi
    a = QuantumRegister(n+1, "a") 
    b = QuantumRegister(n+1, "b")     
    cl = ClassicalRegister(n+1, "cl") 
    qc = QuantumCircuit(a, b, cl, name="qc")

    if operator == '+':
        add.add(first,second,l1,a,b,cl,qc)
    elif operator == '-':
        sub.subtract(first,second,l1,a,b,cl,qc)

    print(bcolors.BOLD + bcolors.OKCYAN + 'Drawing the circuit...' + bcolors.ENDC)
    print(qc)
    print(bcolors.OKCYAN + '#'*150 + bcolors.ENDC)