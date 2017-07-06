class Rectangle(object):
	"""docstring for Rectangle"""
	def __init__(self, width, height):
		super(Rectangle, self).__init__()
		self.width = width
		self.height = height
	def __del__(self):
		print("end")

	def get_width(self):
		print(self.width)

	def get_height(self):
		print(self.height)

	def get_area(self):
		return self.width * self.height

	def __lt__(self, other):
		tmp1 = self.width
		tmp2 = other.width
		# tmp1 = self.get_area()
		# tmp2 = other.get_area()
		return tmp1 < tmp2
		# 重载的话只能比较成员函数，不能比较返回值？
		# python3.x 里不能重载__cmp__

class Triangle(Rectangle):
	"""docstring for Square"""
	def __init__(self, width, height):
		# super(Square, self).__init__()
		self.width = width
		self.height = height
	def get_area(self):
		return 0.5 * self.width * self.height

A = Rectangle(2, 4)
B = Triangle(3, 4)
print(A.__class__.__name__)
print(B.__class__.__name__)