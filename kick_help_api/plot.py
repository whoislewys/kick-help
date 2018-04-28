import csv
import matplotlib.pyplot as p
import numpy as np

x = np.array(range(11))
x = (x * 10) + 1
y = np.ones(11)
with open('model_accuracy.txt', 'r') as file:
	for i, line in enumerate(file):
		y[i] = np.float32(line)
y = 1/y

p.plot(x, y)
p.ylabel('(binary_accuracy)^(-1)')
p.xticks(x, x)
p.xlabel('Number of Nodes')
p.savefig('model_accuracy.png', bbox_inches='tight')