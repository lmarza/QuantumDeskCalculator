# Quantum Desk Calculator with Qiskit


## Problem definition
The task is to build a quantum circuit that performs the difference between the binary representation of two positive integers. The circuit can be defined as a variation of the quantum adder explained in class and using the Quantum Fourier Transform. The circuit must be implemented in `qiskit` and demonstrated on a one or two instances. The project can be extended with the implementation of a complete desk calculator.



## Implementation details
### Prerequisites
- Python3.7+
- qiskit

### Operations implemented:
- [x] Addition Full Adder implementation
- [x] Addition using QFT
- [x] Subtraction using QFT
- [x] Multiplication using continuous QFT sum
- [x] Division using subtraction and addition implemented via QFT


### Clone the repository

```
git clone https://github.com/LM095/QuantumDeskCalculator
cd QuantumDeskCalculator
```
### Run the program
```
python quantumDeskCalculator.py
```


### Example of esecution

#### Addition:
> 320 (101000000) + 150 (10010110) = 470(0111010110)
![](https://i.imgur.com/cf8xpIX.png)
#### Subtraction:
> 1200 (10010110000) - 547 (1000100011) = 653 (001010001101)
![](https://i.imgur.com/N7upjvD.png)
#### Multiplication:
> 53 (110101) * 4 (100) = 212 (0011010100)
![](https://i.imgur.com/j6Y99So.png)
#### Division:
> 12 (1100) / 5 (0101) = 2 (0010)
![](https://i.imgur.com/Qgg1ebh.png)


## Authors

* **Luca Marzari** - [LM095](https://github.com/LM095)
* **Deborah Pintani** - [DebbyX3](https://github.com/DebbyX3)
