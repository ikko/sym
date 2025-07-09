"""This module provides an implementation of a red-black tree.

A red-black tree is a self-balancing binary search tree that maintains a balanced height,
ensuring efficient search, insertion, and deletion operations.
"""
from typing import Any, Callable, Optional, Union

from ..core.base_symb import Symbol

RED = True
BLACK = False

class RedBlackNode:
    def __init__(self, symb: 'Symbol', weight: Union[float, Callable[[Any], float]], color=RED):
        self.symb = symb
        self.weight = weight
        self.color = color
        self.left: Optional['RedBlackNode'] = None
        self.right: Optional['RedBlackNode'] = None
        self.parent: Optional['RedBlackNode'] = None

    def eval_weight(self, *args, **kwargs) -> float:
        return self.weight(self.symb) if callable(self.weight) else self.weight


class RedBlackTree:
    def __init__(self):
        self.root: Optional[RedBlackNode] = None

    def insert(self, symb: 'Symbol', weight: Union[float, Callable]):
        node = RedBlackNode(symb, weight)
        self._bst_insert(node)
        self._fix_insert(node)

    def _bst_insert(self, z: RedBlackNode):
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
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _min_node(self, node: RedBlackNode) -> RedBlackNode:
        while node.left:
            node = node.left
        return node

    def _fix_delete(self, x: RedBlackNode):
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
        if node is None:
            node = self.root
        result = []

        def _walk(n: Optional[RedBlackNode]):
            if not n:
                return
            _walk(n.left)
            result.append(n.symb)
            _walk(n.right)

        _walk(node)
        return result

    def to_ascii(self) -> str:
        lines = []

        def _walk_ascii(node: Optional[RedBlackNode], indent: str = ""):
            if node is None:
                return
            _walk_ascii(node.right, indent + "  ")
            lines.append(f"{indent}- {node.symb.name} ({'R' if node.color else 'B'})")
            _walk_ascii(node.left, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)
