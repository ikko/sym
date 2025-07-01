from typing import Optional, Union, Callable, Any

RED = True
BLACK = False

class RedBlackNode:
    def __init__(self, symbol: 'Symbol', weight: Union[float, Callable[[Any], float]], color=RED):
        self.symbol = symbol
        self.weight = weight
        self.color = color
        self.left: Optional['RedBlackNode'] = None
        self.right: Optional['RedBlackNode'] = None
        self.parent: Optional['RedBlackNode'] = None

    def eval_weight(self, *args, **kwargs) -> float:
        return self.weight(*args, **kwargs) if callable(self.weight) else self.weight


class RedBlackTree:
    def __init__(self):
        self.root: Optional[RedBlackNode] = None

    def insert(self, symbol: 'Symbol', weight: Union[float, Callable]):
        node = RedBlackNode(symbol, weight)
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
        while z != self.root and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
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

    def traverse_inorder(self, node: Optional[RedBlackNode] = None) -> list['Symbol']:
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
        lines = []

        def _walk_ascii(node: Optional[RedBlackNode], indent: str = ""):
            if node is None:
                return
            _walk_ascii(node.right, indent + "  ")
            lines.append(f"{indent}- {node.symbol.name} ({'R' if node.color else 'B'})")
            _walk_ascii(node.left, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)
