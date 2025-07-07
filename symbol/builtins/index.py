"""This module provides index capabilities for Symbol objects.

It allows for creating and managing indexes on Symbol attributes,
and provides methods for rebalancing the index using different strategies.
"""
import datetime
import orjson
from typing import Any, Union, Optional, Callable, Literal

from ..core.base_symbol import Symbol
from .avl_tree import AVLTree
from .red_black_tree import RedBlackTree

ENABLE_ORIGIN = True
MEMORY_AWARE_DELETE = True


class IndexNode:
    def __init__(self, symbol: 'Symbol', weight: Union[float, Callable[[Any], float]] = 0.0):
        self.symbol = symbol
        self.left: Optional['IndexNode'] = None
        self.right: Optional['IndexNode'] = None
        self.weight = weight

    def eval_weight(self) -> float:
        return self.weight(self.symbol) if callable(self.weight) else self.weight


class SymbolIndex:
    def __init__(self, owner: 'Symbol'):
        self.owner = owner
        self.root: Optional[IndexNode] = None
        self._function_map = {}  # {name: IndexNode}

    def insert(self, symbol: 'Symbol', weight: Union[float, Callable]):
        def _insert(node: Optional[IndexNode], sym: Symbol) -> IndexNode:
            if node is None:
                new_node = IndexNode(sym, weight)
                self._function_map[sym.name] = new_node
                return new_node
            # Evaluate the weight of the symbol being inserted for comparison
            # The IndexNode itself will store the original weight (callable or float)
            if (weight(sym) if callable(weight) else weight) < node.eval_weight():
                node.left = _insert(node.left, sym)
            else:
                node.right = _insert(node.right, sym)
            return node

        self.root = _insert(self.root, symbol)

    def map(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        return [fn(sym) for sym in self.traverse(order="in")]

    def filter(self, pred: Callable[['Symbol'], bool]) -> list['Symbol']:
        return [sym for sym in self.traverse(order="in") if pred(sym)]

    def traverse(self, order: Literal["in", "pre", "post"] = "in") -> list['Symbol']:
        result = []

        def _walk(node: Optional[IndexNode]):
            if node is None:
                return
            if order == "pre":
                result.append(node.symbol)
            _walk(node.left)
            if order == "in":
                result.append(node.symbol)
            _walk(node.right)
            if order == "post":
                result.append(node.symbol)

        _walk(self.root)
        return result

    def rebalance(self, strategy: Literal['avl', 'red_black', 'weight', 'hybrid'] = 'weight') -> None:
        syms = self.traverse(order='in')
        weights = [(s, self._function_map[s.name].eval_weight()) for s in syms]

        if strategy == 'weight':
            weights.sort(key=lambda pair: pair[1])

            def build_balanced(sorted_syms):
                if not sorted_syms:
                    return None
                mid = len(sorted_syms) // 2
                node = IndexNode(sorted_syms[mid][0], sorted_syms[mid][1])
                node.left = build_balanced(sorted_syms[:mid])
                node.right = build_balanced(sorted_syms[mid + 1:])
                return node

            self.root = build_balanced(weights)

        elif strategy == 'avl':
            tree = AVLTree()
            root = None
            for sym, w in weights:
                root = tree.insert(root, sym, w)
            from .avl_tree import AVLNode
            def copy_from_avl(node: Optional[AVLNode]) -> Optional[IndexNode]:
                if not node:
                    return None
                n = IndexNode(node.symbol, node.weight)
                n.left = copy_from_avl(node.left)
                n.right = copy_from_avl(node.right)
                return n
            self.root = copy_from_avl(root)

        elif strategy == 'red_black':
            tree = RedBlackTree()
            for sym, w in weights:
                tree.insert(sym, w)
            from .red_black_tree import RedBlackNode
            def copy_from_rbt(node: Optional[RedBlackNode]) -> Optional[IndexNode]:
                if not node:
                    return None
                n = IndexNode(node.symbol, node.weight)
                n.left = copy_from_rbt(node.left)
                n.right = copy_from_rbt(node.right)
                return n
            self.root = copy_from_rbt(tree.root)
            now = datetime.datetime.now()
            def hybrid_weight(sym: 'Symbol'):
                try:
                    ts = datetime.datetime.fromisoformat(sym.name)
                except Exception:
                    ts = now
                age = (now - ts).total_seconds()
                return self._function_map[sym.name].eval_weight() + (1 / (1 + age))

            weights = [(s, hybrid_weight(s)) for s in syms]
            weights.sort(key=lambda pair: pair[1])
            def build_balanced(sorted_syms):
                if not sorted_syms:
                    return None
                mid = len(sorted_syms) // 2
                node = IndexNode(sorted_syms[mid][0], sorted_syms[mid][1])
                node.left = build_balanced(sorted_syms[:mid])
                node.right = build_balanced(sorted_syms[mid + 1:])
                return node
            self.root = build_balanced(weights)

    def remove(self, symbol: 'Symbol') -> None:
        def _remove(node: Optional[IndexNode], sym: Symbol) -> Optional[IndexNode]:
            if node is None:
                return None

            if sym == node.symbol:
                # Node to be deleted found
                del self._function_map[sym.name]

                if node.left is None and node.right is None:
                    return None  # No children
                elif node.left is None:
                    return node.right  # Only right child
                elif node.right is None:
                    return node.left  # Only left child
                else:
                    # Node has two children, find in-order successor
                    successor = node.right
                    while successor.left:
                        successor = successor.left
                    node.symbol = successor.symbol
                    node.weight = successor.weight
                    node.right = _remove(node.right, successor.symbol)
            elif (self._function_map[sym.name].eval_weight() if sym.name in self._function_map else -float('inf')) < node.eval_weight():
                node.left = _remove(node.left, sym)
            else:
                node.right = _remove(node.right, sym)
            return node

        self.root = _remove(self.root, symbol)

    def __getattr__(self, name: str):
        node = self._function_map.get(name)
        if node is None:
            raise AttributeError(f"No function named {name!r} in index")
        func = getattr(node.symbol, name, None)
        if not callable(func):
            raise TypeError(f"{name!r} is not callable on symbol {node.symbol}")

        def wrapped(*args, **kwargs):
            self.before(*args, **kwargs)
            result = func(*args, **kwargs)
            self.after(*args, **kwargs)
            return result

        return wrapped

    def before(self, *args, **kwargs):
        print(f"[Before] index call with args={args} kwargs={kwargs}")

    def after(self, *args, **kwargs):
        print(f"[After] index call with args={args} kwargs={kwargs}")

    def ascii(self):
        lines = []

        def _walk(node: Optional[IndexNode], depth: int = 0):
            if node is None:
                return
            _walk(node.right, depth + 1)
            lines.append("    " * depth + f"- {node.symbol.name}")
            _walk(node.left, depth + 1)

        _walk(self.root)
        return "\n".join(lines)

    def to_ascii(self) -> str:
        return self.ascii()


# Patch Symbol class (assume it exists in the scope):
# Already mounted via Symbol.__new__: obj.index = SymbolIndex(obj)
