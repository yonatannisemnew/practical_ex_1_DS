# id1:329371967
# name1:Yonatan Nissenboym
# username1:
# id2:216083329
# name2:Ilai Shoshani
# username2:ilaishoshani

from math import log, sqrt

PHI = (1+sqrt(5))/2

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key=None, value=None):
        self.key: int = key
        self.value: str = value
        self.left: AVLNode = None
        self.right: AVLNode = None
        self.parent: AVLNode = None
        self.height: int = -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.key is not None

    def balance_factor(self):
        return self.left.height - self.right.height

    def __repr__(self):
        return f"Node[{self.key}, {self.value}]"


"""
A class implementing an AVL tree.
"""
class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.root = None
        self.max_node = None
        self.size: int = 0

    def search_helper(self, tree: AVLNode, key: int):
        if tree is None or not tree.is_real_node():  # Key doesn't exist.
            return None, 0
        if key == tree.key:  # We Found It!
            return tree, 0
        if key < tree.key:  # Search Left
            node, edges = self.search_helper(tree.left, key)
            return node, edges + 1
        if key > tree.key:  # Search Right
            node, edges = self.search_helper(tree.right, key)
            return node, edges + 1

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key: int):
        return self.search_helper(self.root, key)

    def right_rotate(self, root):
        print("Right Rotate:", root)
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
        return root.parent

    def left_rotate(self, root):
        print("Left Rotate:", root)
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
        return root.parent

    def left_then_right_rotate(self, root):
        self.left_rotate(root.left)
        return self.right_rotate(root)

    def right_then_left_rotate(self, root):
        self.right_rotate(root.right)
        return self.left_rotate(root)

    def rebalance_after_insert(self, node: AVLNode):
        if node.parent is None:
            return 0

        if node.parent.height == node.height:
            node.parent.height += 1
            return self.rebalance_after_insert(node.parent) # Propegate Up.
        if node.parent.balance_factor() == -2:  # Right subtree too large
            if node.balance_factor() > 0:  # Right subtree is pretty small, can be added a node.
                node.parent.height -= 1
                self.right_rotate(node.parent)
            else:
                node.parent.height -= 1
                node.height -= 1
                node.right.height += 1
                self.left_then_right_rotate(node.parent)
            return 1
        if node.parent.balance_factor() == 2:  # Left subtree too large
            if node.balance_factor() < 0:  # Left subtree is pretty small, can be added a node.
                node.parent.height -= 1
                self.left_rotate(node.parent)
            else:
                node.parent.height -= 1
                node.height -= 1
                node.left.height += 1
                self.right_then_left_rotate(node.parent)
            return 1
        return 0

    def make_real(self, node: AVLNode, key: int, value: str):
        # Make the given node into a real node.
        node.key = key
        node.value = value
        node.height = 0

        # Create new vnodes for right and left
        node.right = self.make_vnode(node)
        node.left = self.make_vnode(node)
        return node

    def make_vnode(self, parent: AVLNode):
        node = AVLNode(None, None)
        node.parent = parent
        return node

    def insert_helper(self, tree: AVLNode, key: int, val: str):
        if not tree.is_real_node():
            self.make_real(tree, key, val)

            # Update max node.
            if key > self.max_node.key:
                self.max_node = tree
            rotations = self.rebalance_after_insert(tree)
            self.size += 1  # New node added
            return tree, 0, rotations  # No edges encountered.
        if key < tree.key:
            node, edges, rotations = self.insert_helper(tree.left, key, val)
            return node, edges + 1, rotations
        # We assume no key appears twice.
        node, edges, rotations = self.insert_helper(tree.right, key, val)
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

    def insert(self, key: int, val: str):
        if self.root is None:
            self.max_node = self.root = self.make_real(AVLNode(), key, val)
            return self.root, 0, 0  # No edges or promotions done.
        return self.insert_helper(self.root, key, val)

    @staticmethod
    def successor(node: AVLNode):
        if node.right.is_real_node():
            node = node.right
            while node.left.is_real_node():
                node = node.left
            return node
        else:
            # Go up while we are still going left (we were on the right)
            while node.parent.right == node:
                node = node.parent
            if node.parent.right == node:
                return node.parent
            else:
                return None  # No successor found.

    def finger_search(self, key: int):
        if self.root is None:
            return None, 1
        max_node: AVLNode = self.max_node()
        curr_node: AVLNode = max_node
        calc_size = log(PHI, key)
        while curr_node.height < calc_size and curr_node != self.root:
            curr_node = curr_node.parent

        # Search for the node in the subtree and add the diff we traveled to the edge count.
        x, e = self.search_helper(curr_node, key)
        return x, e + (curr_node.height - max_node.height)

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
        if self.root is None:
            self.max_node = self.root = self.make_real(AVLNode(), key, val)
            return self.root, 0, 0  # No edges or promotions done.
        max_node: AVLNode = self.max_node()
        curr_node: AVLNode = max_node
        calc_size = log(PHI, key)
        while curr_node.height < calc_size and curr_node != self.root:
            curr_node = curr_node.parent

        # Insert the node and add the amount of edges we traveled to the edge count.
        x, e, h = self.insert_helper(curr_node, key, val)
        return x, e + (curr_node.height - max_node.height), h

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

    def join_with_subtree(self, subtree: AVLNode, join_node: AVLNode):
        # TODO: Implement. The given node can be virtual - so we need to not do anything if it is.
        # (The subtree can be a virtual node)
        pass

    def join(self, tree2, key: int, val: str):
        # curr_node: AVLNode = self.root
        # if self.size() > tree2.size():
        #     while curr_node.is_real_node() and curr_node.key > tree2.get_root().key:
        #         curr_node = curr_node.left
        pass

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
        left_tree = AVLTree()
        right_tree = AVLTree()

        left_tree.join_with_subtree(node.left, node)
        right_tree.join_with_subtree(node.left, node)
        while node is not self.root:
            if node.parent.left != node:  # We have lower stuff to add.
                left_tree.join_with_subtree(node.left, node)
            elif node.parent.right != node:  # We have higher stuff to add.
                right_tree.join_with_subtree(node.left, node)
            node = node.parent
        return left_tree, right_tree

    def avl_to_array_helper(self, tree: AVLNode, lst):
        # Traverse the tree in-order.
        if tree is not None and tree.is_real_node():
            self.avl_to_array_helper(tree.left, lst)
            lst.append((tree.key, tree.value))
            self.avl_to_array_helper(tree.right, lst)

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        lst = []
        self.avl_to_array_helper(self.root, lst)
        return lst

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self):
        return self.max_node

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.root.size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root


def main():
    tree = AVLTree()
    print(tree.insert(1, "ilai"))
    print(tree.insert(5, "yohnatan-"))
    print(tree.insert(3, "ilai3"))
    print(tree.insert(2, "ilai2"))
    print(tree.insert(10, "not ilai"))
    print(tree.insert(50, "not yohnatan-"))
    print(tree.insert(30, "not ilai3"))
    print(tree.insert(20, "not ilai2"))

    print(tree.avl_to_array())
    node10, edges = tree.search(10)
    print("Node #10:", node10, edges)
    left, right = tree.split(node10)
    print("\nLeft", left.avl_to_array(), "\nRight", right.avl_to_array(), sep="\n")


main()
