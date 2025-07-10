"""This module provides an implementation of an AVL tree.

An AVL tree is a self-balancing binary search tree that maintains a balanced height,
ensuring efficient search, insertion, and deletion operations.
"""
from __future__ import annotations
from typing import Optional, Union, Callable, Any

class AVLNode:
    def __init__(self, symbol: 'Symbol', weight: Union[float, Callable[[Any], float]]):
        """
        what: Initializes an AVL tree node.
        why: To store a Symbol and its associated weight in the tree.
        how: Sets symbol, weight, initial height, and child pointers.
        when: When a new node is added to the AVL tree.
        by (caller(s)): AVLTree.insert.
        how often: Frequently.
        how much: Minimal.
        what is it like: Creating a new entry in a sorted list.
        how, what, why and when to improve: N/A.
        """
        self.symbol = symbol
        self.weight = weight
        self.height = 1
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None

    def eval_weight(self, *args, **kwargs) -> float:
        """
        what: Evaluates the node's weight.
        why: To get a numerical value for comparison in the AVL tree.
        how: Calls the weight if callable, otherwise returns it directly.
        when: During tree operations (insert, search, remove).
        by (caller(s)): AVLTree methods.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting a sort key.
        how, what, why and when to improve: N/A.
        """
        return self.weight(self.symbol) if callable(self.weight) else self.weight


class AVLTree:
    def __init__(self):
        """
        what: Initializes an empty AVL tree.
        why: To create a self-balancing binary search tree for Symbols.
        how: Sets the root node to None.
        when: When a new AVLTree is instantiated.
        by (caller(s)): SymbolIndex.__init__.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating an empty sorted collection.
        how, what, why and when to improve: N/A.
        """
        self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        """
        what: Returns the height of a node.
        why: To calculate balance factors for tree rebalancing.
        how: Returns node's height or 0 if node is None.
        when: During rebalancing operations.
        by (caller(s)): _update_height, _balance_factor.
        how often: Frequently.
        how much: Minimal.
        what is it like: Measuring a subtree's depth.
        how, what, why and when to improve: N/A.
        """
        return node.height if node else 0

    def _update_height(self, node: AVLNode) -> None:
        """
        what: Updates the height of a node.
        why: To maintain correct height information after tree modifications.
        how: Sets height based on max height of children plus one.
        when: After insertions, deletions, or rotations.
        by (caller(s)): _rotate_left, _rotate_right, _rebalance.
        how often: Frequently.
        how much: Minimal.
        what is it like: Recalculating a subtree's depth.
        how, what, why and when to improve: N/A.
        """
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        """
        what: Calculates the balance factor of a node.
        why: To determine if a node is out of balance.
        how: Subtracts right child's height from left child's height.
        when: During rebalancing operations.
        by (caller(s)): _rebalance.
        how often: Frequently.
        how much: Minimal.
        what is it like: Checking a subtree's balance.
        how, what, why and when to improve: N/A.
        """
        return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """
        what: Performs a left rotation on the AVL tree.
        why: To rebalance the tree after an insertion or deletion.
        how: Adjusts node pointers and updates heights.
        when: When a right-heavy imbalance is detected.
        by (caller(s)): _rebalance.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Shifting a branch in a tree.
        how, what, why and when to improve: N/A.
        """
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """
        what: Performs a right rotation on the AVL tree.
        why: To rebalance the tree after an insertion or deletion.
        how: Adjusts node pointers and updates heights.
        when: When a left-heavy imbalance is detected.
        by (caller(s)): _rebalance.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Shifting a branch in a tree.
        how, what, why and when to improve: N/A.
        """
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        self._update_height(z)
        self._update_height(y)

        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        what: Rebalances a node in the AVL tree.
        why: To maintain the AVL tree's self-balancing property.
        how: Performs rotations based on balance factor.
        when: After insertions or deletions.
        by (caller(s)): insert, _remove.
        how often: Frequently.
        how much: Minimal.
        what is it like: Restoring equilibrium to a structure.
        how, what, why and when to improve: N/A.
        """
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left Left Case
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right Case
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left Case
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, node: Optional[AVLNode], symbol: 'Symbol', weight: Union[float, Callable]) -> AVLNode:
        """
        what: Inserts a Symbol into the AVL tree.
        why: To add a new Symbol while maintaining tree balance.
        how: Recursively finds insertion point, creates node, rebalances.
        when: When a new Symbol is created and added to the index.
        by (caller(s)): Symbol.__new__.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Adding an item to a sorted collection.
        how, what, why and when to improve: Optimize for very large trees.
        """
        if not node:
            return AVLNode(symbol, weight)

        if (weight(symbol) if callable(weight) else weight) < node.eval_weight():
            node.left = self.insert(node.left, symbol, weight)
        else:
            node.right = self.insert(node.right, symbol, weight)

        return self._rebalance(node)

    def search(self, weight: float) -> Optional['Symbol']:
        """
        what: Searches for a Symbol with the given weight.
        why: To retrieve a Symbol based on its weight.
        how: Traverses the tree, comparing weights.
        when: When a Symbol needs to be found by its weight.
        by (caller(s)): Symbol.seek, Symbol.prev.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Finding an item in a sorted list.
        how, what, why and when to improve: Optimize for very large trees.
        """
        node = self.root
        while node:
            if weight == node.eval_weight():
                return node.symbol
            elif weight < node.eval_weight():
                node = node.left
            else:
                node = node.right
        return None

    def remove(self, weight: float) -> Optional[AVLNode]:
        """
        what: Removes a node with the given weight.
        why: To delete a Symbol from the AVL tree.
        how: Calls recursive `_remove` method.
        when: When a Symbol is deleted from the index.
        by (caller(s)): Symbol.delete.
        how often: Infrequently.
        how much: Depends on tree depth.
        what is it like: Deleting an item from a sorted collection.
        how, what, why and when to improve: Optimize for very large trees.
        """
        self.root = self._remove(self.root, weight)
        return self.root

    def _remove(self, node: Optional[AVLNode], weight: float) -> Optional[AVLNode]:
        """
        what: Recursively removes a node from the AVL tree.
        why: Internal helper for deletion logic.
        how: Handles various deletion cases (no child, one child, two children).
        when: Called during `remove` operation.
        by (caller(s)): AVLTree.remove.
        how often: Infrequently.
        how much: Depends on tree depth.
        what is it like: Internal tree manipulation.
        how, what, why and when to improve: N/A.
        """
        if not node:
            return node

        if weight < node.eval_weight():
            node.left = self._remove(node.left, weight)
        elif weight > node.eval_weight():
            node.right = self._remove(node.right, weight)
        else:
            # Node with the given weight found

            # Case 1: Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Case 2: Node with two children
            # Get the in-order successor (smallest in the right subtree)
            temp = self._min_value_node(node.right)
            node.symbol = temp.symbol
            node.weight = temp.weight
            node.right = self._remove(node.right, temp.weight)

        # Rebalance the current node after deletion (or recursive calls)
        return self._rebalance(node)

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        """
        what: Finds the node with the minimum value in a subtree.
        why: Helper for deletion when a node has two children.
        how: Traverses left children until no more left child.
        when: During deletion of nodes with two children.
        by (caller(s)): _remove.
        how often: Infrequently.
        how much: Depends on subtree depth.
        what is it like: Finding the smallest element in a branch.
        how, what, why and when to improve: N/A.
        """
        current = node
        while current.left:
            current = current.left
        return current

    def min_node(self) -> Optional[AVLNode]:
        """
        what: Finds the node with the minimum value in the tree.
        why: To get the smallest Symbol in the collection.
        how: Calls `_min_value_node` starting from the root.
        when: When the smallest Symbol is needed.
        by (caller(s)): Symbol.first.
        how often: Infrequently.
        how much: Depends on tree depth.
        what is it like: Finding the smallest element.
        how, what, why and when to improve: Optimize for very large trees.
        """
        if not self.root:
            return None
        return self._min_value_node(self.root)

    def max_node(self) -> Optional[AVLNode]:
        """
        what: Finds the node with the maximum value in the tree.
        why: To get the largest Symbol in the collection.
        how: Traverses right children until no more right child.
        when: When the largest Symbol is needed.
        by (caller(s)): Symbol.last.
        how often: Infrequently.
        how much: Depends on tree depth.
        what is it like: Finding the largest element.
        how, what, why and when to improve: Optimize for very large trees.
        """
        if not self.root:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current

    def traverse_inorder(self, node: Optional[AVLNode] = None) -> list['Symbol']:
        """
        what: Traverses the AVL tree in-order.
        why: To retrieve Symbols in sorted order.
        how: Recursively visits left, current, then right nodes.
        when: When sorted iteration of Symbols is needed.
        by (caller(s)): AVLTree.__iter__, Symbol.each.
        how often: Infrequently.
        how much: Depends on tree size.
        what is it like: Reading a sorted list.
        how, what, why and when to improve: Optimize for very large trees.
        """
        if node is None:
            node = self.root
        result = []

        def _walk(n: Optional[AVLNode]):
            if not n:
                return
            _walk(n.left)
            result.append(n.symbol)
            _walk(n.right)

        _walk(node)
        return result

    def __iter__(self):
        """
        what: Provides an iterator for the AVL tree.
        why: To allow direct iteration over Symbols in sorted order.
        how: Delegates to `traverse_inorder`.
        when: When iterating over Symbols in the tree.
        by (caller(s)): Python's iteration mechanism.
        how often: Infrequently.
        how much: Depends on tree size.
        what is it like: Looping through a sorted collection.
        how, what, why and when to improve: N/A.
        """
        return iter(self.traverse_inorder())

    def to_ascii(self) -> str:
        """
        what: Generates an ASCII art representation of the AVL tree.
        why: For debugging and visualization of the tree structure.
        how: Recursively walks the tree, formatting nodes with indentation.
        when: When visualizing the AVL tree.
        by (caller(s)): External debugging tools.
        how often: Infrequently.
        how much: Depends on tree size.
        what is it like: Drawing a text-based tree diagram.
        how, what, why and when to improve: Improve formatting for large trees.
        """
        lines = []

        def _walk_ascii(node: Optional[AVLNode], indent: str = ""):
            if node is None:
                return
            _walk_ascii(node.right, indent + "  ")
            lines.append(f"{indent}- {node.symbol.name} (W:{node.eval_weight():.2f}, H:{node.height})")
            _walk_ascii(node.left, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)
