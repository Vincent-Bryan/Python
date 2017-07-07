import sys
import six

g_code = {}
class node(object):
	"""docstring for node
	0 for leaf
	1 for root
	"""
	def __init__(self, flag, value, freq, left_child, right_child):
		super(node, self).__init__()
		if(flag == 0):
			self.is_leaf = True;
			self.value = value
			self.freq = freq
			self.left_child = None
			self.right_child = None
		else:
			self.is_leaf = False;
			self.value = None
			self.freq = left_child.get_freq() + right_child.get_freq()
			self.left_child = left_child
			self.right_child = right_child

	def get_freq(self):
		return self.freq

	def get_value(self):
		return self.value

	def get_left_child(self):
		return self.left_child

	def get_right_child(self):
		return self.right_child

	def traverse(self, code):
		if self.is_leaf == True:
			g_code[self.get_value()] = code
		else:
			self.left_child.traverse (code + '0')
			self.right_child.traverse(code + '1')

def build_huff_tree(node_list):
	while len(node_list) > 1:
		node_list.sort(key = lambda x : x.get_freq())
		tmp1 = node_list[0]
		tmp2 = node_list[1]
		node_list = node_list[2:]

		new_node = node(1, 0, 0, tmp1, tmp2)
		node_list.append(new_node)

	return node_list[0]

'''
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
		if tmp in char_freq.keys():
			char_freq[tmp] = char_freq[tmp] + 1
		else:
			char_freq[tmp] = 1

	for tmp in char_freq.keys():
		print(chr(tmp),char_freq[tmp])

	node_list = []
	for x in char_freq.keys():
		tmp = node(0, x, char_freq[x], None, None)
		node_list.append(tmp)

	tmp = build_huff_tree(node_list)
	tmp.traverse('')
	for x in g_code.keys():
		print(x, chr(x), g_code[x])
		
'''

def compress(input_file, output_file):
	f = open(input_file, 'rb')
	file_data = f.read()
	file_size = f.tell()

	char_freq = {}
	for x in range(file_size):
		tmp = file_data[x]
		if tmp in char_freq.keys():
			char_freq[tmp] = char_freq[tmp] + 1
		else:
			char_freq[tmp] = 1

	for tmp in char_freq.keys():
		print(chr(tmp),char_freq[tmp])

	node_list = []
	for x in char_freq.keys():
		tmp = node(0, x, char_freq[x], None, None)
		node_list.append(tmp)

	length = len(char_freq.keys())
	output = open(output_file, 'wb')

	a4 = length & 255 		# 取低8位
    length = length >> 8	# 左移8位
    a3 = length & 255
    length = length >> 8
    a2 = length & 255
    length = length >> 8
    a1 = length & 255
    output.write(six.int2byte(a1))
    output.write(six.int2byte(a2))
    output.write(six.int2byte(a3))
    output.write(six.int2byte(a4))

    tmp = build_huff_tree(node_list)
	tmp.traverse('')

	# content = ''
	for i in range(file_size):
		key = file_data[i]
		# content = content + g_code[key]
		output.write(g_code[key])

	output.close()
		
		

