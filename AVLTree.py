# id1:329371967
# name1:Yonatan Nissenboym
# username1:
# id2:216083329
# name2:Ilai Shoshani
# username2:ilaishoshani

from math import log, sqrt
import matplotlib.pyplot as plt

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

    def leaf(self):
        return not self.left.is_real_node() and not self.right.is_real_node()

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
        self.max = None
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

        # Ensure there is a left child to rotate
        if not root.left.is_real_node():
            return

        # Identify nodes involved in rotation
        new_root = root.left
        parent_of_root = root.parent
        root.left = new_root.right

        # Update parent of the subtree being rotated
        new_root.right.parent = root

        # Perform rotation
        new_root.right = root
        root.parent = new_root

        # Update the parent of the new root
        new_root.parent = parent_of_root
        if parent_of_root is None:
            self.root = new_root  # Update tree root if root was the root of the tree
        else:
            # Attach new root to the appropriate parent child
            if parent_of_root.left == root:
                parent_of_root.left = new_root
            else:
                parent_of_root.right = new_root
        root.height = max(root.left.height, root.right.height) + 1
        new_root.height = max(new_root.left.height, new_root.right.height) + 1
        return new_root

    def left_rotate(self, root):
        print("Left Rotate:", root)
        if not root.right.is_real_node():
            return
        root_parent = root.parent
        new_root = root.right
        tmp = new_root.left
        new_root.left = root
        new_root.parent = root_parent
        root.right = tmp
        root.parent = new_root
        if tmp:
            tmp.parent = root
        if root_parent is None:
            self.root = new_root
        else:
            if root_parent.left == root:
                root_parent.left = new_root
            else:
                root_parent.right = new_root
        # Update heights
        root.height = max(root.left.height, root.right.height) + 1
        new_root.height = max(new_root.left.height, new_root.right.height) + 1
        return new_root

    def left_then_right_rotate(self, root):
        self.left_rotate(root.left)
        return self.right_rotate(root)

    def right_then_left_rotate(self, root):
        self.right_rotate(root.right)
        return self.left_rotate(root)

    def rebalance_after_insert(self, node: AVLNode):
        if node.parent is None:
            return 0

        # TODO: Maybe we should prevent the case of >2 in join
        if node.parent.balance_factor() >= 2:  # Left subtree too large
            if node.balance_factor() > 0:  # Right subtree is pretty small, can be added a node.
                self.right_rotate(node.parent)
            else:
                self.left_then_right_rotate(node.parent)
            return 1
        if node.parent.balance_factor() <= -2:  # Right subtree too large
            # For Visualising, do:  self.visualize_tree()
            if node.balance_factor() < 0:  # Left subtree is pretty small, can be added a node.
                self.left_rotate(node.parent)
            else:
                self.right_then_left_rotate(node.parent)
            return 1
        if node.parent.height == node.height:
            node.parent.height += 1
            return self.rebalance_after_insert(node.parent)  # Propagate Up.
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
            if self.max is None or key > self.max.key:
                self.max = tree
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
            self.max = self.root = self.make_real(AVLNode(), key, val)
            return self.root, 0, 0  # No edges or promotions done.
        return self.insert_helper(self.root, key, val)

    def finger_search(self, key: int):
        if self.root is None or not self.root.is_real_node():
            return None, 1
        max: AVLNode = self.max_node()
        curr_node: AVLNode = max
        while curr_node.key < key and curr_node != self.root:  # TODO: Mathematically this takes maximum log time.
            curr_node = curr_node.parent

        # Search for the node in the subtree and add the diff we traveled to the edge count.
        x, e = self.search_helper(curr_node, key)
        return x, e + (curr_node.height - max.height)

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
        if self.root is None or not self.root.is_real_node():
            self.max = self.root = self.make_real(AVLNode(), key, val)
            return self.root, 0, 0  # No edges or promotions done.
        curr_node: AVLNode = self.max_node()
        max_height: int = curr_node.height
        while curr_node.key < key and curr_node != self.root:
            curr_node = curr_node.parent

        # Insert the node and add the amount of edges we traveled to the edge count.
        x, e, h = self.insert_helper(curr_node, key, val)
        return x, e + (curr_node.height - max_height), h

    @staticmethod
    def successor(node: AVLNode):  # Assume node is not None or virtual (max node never has right son).
        if node is None or not node.is_real_node():
            return None
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

    @staticmethod
    def predecessor(node: AVLNode):
        if node is None or not node.is_real_node():
            return None
        if node.left.is_real_node():
            node = node.left
            while node.right.is_real_node():
                node = node.right
            return node
        else:
            # Go up while we are still going right (we were on the left)
            while node.parent.left == node:
                node = node.parent
            if node.parent.left == node:
                return node.parent
            else:
                return None  # No predecessor found.

    def balance_deletion(self, node: AVLNode):
        right_difference = node.height - node.right.height
        left_difference = node.height - node.left.height
        right_left_difference = node.right.height - node.right.left.height
        right_right_difference = node.right.height - node.right.right.height
        left_left_difference = node.left.height - node.left.left.height
        left_right_difference = node.left.height - node.left.right.height

        if right_difference == 2 and left_difference == 2:
            node.height -= 1
        elif left_difference == 3 and right_difference == 1 and right_right_difference == 1 and right_left_difference == 1:
            node = self.left_rotate(node)
            node.left.height -= 1
            node.height += 1
        elif right_difference == 3 and left_difference == 1 and left_right_difference == 1 and left_left_difference == 1:
            node = self.right_rotate(node)
            node.right.height -= 1
            node.height += 1
        elif left_difference == 3 and right_difference == 1 and right_right_difference == 1 and right_left_difference == 2:
            node = self.left_rotate(node)
            node.left.height -= 2
        elif right_difference == 3 and left_difference == 1 and left_right_difference == 2 and left_left_difference == 1:
            node = self.right_rotate(node)
            node.right.height -= 2
        elif left_difference == 3 and right_difference == 1 and right_right_difference == 2 and right_left_difference == 1:
            node = self.right_then_left_rotate(node)
        elif right_difference == 3 and left_difference == 1 and left_right_difference == 1 and left_left_difference == 2:
            node = self.left_then_right_rotate(node)
        if node.parent is not None:
            self.balance_deletion(node.parent)
        self.root = node

    def replace(self, to_replace: AVLNode, node: AVLNode):
        # Assume to_replace isn't None or virtual.
        if to_replace.parent is not None:
            if to_replace.parent.right == to_replace:
                to_replace.parent.right = node
            else:
                to_replace.parent.left = node

        if node.parent is not None:
            if node.parent.right == node:
                node.parent.right = to_replace
            else:
                node.parent.left = to_replace

        node.parent, to_replace.parent = to_replace.parent, node.parent
        node.left, to_replace.left = to_replace.left, node.left
        node.right, to_replace.right = to_replace.right, node.right


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):  # Assume node is a real node in the tree.
        if self.max == node:
            self.max = self.predecessor(self.max)
        if node.left.is_real_node() and node.right.is_real_node():
            to_replace = self.successor(node)  # We have a successor cause we have a right node.
            self.replace(to_replace, node)
            self.delete(node)
            return

        self.size -= 1
        if node == self.root:
            if node.left.is_real_node():
                node.left.parent = None
                self.root = node.left
            elif node.right.is_real_node():
                node.right.parent = None
                self.root = node.right
            else:
                self.root = None
            return

        if node.left.is_real_node():
            parent = node.parent
            if parent.right == node:
                parent.right = node.left
            else:
                parent.left = node.left
        else:
            parent = node.parent
            if parent.right == node:
                parent.right = node.right
            else:
                parent.left = node.right
        """
        Now we can assume node has 0 or 1 children.
        If root has changed this function will change it.
        (Parent of something is null).
        """
        self.balance_deletion(parent)

    def join_with_subtree(self, subtree: AVLNode, key: int, val: str):
        # Assume subtree isn't None or virtual.
        if self.root is None:
            self.root = self.make_vnode(None)

        self_is_smaller = subtree.height > self.root.height
        small_tree, big_tree = (self.root, subtree) if self_is_smaller else (subtree, self.root)
        curr_node = big_tree
        join_node = AVLNode(key, val)
        if join_node.key <= big_tree.key:
            print("Longer tree is also bigger", join_node, big_tree)
            while curr_node.left.is_real_node() and curr_node.height > small_tree.height:
                curr_node = curr_node.left
            if curr_node.parent is not None:
                curr_node = curr_node.parent
            join_node.right = curr_node.left
            curr_node.left.parent = join_node

            curr_node.left = join_node
            join_node.parent = curr_node

            join_node.left = small_tree
            small_tree.parent = join_node

            join_node.height = max(join_node.left.height, join_node.right.height) + 1
            curr_node.height = curr_node.right.height + 1
            # self.rebalance_after_insert(join_node)  # May help with edge cases
        else:
            print("Longer tree is smaller")
            while curr_node.right.is_real_node() and curr_node.height > small_tree.height:
                curr_node = curr_node.right
            if curr_node.parent is not None:
                curr_node = curr_node.parent
            join_node.left = curr_node.right
            curr_node.right.parent = join_node

            curr_node.right = join_node
            join_node.parent = curr_node

            join_node.right = small_tree
            small_tree.parent = join_node

            join_node.height = max(join_node.left.height, join_node.right.height) + 1
            curr_node.height = curr_node.left.height + 1
            # self.rebalance_after_insert(join_node)  # May help with edge cases
        self.root = big_tree
        self.rebalance_after_insert(join_node)

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
    def join(self, tree2, key: int, val: str):
        new_size = self.size + tree2.size + 1
        self.join_with_subtree(tree2.root, key, val)
        # Update Max Node
        if tree2.max is not None and (self.max is None or tree2.max.key > self.max.key):
            self.max = tree2.max
        self.size = new_size

    def find_max(self):
        curr_node: AVLNode = self.root

        if curr_node is None or not curr_node.is_real_node():
            return None
        while curr_node.right.is_real_node():
            curr_node = curr_node.right
        return curr_node

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
        # TODO: Check if this is the best solution in terms of complexity.
        left_tree = AVLTree()
        right_tree = AVLTree()

        if node.left is not None and node.left.is_real_node():
            node.left.parent = None
            left_tree.root = node.left
        if node.right is not None and node.right.is_real_node():
            node.right.parent = None
            right_tree.root = node.right

        while node is not self.root:
            parent: AVLNode = node.parent
            if parent is None:
                print("Why?")
            if parent.left == node:  # We went up right
                parent.right.parent = None
                right_tree.join_with_subtree(parent.right, parent.key, parent.value)
            else:
                parent.left.parent = None
                left_tree.join_with_subtree(parent.left, parent.key, parent.value)
            node = node.parent
        left_tree.max = left_tree.find_max()    # Update Max
        right_tree.max = right_tree.find_max()  # Update Max
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
        return self.max

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

    def nice_print_helper(self, tree: AVLNode, prefix: str):
        if not tree.is_real_node():
            print(prefix + "X")  # Virtual Node
        else:
            print(prefix + repr(tree))
            self.nice_print_helper(tree.left,  prefix + "  ")
            self.nice_print_helper(tree.right, prefix + "  ")

    def nice_print(self):
        if self.root is None:
            print("Empty Tree")
        else:
            self.nice_print_helper(self.root, "")

    def visualize_tree(self):
        def draw_node(node, x, y, dx, ax):
            if not node.is_real_node():
                # Draw virtual nodes as gray circles
                ax.plot(x, y, "o", color="gray")
                ax.text(x, y, "X", ha="center", va="center", color="white")
                return

            # Draw the current node as a blue circle
            ax.plot(x, y, "o", color="blue", markersize=50)
            ax.text(x, y, f"{node.key}\n{node.value}\nH:{node.height}",
                    ha="center", va="center", color="white", fontsize=8)

            # Draw left child
            if node.left:
                lx, ly = x - dx, y - 2
                ax.plot([x, lx], [y, ly], "-", color="black")  # Line to left child
                draw_node(node.left, lx, ly, dx / 2, ax)

            # Draw right child
            if node.right:
                rx, ry = x + dx, y - 2
                ax.plot([x, rx], [y, ry], "-", color="black")  # Line to right child
                draw_node(node.right, rx, ry, dx / 2, ax)

        if self.root is None or not self.root.is_real_node():
            print("Empty Tree")
            return

        # Initialize plot
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis("off")  # Turn off the axis

        # Start drawing from the root
        draw_node(self.root, x=0, y=0, dx=10, ax=ax)

        # Show the plot
        plt.show()

    # Add to your existing class
    # self.visualize_tree = visualize_tree.__get__(self)


def main():
    tree = AVLTree()

    """ Test: Insert """
    print(tree.insert(1, "ilai"))
    print(tree.insert(5, "yohnatan-"))
    print(tree.insert(3, "ilai3"))
    print(tree.insert(2, "ilai2"))
    print(tree.insert(10, "not ilai"))
    print(tree.insert(50, "not yohnatan-"))
    print(tree.insert(30, "not ilai3"))
    print(tree.insert(20, "not ilai2"))

    """ Test: To Array """
    #   print(tree.avl_to_array())

    tree2 = AVLTree()

    """ Test: Insert """
    print(tree2.insert(549, "addition"))
    print(tree2.insert(586, "algo"))
    print(tree2.insert(553, "52"))
    print(tree2.insert(111, "hi"))
    print(tree2.insert(222, "hi2"))
    print(tree2.insert(333, "hello"))
    print(tree2.insert(444, "hello2"))
    print(tree2.insert(555, "hello3"))

    # tree.visualize_tree()
    # tree2.visualize_tree()
    tree2.join(tree, 55, "VAL")

    print("Let's Visualize! Shurely nothing can go wrong!!!")
    tree2.nice_print()
    tree2.visualize_tree()

    # """ Test: Split """
    # tree.visualize_tree()

    """ Test: Search """
    node10, edges = tree2.search(10)
    print("Node #10:", node10, edges)

    left, right = tree2.split(node10)
    print("\nLeft", left.avl_to_array(), "\nRight", right.avl_to_array(), sep="\n")
    left.visualize_tree()
    right.visualize_tree()


main()