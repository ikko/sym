"""This module provides an implementation of a red-black tree.

A red-black tree is a self-balancing binary search tree that maintains a balanced height,
ensuring efficient search, insertion, and deletion operations.
"""
from typing import Any, Callable, Optional, Union

from ..core.base_symbol import Symbol

RED = True
BLACK = False

class RedBlackNode:
    def __init__(self, symbol: 'Symbol', weight: Union[float, Callable[[Any], float]], color=RED):
        """
        what: Initializes a Red-Black tree node.
        why: To store a Symbol and its weight within the tree structure.
        how: Sets symbol, weight, color, and child/parent pointers.
        when: When a new node is inserted into the Red-Black tree.
        by (caller(s)): RedBlackTree.insert.
        how often: Frequently.
        how much: Minimal.
        what is it like: Creating an entry in a self-balancing list.
        how, what, why and when to improve: N/A.
        """
        self.symbol = symbol
        self.weight = weight
        self.color = color
        self.left: Optional['RedBlackNode'] = None
        self.right: Optional['RedBlackNode'] = None
        self.parent: Optional['RedBlackNode'] = None

    def eval_weight(self, *args, **kwargs) -> float:
        """
        what: Evaluates the node's weight.
        why: To get a numerical value for comparison in the Red-Black tree.
        how: Calls the weight if callable, otherwise returns it directly.
        when: During tree operations (insert, search, remove).
        by (caller(s)): RedBlackTree methods.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting a sort key.
        how, what, why and when to improve: N/A.
        """
        return self.weight(self.symbol) if callable(self.weight) else self.weight


class RedBlackTree:
    def __init__(self):
        """
        what: Initializes an empty Red-Black tree.
        why: To create a self-balancing binary search tree for Symbols.
        how: Sets the root node to None.
        when: When a new RedBlackTree is instantiated.
        by (caller(s)): SymbolIndex.__init__.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating an empty sorted collection.
        how, what, why and when to improve: N/A.
        """
        self.root: Optional[RedBlackNode] = None

    def insert(self, symbol: 'Symbol', weight: Union[float, Callable]):
        """
        what: Inserts a Symbol into the Red-Black tree.
        why: To add a new Symbol while maintaining tree balance.
        how: Performs BST insertion, then fixes Red-Black properties.
        when: When a new Symbol is created and added to the index.
        by (caller(s)): Symbol.__new__.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Adding an item to a sorted collection.
        how, what, why and when to improve: Optimize for very large trees.
        """
        node = RedBlackNode(symbol, weight)
        self._bst_insert(node)
        self._fix_insert(node)

    def _bst_insert(self, z: RedBlackNode):
        """
        what: Performs a standard Binary Search Tree insertion.
        why: Helper for Red-Black tree insertion.
        how: Traverses the tree to find insertion point, links new node.
        when: During Red-Black tree insertion.
        by (caller(s)): RedBlackTree.insert.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Basic tree node placement.
        how, what, why and when to improve: N/A.
        """
        y = None
        x = self.root
        while x:
            y = x
            if z.eval_weight() < x.eval_weight():
                x = x.left
            else:
                x = x.right
        z.parent = y
        if not y:
            self.root = z
        elif z.eval_weight() < y.eval_weight():
            y.left = z
        else:
            y.right = z

    def _fix_insert(self, z: RedBlackNode):
        """
        what: Restores Red-Black tree properties after insertion.
        why: To maintain the self-balancing nature of the tree.
        how: Performs rotations and color changes based on Red-Black rules.
        when: After a new node is inserted.
        by (caller(s)): RedBlackTree.insert.
        how often: Frequently.
        how much: Depends on tree depth and imbalance.
        what is it like: Rebalancing a complex structure.
        how, what, why and when to improve: N/A.
        """
        while z != self.root and z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right # Uncle
                if y and y.color == RED:
                    # Case 1: Uncle is RED
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    # Case 2 & 3: Uncle is BLACK
                    if z == z.parent.right:
                        # Case 2: Left-Right Case
                        z = z.parent
                        self._left_rotate(z)
                    # Case 3: Left-Left Case
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                # Symmetric cases for right child
                y = z.parent.parent.left # Uncle
                if y and y.color == RED:
                    # Case 1: Uncle is RED
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    # Case 2 & 3: Uncle is BLACK
                    if z == z.parent.left:
                        # Case 2: Right-Left Case
                        z = z.parent
                        self._right_rotate(z)
                    # Case 3: Right-Right Case
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _left_rotate(self, x: RedBlackNode):
        """
        what: Performs a left rotation on the Red-Black tree.
        why: To rebalance the tree and maintain Red-Black properties.
        how: Adjusts node pointers and parent references.
        when: During insertion or deletion fix-up.
        by (caller(s)): _fix_insert, _fix_delete.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Shifting a branch in a tree.
        how, what, why and when to improve: N/A.
        """
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: RedBlackNode):
        """
        what: Performs a right rotation on the Red-Black tree.
        why: To rebalance the tree and maintain Red-Black properties.
        how: Adjusts node pointers and parent references.
        when: During insertion or deletion fix-up.
        by (caller(s)): _fix_insert, _fix_delete.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Shifting a branch in a tree.
        how, what, why and when to improve: N/A.
        """
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search(self, weight: float) -> Optional[RedBlackNode]:
        """
        what: Searches for a node with the given weight.
        why: To retrieve a node based on its weight.
        how: Traverses the tree, comparing weights.
        when: When a node needs to be found by its weight.
        by (caller(s)): RedBlackTree.remove.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Finding an item in a sorted list.
        how, what, why and when to improve: Optimize for very large trees.
        """
        node = self.root
        while node:
            if weight == node.eval_weight():
                return node
            elif weight < node.eval_weight():
                node = node.left
            else:
                node = node.right
        return None

    def search(self, weight: float) -> Optional[RedBlackNode]:
        """
        what: Searches for a node with the given weight.
        why: To retrieve a node based on its weight.
        how: Traverses the tree, comparing weights.
        when: When a node needs to be found by its weight.
        by (caller(s)): RedBlackTree.remove.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Finding an item in a sorted list.
        how, what, why and when to improve: Optimize for very large trees.
        """
        node = self.root
        while node:
            if weight == node.eval_weight():
                return node
            elif weight < node.eval_weight():
                node = node.left
            else:
                node = node.right
        return None

    def remove(self, weight: float):
        """
        what: Removes a node with the given weight.
        why: To delete a Symbol from the Red-Black tree.
        how: Finds node, performs deletion, then fixes Red-Black properties.
        when: When a Symbol is deleted from the index.
        by (caller(s)): Symbol.delete.
        how often: Infrequently.
        how much: Depends on tree depth.
        what is it like: Deleting an item from a sorted collection.
        how, what, why and when to improve: Optimize for very large trees.
        """
        z = self.search(weight)
        if not z:
            return

        y = z
        y_original_color = y.color
        if not z.left:
            x = z.right
            self._transplant(z, z.right)
        elif not z.right:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._min_node(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                if x: x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            if x: self._fix_delete(x)

    def _transplant(self, u: RedBlackNode, v: Optional[RedBlackNode]):
        """
        what: Replaces one subtree with another.
        why: Helper for Red-Black tree deletion.
        how: Adjusts parent and child pointers to bypass a node.
        when: During node removal in deletion process.
        by (caller(s)): RedBlackTree.remove.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Swapping out a tree branch.
        how, what, why and when to improve: N/A.
        """
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _min_node(self, node: RedBlackNode) -> RedBlackNode:
        """
        what: Finds the node with the minimum value in a subtree.
        why: Helper for Red-Black tree deletion.
        how: Traverses left children until no more left child.
        when: During deletion of nodes with two children.
        by (caller(s)): RedBlackTree.remove.
        how often: Infrequently.
        how much: Depends on subtree depth.
        what is it like: Finding the smallest element in a branch.
        how, what, why and when to improve: N/A.
        """
        while node.left:
            node = node.left
        return node

    def _fix_delete(self, x: RedBlackNode):
        """
        what: Restores Red-Black tree properties after deletion.
        why: To maintain the self-balancing nature of the tree.
        how: Performs rotations and color changes based on Red-Black rules.
        when: After a node is deleted.
        by (caller(s)): RedBlackTree.remove.
        how often: Infrequently.
        how much: Depends on tree depth and imbalance.
        what is it like: Rebalancing a complex structure.
        how, what, why and when to improve: N/A.
        """
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if (not w.left or w.left.color == BLACK) and \
                   (not w.right or w.right.color == BLACK):
                    w.color = RED
                    x = x.parent
                else:
                    if not w.right or w.right.color == BLACK:
                        if w.left: w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    if w.right: w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if (not w.right or w.right.color == BLACK) and \
                   (not w.left or w.left.color == BLACK):
                    w.color = RED
                    x = x.parent
                else:
                    if not w.left or w.left.color == BLACK:
                        if w.right: w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    if w.left: w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def traverse_inorder(self, node: Optional[RedBlackNode] = None) -> list['Symbol']:
        """
        what: Traverses the Red-Black tree in-order.
        why: To retrieve Symbols in sorted order.
        how: Recursively visits left, current, then right nodes.
        when: When sorted iteration of Symbols is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on tree size.
        what is it like: Reading a sorted list.
        how, what, why and when to improve: Optimize for very large trees.
        """
        if node is None:
            node = self.root
        result = []

        def _walk(n: Optional[RedBlackNode]):
            if not n:
                return
            _walk(n.left)
            result.append(n.symbol)
            _walk(n.right)

        _walk(node)
        return result

    def to_ascii(self) -> str:
        """
        what: Generates an ASCII art representation of the Red-Black tree.
        why: For debugging and visualization of the tree structure.
        how: Recursively walks the tree, formatting nodes with indentation.
        when: When visualizing the Red-Black tree.
        by (caller(s)): External debugging tools.
        how often: Infrequently.
        how much: Depends on tree size.
        what is it like: Drawing a text-based tree diagram.
        how, what, why and when to improve: Improve formatting for large trees.
        """
        lines = []

        def _walk_ascii(node: Optional[RedBlackNode], indent: str = ""):
            if node is None:
                return
            _walk_ascii(node.right, indent + "  ")
            lines.append(f"{indent}- {node.symbol.name} ({'R' if node.color else 'B'})")
            _walk_ascii(node.left, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)
