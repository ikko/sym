"""This module provides index capabilities for Symbol objects.

It allows for creating and managing indexes on Symbol attributes,
and provides methods for rebalancing the index using different strategies.
"""
from typing import Any, Union, Optional, Callable, Literal

from ..core.base_symb import Symbol
from .avl_tree import AVLTree
from .red_black_tree import RedBlackTree

ENABLE_ORIGIN = True
MEMORY_AWARE_DELETE = True

class SymbolIndex:
    def __init__(self, owner: 'Symbol'):
        self.owner = owner
        self.tree: Optional[AVLTree] = AVLTree() # Use AVLTree for underlying storage

    def insert(self, symb: 'Symbol', weight: Union[float, Callable]):
        self.tree.root = self.tree.insert(self.tree.root, symb, weight)

    def map(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        return [fn(sym) for sym in self.traverse(order="in")]

    def filter(self, pred: Callable[['Symbol'], bool]) -> list['Symbol']:
        return [sym for sym in self.traverse(order="in") if pred(sym)]

    def traverse(self, order: Literal["in", "pre", "post"] = "in") -> list['Symbol']:
        if order == "in":
            return self.tree.traverse_inorder()
        # Pre-order and Post-order traversals are not directly supported by AVLTree
        # For now, return in-order for other requests or raise an error
        raise NotImplementedError(f"Traversal order '{order}' not implemented for SymbolIndex.")

    def rebalance(self, strategy: Literal['avl', 'red_black', 'weight', 'hybrid'] = 'weight') -> None:
        # Rebalancing is handled by the underlying AVLTree on insertion
        # For other strategies, a new tree would need to be built
        if strategy == 'avl':
            pass # AVLTree is self-balancing
        else:
            raise NotImplementedError(f"Rebalancing strategy '{strategy}' not implemented for SymbolIndex.")

    def remove(self, symb: 'Symbol') -> None:
        self.tree.remove(symb._position)

    def ascii(self):
        return self.tree.to_ascii()

    def to_ascii(self) -> str:
        return self.ascii()
