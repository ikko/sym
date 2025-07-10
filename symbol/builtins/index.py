"""This module provides index capabilities for Symbol objects.

It allows for creating and managing indexes on Symbol attributes,
and provides methods for rebalancing the index using different strategies.
"""
from typing import Any, Union, Optional, Callable, Literal

from ..core.base_symbol import Symbol
from .avl_tree import AVLTree
from .red_black_tree import RedBlackTree

ENABLE_ORIGIN = True
MEMORY_AWARE_DELETE = True

class SymbolIndex:
    def __init__(self, owner: 'Symbol'):
        """
        what: Initializes a SymbolIndex instance.
        why: To create an index for Symbols, typically for a Symbol's children.
        how: Stores the owner Symbol and initializes an AVLTree for storage.
        when: When a Symbol's index is accessed for the first time.
        by (caller(s)): Symbol.index property.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating a sorted list for a collection.
        how, what, why and when to improve: N/A.
        """
        self.owner = owner
        self.tree: Optional[AVLTree] = AVLTree() # Use AVLTree for underlying storage

    def insert(self, symbol: 'Symbol', weight: Union[float, Callable]):
        """
        what: Inserts a Symbol into the index.
        why: To add a Symbol to the indexed collection.
        how: Delegates to the underlying AVLTree's insert method.
        when: When a Symbol is added to the indexed collection.
        by (caller(s)): Symbol.__new__.
        how often: Frequently.
        how much: Depends on tree depth.
        what is it like: Adding an item to a sorted index.
        how, what, why and when to improve: Optimize for very large indexes.
        """
        self.tree.root = self.tree.insert(self.tree.root, symbol, weight)

    def map(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        """
        what: Applies a function to each Symbol in the index.
        why: To transform each Symbol in the indexed collection.
        how: Traverses the index in-order and applies the function.
        when: When transforming a collection of indexed Symbols.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Applying a transformation to a list.
        how, what, why and when to improve: Optimize for large collections.
        """
        return [fn(sym) for sym in self.traverse(order="in")]

    def filter(self, pred: Callable[['Symbol'], bool]) -> list['Symbol']:
        """
        what: Filters Symbols in the index based on a predicate.
        why: To select Symbols that satisfy a specific condition.
        how: Traverses the index in-order and applies the predicate.
        when: When searching for specific Symbols in the index.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Filtering a list.
        how, what, why and when to improve: Optimize for large collections.
        """
        return [sym for sym in self.traverse(order="in") if pred(sym)]

    def traverse(self, order: Literal["in", "pre", "post"] = "in") -> list['Symbol']:
        """
        what: Traverses the index in a specified order.
        why: To retrieve Symbols from the index in a structured way.
        how: Delegates to the underlying AVLTree's traversal methods.
        when: When iterating over indexed Symbols.
        by (caller(s)): SymbolIndex.map, SymbolIndex.filter.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Walking through a sorted collection.
        how, what, why and when to improve: Implement more traversal orders.
        """
        if order == "in":
            return self.tree.traverse_inorder()
        # Pre-order and Post-order traversals are not directly supported by AVLTree
        # For now, return in-order for other requests or raise an error
        raise NotImplementedError(f"Traversal order '{order}' not implemented for SymbolIndex.")

    def rebalance(self, strategy: Literal['avl', 'red_black', 'weight', 'hybrid'] = 'weight') -> None:
        """
        what: Rebalances the index using a specified strategy.
        why: To optimize the index for performance after modifications.
        how: Delegates to the underlying tree's rebalancing mechanism.
        when: After significant insertions or deletions.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on index size.
        what is it like: Optimizing a database index.
        how, what, why and when to improve: Implement more rebalancing strategies.
        """
        # Rebalancing is handled by the underlying AVLTree on insertion
        # For other strategies, a new tree would need to be built
        if strategy == 'avl':
            pass # AVLTree is self-balancing
        else:
            raise NotImplementedError(f"Rebalancing strategy '{strategy}' not implemented for SymbolIndex.")

    def remove(self, symbol: 'Symbol') -> None:
        """
        what: Removes a Symbol from the index.
        why: To delete a Symbol from the indexed collection.
        how: Delegates to the underlying AVLTree's remove method.
        when: When a Symbol is deleted.
        by (caller(s)): Symbol.delete.
        how often: Infrequently.
        how much: Depends on tree depth.
        what is it like: Removing an item from a sorted index.
        how, what, why and when to improve: Optimize for very large indexes.
        """
        self.tree.remove(symbol._position)

    def ascii(self):
        """
        what: Generates an ASCII art representation of the index.
        why: For debugging and visualization of the index structure.
        how: Delegates to the underlying AVLTree's `to_ascii` method.
        when: When visualizing the index.
        by (caller(s)): External debugging tools.
        how often: Infrequently.
        how much: Depends on index size.
        what is it like: Drawing a text-based tree diagram.
        how, what, why and when to improve: Improve formatting for large indexes.
        """
        return self.tree.to_ascii()

    def to_ascii(self) -> str:
        """
        what: Generates an ASCII art representation of the index.
        why: Alias for `ascii` method.
        how: Delegates to the `ascii` method.
        when: When visualizing the index.
        by (caller(s)): External debugging tools.
        how often: Infrequently.
        how much: Depends on index size.
        what is it like: Drawing a text-based tree diagram.
        how, what, why and when to improve: N/A.
        """
        return self.ascii()
