import matplotlib.pyplot as plt
from des import hex_to_bin,permute,shift_left,bin_to_hex,encrypt,hamming_distance

    
pt0='123456DCBA132536'
pt=['123456DCBA132556','323456DCBA132536','123453DCBA132536','123456ACBA132536','123456DCBC132536','123456DCEA132536']
key = "AACB09182436CCAD"

key = hex_to_bin(key)

keyp = [57, 49, 41, 33, 25, 17, 9,
		1, 58, 50, 42, 34, 26, 18,
		10, 2, 59, 51, 43, 35, 27,
		19, 11, 3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		7, 62, 54, 46, 38, 30, 22,
		14, 6, 61, 53, 45, 37, 29,
		21, 13, 5, 28, 20, 12, 4 ]

key = permute(key, keyp, 56)

shift_table = [1, 1, 2, 2,
				2, 2, 2, 2,
				1, 2, 2, 2,
				2, 2, 2, 1 ]

key_comp = [14, 17, 11, 24, 1, 5,
			3, 28, 15, 6, 21, 10,
			23, 19, 12, 4, 26, 8,
			16, 7, 27, 20, 13, 2,
			41, 52, 31, 37, 47, 55,
			30, 40, 51, 45, 33, 48,
			44, 49, 39, 56, 34, 53,
			46, 42, 50, 36, 29, 32 ]


left = key[0:28] 
right = key[28:56] 

rkb = []
rk = []
for i in range(0, 16):
	left = shift_left(left, shift_table[i])
	right = shift_left(right, shift_table[i])
	combine_str = left + right
	round_key = permute(combine_str, key_comp, 48)

	rkb.append(round_key)
	rk.append(bin_to_hex(round_key))

_, parent_ciphers= encrypt(pt0, rkb, rk)
matrix=[]
for i in range(5):
  _ , ciphers = encrypt(pt[i], rkb, rk)
  matrix.append(ciphers)
matrix =[[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(len(matrix),len(matrix[0]))
print(len(parent_ciphers))

hamming_distances=[]



for i in range(16):
  temp=[]
  for j in range(5):
    hd=hamming_distance(matrix[i][j] , parent_ciphers[i])
    temp.append(hd)
  hamming_distances.append(temp)
print(hamming_distances)

mean_hamming_distances=[]
for i in hamming_distances:
  mean_hamming_distances.append(sum(i)/len(i))


plt.boxplot(hamming_distances)
plt.title('Avalanche Effect on DES Rounds for 5 different plaintexts')
plt.xlabel('DES Rounds')
plt.ylabel('Hamming Distance')
plt.ylim(1,50)
plt.show()
