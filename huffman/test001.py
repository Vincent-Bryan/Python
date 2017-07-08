import sys
import six
g_code = {101:'0', 122:'100', 100:'101', 99:'11'}

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Please input a filename")
		exit(0)
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2]

	f = open(input_file, 'rb')
	output_ptr = open(output_file, 'wb')
	file_data = f.read()
	file_size = f.tell()

	char_freq = {}
	content = ''
	cnt = 0
	for x in range(file_size):
		tmp = file_data[x]
		# print(tmp)
		content = content + g_code[tmp]
		out = 0
		while len(content) > 8:
			cnt = cnt + 1
			for i in range(8):
				out = out << 1
				if content[i] == '1':
					out = out | 1
			content = content[8:]
			# print(six.int2byte(out))
			output_ptr.write(six.int2byte(out))
			out = 0
		# if tmp in char_freq.keys():
		# 	char_freq[tmp] = char_freq[tmp] + 1
		# else:
		# 	char_freq[tmp] = 1
	# print(cnt)


	# for tmp in char_freq.keys():
	# 	print(chr(tmp),char_freq[tmp])