"""This module provides pathfinding capabilities for Symbol objects.

It includes a mixin that adds methods for finding paths between Symbols
and for matching Symbols based on a predicate.
"""
from __future__ import annotations
from typing import Callable, Iterator, List

from ..core.protocols import SymbolPathProtocol

class SymbolPathMixin(SymbolPathProtocol):
    def path_to(self, target: 'Symbol') -> list['Symbol']:
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
