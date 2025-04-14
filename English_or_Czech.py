en_freq = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
           0.772, 4.025, 2.406, 6.749,  7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
           2.758, 0.978, 2.360, 0.150,  1.974, 0.074]
cz_freq = [8.421, 0.822, 0.740, 3.475, 7.562, 0.084, 0.092, 1.356, 6.073, 1.433,
           2.894, 3.802, 2.446, 6.468, 6.695, 1.906, 0.001, 4.799, 5.212, 5.727,
           2.160, 5.344, 0.016, 0.027, 1.043, 1.503]
a = 27*[0]
b = 27*[0]
sumEn = float(0)
sumCz = float(0)
allLet = 0
for i in range (1, len(b), 1):
	b[i] = chr(i+64)
import sys
for s in sys.stdin:
	for i in range(0, len(s), 1):
		c = s[i].upper()
		for j in range(1, len(b),1):
			if (c == b[j]):
				a[j]+=1
				allLet += 1
for i in range (1, len(a), 1):
	#if (a[i] != 0):
		sumEn += (((a[i]/allLet) - (en_freq[i-1]/100))**2)/(en_freq[i-1]/100)
		sumCz += (((a[i]/allLet) - (cz_freq[i-1]/100))**2)/(cz_freq[i-1]/100)
print (f'Match with English: {sumEn:.2f}')
print (f'Match with Czech: {sumCz:.2f}')  
if (sumEn > sumCz):
	print('Text is in Czech')
else: 
	print('Text is in English')    
