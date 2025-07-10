"""This module provides pathfinding capabilities for Symbol objects.

It includes a mixin that adds methods for finding paths between Symbols
and for matching Symbols based on a predicate.
"""
from __future__ import annotations
from typing import Callable, Iterator, List

from ..core.protocols import SymbolPathProtocol

class SymbolPathMixin(SymbolPathProtocol):
    __slots__ = ('_init_time',)

    def __init__(self):
        """
        what: Initializes the SymbolPathMixin instance.
        why: To set up the mixin for pathfinding operations.
        how: Records the initialization time.
        when: Upon instantiation of a Symbol with this mixin.
        by (caller(s)): Symbol class instantiation.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Setting up a tool.
        how, what, why and when to improve: N/A.
        """
        self._init_time = datetime.datetime.now()
    def path_to(self, target: 'Symbol') -> list['Symbol']:
        """
        what: Finds a path from this Symbol to a target Symbol.
        why: To determine connectivity and sequence in the graph.
        how: Uses a depth-first search (DFS) algorithm.
        when: When a path between two Symbols is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on graph size and path length.
        what is it like: Navigating a maze.
        how, what, why and when to improve: Optimize for large graphs, implement BFS option.
        """
        visited = set()
        path = []

        def dfs(node: 'Symbol') -> bool:
            if node in visited:
                return False
            visited.add(node)
            path.append(node)
            if node == target:
                return True
            for child in node.children:
                if dfs(child):
                    return True
            path.pop()
            return False

        if dfs(self):
            return path
        return []

    def match(self, predicate: Callable[['Symbol'], bool], traversal: str = 'dfs') -> Iterator['Symbol']:
        """
        what: Finds Symbols matching a predicate.
        why: To filter Symbols based on custom criteria.
        how: Traverses the graph using DFS or BFS, applies predicate.
        when: When searching for specific Symbols in the graph.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on graph size and predicate complexity.
        what is it like: Searching for specific items in a collection.
        how, what, why and when to improve: Optimize traversal, add more traversal options.
        """
        visited = set()

        def dfs(node: 'Symbol'):
            if node in visited:
                return
            visited.add(node)
            if predicate(node):
                yield node
            for child in node.children:
                yield from dfs(child)

        def bfs(start: 'Symbol'):
            queue = [start]
            while queue:
                node = queue.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                if predicate(node):
                    yield node
                queue.extend(node.children)

        if traversal == 'bfs':
            yield from bfs(self)
        else:
            yield from dfs(self)

# Attach at runtime:
# Symbol.path_to = SymbolPathMixin.path_to
# Symbol.match = SymbolPathMixin.match
