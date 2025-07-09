"""This module provides an implementation of an AVL tree.

An AVL tree is a self-balancing binary search tree that maintains a balanced height,
ensuring efficient search, insertion, and deletion operations.
"""
from __future__ import annotations
from typing import Optional, Union, Callable, Any

class AVLNode:
    def __init__(self, symb: 'Symbol', weight: Union[float, Callable[[Any], float]]):
        self.symb = symb
        self.weight = weight
        self.height = 1
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None

    def eval_weight(self, *args, **kwargs) -> float:
        return self.weight(self.symb) if callable(self.weight) else self.weight


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        self._update_height(z)
        self._update_height(y)

        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
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

    def insert(self, node: Optional[AVLNode], symb: 'Symbol', weight: Union[float, Callable]) -> AVLNode:
        if not node:
            return AVLNode(symb, weight)

        if (weight(symb) if callable(weight) else weight) < node.eval_weight():
            node.left = self.insert(node.left, symb, weight)
        else:
            node.right = self.insert(node.right, symb, weight)

        return self._rebalance(node)

    def search(self, weight: float) -> Optional['Symbol']:
        """Searches for a symb with the given weight."""
        node = self.root
        while node:
            if weight == node.eval_weight():
                return node.symb
            elif weight < node.eval_weight():
                node = node.left
            else:
                node = node.right
        return None

    def remove(self, weight: float) -> Optional[AVLNode]:
        """Removes a node with the given weight from the tree."""
        self.root = self._remove(self.root, weight)
        return self.root

    def _remove(self, node: Optional[AVLNode], weight: float) -> Optional[AVLNode]:
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
            node.symb = temp.symb
            node.weight = temp.weight
            node.right = self._remove(node.right, temp.weight)

        # Rebalance the current node after deletion (or recursive calls)
        return self._rebalance(node)

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left:
            current = current.left
        return current

    def min_node(self) -> Optional[AVLNode]:
        if not self.root:
            return None
        return self._min_value_node(self.root)

    def max_node(self) -> Optional[AVLNode]:
        if not self.root:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current

    def traverse_inorder(self, node: Optional[AVLNode] = None) -> list['Symbol']:
        if node is None:
            node = self.root
        result = []

        def _walk(n: Optional[AVLNode]):
            if not n:
                return
            _walk(n.left)
            result.append(n.symb)
            _walk(n.right)

        _walk(node)
        return result

    def __iter__(self):
        return iter(self.traverse_inorder())

    def to_ascii(self) -> str:
        lines = []

        def _walk_ascii(node: Optional[AVLNode], indent: str = ""):
            if node is None:
                return
            _walk_ascii(node.right, indent + "  ")
            lines.append(f"{indent}- {node.symb.name} (W:{node.eval_weight():.2f}, H:{node.height})")
            _walk_ascii(node.left, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)
