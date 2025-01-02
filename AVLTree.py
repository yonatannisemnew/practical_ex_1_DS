#id1:329371967
#name1:Yonatan Nissenboym
#username1:
#id2:216083329
#name2:Ilai Shoshani
#username2:ilaishoshani


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key: int = key
		self.value: int = value
		self.left: AVLNode = None
		self.right: AVLNode = None
		self.parent: AVLNode = None
		self.height: int = -1

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		if self.key:
			return False
		return True

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		temp_node = self.root
		e = 1
		if temp_node == None:
			return None, -1
		while temp_node.is_real_node() and temp_node.key != key:
			e+=1
		if temp_node.key == key:
			return temp_node, e
		return None, -1

	def right_rotate(self, root):
		if not root.left.is_real_node():
			return
		parent_of_root = root.parent
		tmp = root.left.right
		tmp.parent = root
		root.left.right = root
		root.left.parent = parent_of_root
		root.parent = root.left
		root.left = tmp
		if parent_of_root is None:
			self.root = root.parent

	def left_rotate(self, root):
		if not root.right.is_real_node():
			return
		root_parent = root.parent
		tmp = root.right.left
		root.right.left = root
		root.right.parent = root_parent
		root.parent = root.right
		root.right = tmp
		root.right.parent = root
		if root_parent is None:
			self.root = root.parent
	def left_then_right_rotate(self, root):
		self.left_rotate(root.left)
		self.right_rotate(root.parent.parent)
		return
	def right_then_left_rotate(self, root):
		self.right_rotate(root.right)
		self.left_rotate(root.parent.parent)

	def finger_search(self, key: int):
		return None, -1
	
	def insert_helper(self, tree: AVLNode, key: int, val: int):
		if not tree.is_real_node():
			tree.key = key
			tree.val = val
			tree.right = AVLNode(None, None)
			tree.left = AVLNode(None, None)
			return tree, 0, 0 # No edges or rotations encountered.
		if key < tree.key:
			node, edges, rotations = self.insert_node(tree.left, key, val)
			return node, edges + 1, rotations
		# We assume no key appears twice.
		node, edges, rotations = self.insert_node(tree.right, key, val)
		return node, edges + 1, rotations


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key: int, val: int):
		if self.root == None:
			self.root = AVLNode(key, val)
			return self.root, 0, 0 # No edges or promotions done.
		return self.insert_helper(key, val)


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None
