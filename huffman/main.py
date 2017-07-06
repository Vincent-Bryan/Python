import six
import sys
class huff_node(object):
	"""docstring for huff_node"""
	# def __init__(self, arg):
	# 	super(huff_node, self).__init__()
	# 	self.arg = arg
	def get_value(self):
		raise NotImplementedError(
            "The Abstract Node Class doesn't define 'get_weight'")
	def is_leaf(self):
		raise NotImplementedError(
            "The Abstract Node Class doesn't define 'isleaf'")

class leaf_node(huff_node):
	"""docstring for leaf_node"""
	def __init__(self, value, freq):
		super(leaf_node, self).__init__()
		self.value = value
		self.freq = freq
	def get_value(self):
		return self.value
	def get_freq(self):
		return self.freq
	def is_leaf(self):
		return True

class init_node(huff_node):
	"""docstring for init_node"""
	def __init__(self, left_child = None, right_child = None):
		super(init_node, self).__init__()
		self.left_child = left_child
		self.right_child = right_child
		self.freq = left_child.get_freq() + right_child.get_freq()
		self.value = None
	def get_freq(self):
		return self.freq
	def get_left_child(self):
		return self.left_child
	def get_right_child(self):
		return self.right_child
	def is_leaf(self):
		return False

class huff_tree(object):
	"""docstring for huff_tree"""
	def __init__(self, flag, value = 0, freq = 0, left_child = None, right_child = None):
		super(huff_tree, self).__init__()
		if(flag == 0):
			self.root = leaf_node(value, freq)
		else:
			self.root = init_node(left_child, right_child)
	def get_freq(self):
		return self.root.get_freq()
	def get_root(self):
		return self.root

	def traverse(self, root, code, char_freq):
		# print(self.root.__class__.__name__)
		if self.root.is_leaf():
			decode[root.get_value()] = code
			return None
		else:
			self.traverse(self.root.get_left_child(), code+'0', char_freq)
			self.traverse(self.root.get_right_child(), code+'1', char_freq)

def builf_huff_tree(node_list):
	while len(node_list) > 1:
		node_list.sort(key = lambda x : x.get_freq())
		tmp1 = node_list[0]
		tmp2 = node_list[1]
		node_list = node_list[2:]

		new_huff_tree = huff_tree(1, 0, 0, tmp1, tmp2)
		# print(new_huff_tree.__class__.__name__)
		node_list.append(new_huff_tree)

	return node_list[0]


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
		# print(file_data[x])
		# tmp = six.byte2int(file_data[x])
		tmp = file_data[x]
		if tmp in char_freq.keys():
			char_freq[tmp] = char_freq[tmp] + 1
		else:
			char_freq[tmp] = 1

	for tmp in char_freq.keys():
		print(chr(tmp),char_freq[tmp])

	huff_tree_list = []
	for x in char_freq.keys():
		tmp = huff_tree(0, x, char_freq[x], None, None)
		huff_tree_list.append(tmp)
		# print(tmp.get_root().__class__.__name__)

	# for x in range(0, len(huff_tree_list)):
	# 	print(chr(huff_tree_list[x].root.get_value()), ' ', huff_tree_list[x].root.get_freq())
	tmp = builf_huff_tree(huff_tree_list)
	tmp.traverse(tmp.get_root(), '', char_freq)
	# print(tmp.get_root().__class__.__name__)
	# print(tmp.get_root().is_leaf())