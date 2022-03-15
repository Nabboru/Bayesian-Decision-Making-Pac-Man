import matplotlib.pyplot as plt
from scipy.stats import bernoulli, binom
import numpy as np


bd = bernoulli(0.16)
X = [0, 1]
plt.figure(figsize=(7,7))
plt.xlim(-2, 3)
plt.xticks([0,1])
#plt.xticklabels(['0','1'])
plt.bar(X, bd.pmf(X), color='navy')
plt.title('Bernoulli Distribution', fontsize='15')
plt.xlabel('Outcome (0 = Failure, 1 = Success)', fontsize='10')
plt.ylabel('Probability', fontsize='10')
plt.show()


n = 10
p = 0.16
x = np.arange(0, n+1)
binomial_pmf = binom.pmf(x, n, p)
x =  np.arange(1, n+2)
plt.xticks(np.arange(1, n+1))
plt.xlim(0, 11)
plt.bar(x, binomial_pmf, color='navy')
plt.title(f"Binomial Distribution")
plt.xlabel('Trial Nº', fontsize='10')
plt.ylabel('Probability of Success for Each Trial', fontsize='10')
plt.show()