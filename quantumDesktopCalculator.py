from qiskit import *
from operations import add, sub, multiplication, power
from utils import bcolors
import math

def selectOperator():
    valid_operators = ["+", "-", "*", "/", "**"]
    operator = input(bcolors.WARNING + "\nSelect one operator [+ addition, - subtraction, * multiplication, / division, ** power]:  " + bcolors.ENDC)
    
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

def printResult(first, second, qc,result, cl, n, operator):

    # Measure qubits
    for i in range(n+1):
        qc.measure(result[i], cl[i])

    # Execute using the local simulator
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connecting to local simulator...' + bcolors.ENDC)
    # Set chosen backend and execute job
    num_shots = 100 #Setting the number of times to repeat measurement
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connect!' + bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + f'Running the experiment on {num_shots} shots...' + bcolors.ENDC)
    job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=num_shots)
    # Get results of program
    job_stats = job.result().get_counts()
    print(bcolors.BOLD + bcolors.OKGREEN + f'The result of the operation {first} {operator} {second} is {job_stats}' + bcolors.ENDC)
   
    '''
    # Execute using the IBM remote simulator
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connecting to IBM remote simulator...' + bcolors.ENDC)
    IBMQ.load_account()
    print(bcolors.BOLD + bcolors.OKCYAN + 'Connect!' + bcolors.ENDC)
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')
    print(bcolors.BOLD + bcolors.OKCYAN + f'Running the experiment...' + bcolors.ENDC)
    counts = execute(qc, backend, shots=100).result().get_counts()
    second = '{0:{fill}3b}'.format(second, fill='0')
    print(bcolors.BOLD + bcolors.OKGREEN + f'The result of the operation {first} * {second} is {counts}' + bcolors.ENDC)
    '''


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
    # for multiplication
    firstDec = input1
    secondDec = input2

    l1 = len(first)
    l2 = len(second)

    # Making sure that 'first' and 'second' are of the same length 
    # by padding the smaller string with zeros

    if operator == '+' or operator == '-':
        if l2>l1:
            first,second = second, first
            l2, l1 = l1, l2
        second = ("0")*(l1-l2) + second
        n = l1

    elif operator == '*':
        # Padding 'first' the same lenght of 'result'
        # since result can have at max len(first) + len(second) bits when multiplying
        first = ("0")*(l2) + first
        n = l1+l2


    print()
    print(bcolors.OKCYAN + '#'*150 + bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + 'You want to perform the following operation:'+ bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKCYAN + f'{input1} {operator} {input2} --> {first} {operator} {second} = ...' + bcolors.ENDC)

    # create the register based on the operation choosen
    pie = math.pi
    a = QuantumRegister(n+1, "a") 
    b = QuantumRegister(n+1, "b")     
    cl = ClassicalRegister(n+1, "cl") 
    qc = QuantumCircuit(a, b, cl, name="qc")

    if operator == '+':
        add.add(first,second,n,a,b,cl,qc)
        printResult(first, second, qc,a, cl, n, operator)
    elif operator == '-':
        sub.subtract(first,second,n,a,b,cl,qc)
        printResult(first, second, qc,a, cl, n, operator)
    elif operator == '*':
        multiplication.multiply(first,secondDec,n,a,b,cl,qc)
        printResult(first, second, qc, b, cl, n,operator)
    elif operator == '**':
        power.pow(first,firstDec,secondDec,n,a,b,cl,qc)
    #else:
        #division.divide()

    print(bcolors.OKCYAN + '#'*150 + bcolors.ENDC)