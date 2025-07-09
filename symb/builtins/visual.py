"""This module provides visualization capabilities for Symbol objects.

It allows for rendering Symbol graphs to various formats, such as DOT, SVG, PNG, and Mermaid.
"""
from __future__ import annotations
from typing import Literal, Optional
import anyio
import warnings

try:
    import graphviz
    _GRAPHVIZ_AVAILABLE = True
except ImportError:
    _GRAPHVIZ_AVAILABLE = False

from ..core.protocols import SymbolVisualProtocol


class SymbolRender(SymbolVisualProtocol):
    def __init__(self, root: 'Symbol'):
        self.root = root

    def _build_dot_source(self, mode: Literal["tree", "graph"]) -> str:
        seen = set()
        lines = ["digraph G {"]

        def escape(sym):
            return f'"{sym.name}"'

        def walk(sym):
            if sym in seen:
                return
            seen.add(sym)
            if mode == "tree":
                for child in sym.children:
                    lines.append(f"{escape(sym)} -> {escape(child)}")
                    walk(child)
            elif mode == "graph":
                # Assuming 'related_to' or similar for generic graph traversal
                # For now, using children for simplicity, but this could be extended
                for neighbor in sym.children:
                    lines.append(f"{escape(sym)} -> {escape(neighbor)}")
                    walk(neighbor)

        walk(self.root)
        lines.append("}")
        return "\n".join(lines)

    def to_dot(self, mode: Literal["tree", "graph"] = "tree") -> str:
        if not _GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz is not installed. Please install it with `pip install 'symb[visual]'`.")
        return self._build_dot_source(mode)

    async def a_to_svg(self, mode: Literal["tree", "graph"] = "tree") -> str:
        if not _GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz is not installed. Please install it with `pip install 'symb[visual]'`.")
        dot = self._build_dot_source(mode)
        # Run in a thread pool to avoid blocking the event loop
        return await anyio.to_thread.run_sync(lambda: graphviz.Source(dot).pipe(format="svg").decode())

    def to_svg(self, mode: Literal["tree", "graph"] = "tree") -> str:
        return anyio.run(self.a_to_svg, mode)

    async def a_to_png(self, mode: Literal["tree", "graph"] = "tree") -> bytes:
        if not _GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz is not installed. Please install it with `pip install 'symb[visual]'`.")
        dot = self._build_dot_source(mode)
        # Run in a thread pool to avoid blocking the event loop
        return await anyio.to_thread.run_sync(lambda: graphviz.Source(dot).pipe(format="png"))

    def to_png(self, mode: Literal["tree", "graph"] = "tree") -> bytes:
        return anyio.run(self.a_to_png, mode)

    def to_mmd(self, mode: Literal["tree", "graph"] = "tree") -> str:
        seen = set()
        lines = ["graph TD"] if mode == "tree" else ["graph LR"]

        def esc(sym):
            return sym.name.replace(" ", "_")

        def walk(sym):
            if sym in seen:
                return
            seen.add(sym)
            if mode == "tree":
                for child in sorted(sym.children, key=lambda s: s.name):
                    lines.append(f"{esc(sym)} --> {esc(child)}")
                    walk(child)
            elif mode == "graph":
                for neighbor in sym.children:
                    lines.append(f"{esc(sym)} --> {esc(neighbor)}")
                    walk(neighbor)

        walk(self.root)
        header = lines[0]
        sorted_lines = sorted(lines[1:])
        return header + "\n" + "\n".join(sorted_lines)

    def to_ascii(self, mode: Literal["tree", "graph"] = "tree") -> str:
        # This will be handled by the Symbol's own to_ascii method, or a dedicated GraphTraversal
        # For now, a placeholder or direct call to Symbol's method
        if mode == "tree":
            return self.root.to_ascii()
        else:
            # For generic graph, we might need a more sophisticated ASCII renderer
            # For simplicity, let's just use the tree representation for now
            return self.root.to_ascii()
