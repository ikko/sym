import warnings

from .symbol import Symbol


class GraphTraversal:
    def __init__(self, root: 'Symbol', mode: str = 'graph'):
        self.root = root
        self.mode = mode  # 'graph' or 'tree'
        self.visited = set()
        self.result = []

    def traverse(self):
        self._walk(self.root)
        return self.result

    def _walk(self, symbol: 'Symbol'):
        if symbol in self.visited:
            warnings.warn(f"Cycle detected in {self.mode} at {symbol}")
            return
        self.visited.add(symbol)
        self.result.append(symbol)
        neighbors = symbol.children if self.mode == 'tree' else symbol.children
        for child in neighbors:
            self._walk(child)

    def to_ascii(self) -> str:
        lines = []
        visited_ascii = set()

        def _walk_ascii(symbol: 'Symbol', indent: str = ""):
            if symbol in visited_ascii:
                return
            visited_ascii.add(symbol)
            lines.append(f"{indent}- {symbol.name}")
            for child in symbol.children:
                _walk_ascii(child, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)
