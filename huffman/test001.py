import sys
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Please input a filename")
		exit(0)
	else:
		INPUTFILE = sys.argv[1]

	f = open(INPUTFILE, 'rb')
	file_data = f.read()
	file_size = f.tell()

	char_freq = {}
	for x in range(file_size):
		tmp = file_data[x]
		# print(tmp.__class__.__name__)
		# print(str(tmp))
		tt = str(tmp).encode()
		print(len(tmp), len(tt), tt[0], tt[1])
		if tmp in char_freq.keys():
			char_freq[tmp] = char_freq[tmp] + 1
		else:
			char_freq[tmp] = 1

	for tmp in char_freq.keys():
		print(chr(tmp),char_freq[tmp])