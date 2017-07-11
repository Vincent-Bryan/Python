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

def dfs(node):
	if node.is_leaf:
		print(chr(node.get_value()))
	else:
		dfs(node.get_left_child())
		dfs(node.get_right_child())

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

	node_list = []
	for x in char_freq.keys():
		tmp = node(0, x, char_freq[x], None, None)
		node_list.append(tmp)

	length = len(char_freq.keys())
	output_ptr = open(output_file, 'wb')


	# 写入长度
	print("length: ",length)
	a4 = length & 255 		# 取低8位
	length = length >> 8	# 左移8位
	a3 = length & 255
	length = length >> 8
	a2 = length & 255
	length = length >> 8
	a1 = length & 255
	output_ptr.write(six.int2byte(a1))
	output_ptr.write(six.int2byte(a2))
	output_ptr.write(six.int2byte(a3))
	output_ptr.write(six.int2byte(a4))

	print("writing length done")
	for x in char_freq.keys():
		output_ptr.write(six.int2byte(x))
		tmp = char_freq[x]

		a4 = tmp & 255
		tmp = tmp >> 8
		a3 = tmp & 255
		tmp = tmp >> 8
		a2 = tmp & 255
		tmp = tmp >> 8
		a1 = tmp & 255
		output_ptr.write(six.int2byte(a1))
		output_ptr.write(six.int2byte(a2))
		output_ptr.write(six.int2byte(a3))
		output_ptr.write(six.int2byte(a4))

	print("writing char_freq done")

	node_list = []
	g_code.clear()
	for x in char_freq.keys():
		tmp = node(0, x, char_freq[x], None, None)
		node_list.append(tmp)
	tmp = build_huff_tree(node_list)
	tmp.traverse('')

	# print("leaf_ndoe_size: ", leaf_node_size)
	for tmp in char_freq.keys():
		print(chr(tmp),char_freq[tmp], g_code[tmp])
		
	# 将编码后的内容以二进制的形式写入
	content = ''
	for i in range(file_size):
		key = file_data[i]
		content = content + g_code[key]
		# output_ptr.write(g_code[key])
		out = 0
		while len(content) > 8:
			for x in range(8):
				out = out << 1
				if content[x] == '1':
					out = out | 1
			content = content[8:]
			output_ptr.write(six.int2byte(out))
			out = 0
	# print(cnt)

	# 处理剩下未满8位的情况
	output_ptr.write(six.int2byte(len(content)))
	out = 0
	for i in range((len(content))):
		out = out << 1
		if content[i] == '1':
			out = out | 1
	for i in range(8-len(content)):
		out = out << 1
	output_ptr.write(six.int2byte(out))
	output_ptr.close()


def decompress(input_file, output_file):
	f = open(input_file, 'rb')
	file_data = f.read()
	file_size = f.tell()

	a1 = file_data[0]
	a2 = file_data[1]
	a3 = file_data[2]
	a4 = file_data[3]
	j = 0
	j = j | a1
	j = j << 8
	j = j | a2
	j = j << 8
	j = j | a3
	j = j << 8
	j = j | a4

	leaf_node_size = j

	char_freq = {}
	for i in range(leaf_node_size):
		c = file_data[4 + i*5 + 0]

		a1 = file_data[4 + i*5 + 1]
		a2 = file_data[4 + i*5 + 2]
		a3 = file_data[4 + i*5 + 3]
		a4 = file_data[4 + i*5 + 4]
		
		j = 0
		j = j | a1
		j = j << 8
		j = j | a2
		j = j << 8
		j = j | a3
		j = j << 8
		j = j | a4
		print(c, j)
		char_freq[c] = j

	# 重建哈夫曼树
	node_list = []
	g_code.clear()
	for x in char_freq.keys():
		tmp = node(0, x, char_freq[x], None, None)
		node_list.append(tmp)
	root_node = build_huff_tree(node_list)
	root_node.traverse('')

	print("leaf_ndoe_size: ", leaf_node_size)


	dfs(root_node)
	# dfs(root_node)

	for tmp in char_freq.keys():
		print(chr(tmp),char_freq[tmp], g_code[tmp])

	output_ptr = open(output_file, 'wb')
	content = ''
	cur_node = root_node
	for x in range(leaf_node_size*5+4, file_size):

		c = file_data[x]
		for i in range(8):
			if c & 128:	
				content = content + '1'
			else:
				content = content + '0'
			c = c << 1
		while len(content) > 24:
			if cur_node.is_leaf:
				tmp_byte = six.int2byte(cur_node.get_value())
				output_ptr.write(tmp_byte)
				cur_node = root_node
			else:
				if content[0] == '1':
					cur_node = cur_node.get_right_child()
				else:
					cur_node = cur_node.get_left_child()
				content = content[1:]

	remainder = content[-16:-8]
	last_length = 0
	for i in range(8):
		last_length = last_length << 1
		if remainder[i] == '1':
			last_length = last_length | 1

	content = content[:-16] + content[-8:-8+last_length]
	while len(content) > 0:
		if cur_node.is_leaf:
			tmp_byte = six.int2byte(cur_node.get_value())
			output_ptr.write(tmp_byte)
			cur_node = root_node
		else:
			if content[0] == '1':
				cur_node = cur_node.get_right_child()
			else:
				cur_node = cur_node.get_left_child()
			content = content[1:]

	if cur_node.is_leaf:
		tmp_byte = six.int2byte(cur_node.get_value())
		output_ptr.write(tmp_byte)
		cur_node = root_node

	output_ptr.close()


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("INPUT ERROR!!")		
		exit(0)
	else:
		FLAG = sys.argv[1]
		input_file = sys.argv[2]
		output_file = sys.argv[3]

	if FLAG == '0':
		print("compress file")
		compress(input_file, output_file)
	else:
		print("decompress file")
		decompress(input_file, output_file)
