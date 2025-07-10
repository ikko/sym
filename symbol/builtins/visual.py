"""This module provides visualization capabilities for Symbol objects.

It allows for rendering Symbol graphs to various formats, such as DOT, SVG, PNG, and Mermaid.
"""
from __future__ import annotations
import datetime
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
    __slots__ = ('_init_time',)

    def __init__(self, root: 'Symbol'):
        """
        what: Initializes the SymbolRender instance.
        why: To prepare the renderer with a root symbol.
        how: Stores the provided root symbol.
        when: Upon instantiation of SymbolRender.
        by (caller(s)): Symbol.stat, Symbol.ls, Symbol.ps.
        how often: Infrequently, when creating new renderers.
        how much: Minimal, just object reference.
        what is it like: Setting up a drawing canvas.
        how, what, why and when to improve: N/A.
        """
        self._init_time = datetime.datetime.now()
        self.root = root

    def _build_dot_source(self, mode: Literal["tree", "graph"]) -> str:
        """
        what: Builds a DOT language string for graph visualization.
        why: To generate a graph representation for Graphviz.
        how: Traverses the symbol graph and formats nodes/edges.
        when: Called by to_dot, a_to_svg, a_to_png.
        by (caller(s)): to_dot, a_to_svg, a_to_png.
        how often: When generating graph visualizations.
        how much: Depends on graph size.
        what is it like: Drawing a blueprint.
        how, what, why and when to improve: Optimize traversal for large graphs.
        """
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
        """
        what: Generates a DOT language string for the symbol graph.
        why: To provide a Graphviz-compatible representation.
        how: Calls _build_dot_source.
        when: When a DOT representation is needed.
        by (caller(s)): External tools, debugging.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Exporting a graph definition.
        how, what, why and when to improve: N/A.
        """
        if not _GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz is not installed. Please install it with `pip install 'symbol[visual]'`.")
        return self._build_dot_source(mode)

    async def a_to_svg(self, mode: Literal["tree", "graph"] = "tree") -> str:
        """
        what: Asynchronously renders the symbol graph to an SVG string.
        why: To provide a scalable vector graphic representation.
        how: Builds DOT source, pipes to Graphviz in a thread.
        when: When an SVG representation is needed.
        by (caller(s)): to_svg.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Asynchronously drawing a picture.
        how, what, why and when to improve: Optimize Graphviz call.
        """
        if not _GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz is not installed. Please install it with `pip install 'symbol[visual]'`.")
        dot = self._build_dot_source(mode)
        # Run in a thread pool to avoid blocking the event loop
        return await anyio.to_thread.run_sync(lambda: graphviz.Source(dot).pipe(format="svg").decode())

    def to_svg(self, mode: Literal["tree", "graph"] = "tree") -> str:
        """
        what: Renders the symbol graph to an SVG string.
        why: To provide a scalable vector graphic representation.
        how: Runs a_to_svg asynchronously.
        when: When an SVG representation is needed.
        by (caller(s)): External tools, debugging.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Synchronously getting an SVG.
        how, what, why and when to improve: N/A.
        """
        return anyio.run(self.a_to_svg, mode)

    async def a_to_png(self, mode: Literal["tree", "graph"] = "tree") -> bytes:
        """
        what: Asynchronously renders the symbol graph to PNG bytes.
        why: To provide a portable network graphic representation.
        how: Builds DOT source, pipes to Graphviz in a thread.
        when: When a PNG representation is needed.
        by (caller(s)): to_png.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Asynchronously drawing a picture.
        how, what, why and when to improve: Optimize Graphviz call.
        """
        if not _GRAPHVIZ_AVAILABLE:
            raise ImportError("Graphviz is not installed. Please install it with `pip install 'symbol[visual]'`.")
        dot = self._build_dot_source(mode)
        # Run in a thread pool to avoid blocking the event loop
        return await anyio.to_thread.run_sync(lambda: graphviz.Source(dot).pipe(format="png"))

    def to_png(self, mode: Literal["tree", "graph"] = "tree") -> bytes:
        """
        what: Renders the symbol graph to PNG bytes.
        why: To provide a portable network graphic representation.
        how: Runs a_to_png asynchronously.
        when: When a PNG representation is needed.
        by (caller(s)): External tools, debugging.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Synchronously getting a PNG.
        how, what, why and when to improve: N/A.
        """
        return anyio.run(self.a_to_png, mode)

    def to_mmd(self, mode: Literal["tree", "graph"] = "tree") -> str:
        """
        what: Generates a Mermaid diagram string for the symbol graph.
        why: To provide a Mermaid-compatible representation.
        how: Traverses the symbol graph and formats nodes/edges.
        when: When a Mermaid representation is needed.
        by (caller(s)): External tools, debugging.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Exporting a graph definition.
        how, what, why and when to improve: Optimize traversal for large graphs.
        """
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
        """
        what: Generates an ASCII art representation of the symbol graph.
        why: To provide a text-based visualization.
        how: Delegates to Symbol's to_ascii method.
        when: When an ASCII representation is needed.
        by (caller(s)): External tools, debugging.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Exporting a text graph.
        how, what, why and when to improve: Implement full graph ASCII renderer.
        """
        # This will be handled by the Symbol's own to_ascii method, or a dedicated GraphTraversal
        # For now, a placeholder or direct call to Symbol's method
        if mode == "tree":
            return self.root.to_ascii()
        else:
            # For generic graph, we might need a more sophisticated ASCII renderer
            # For simplicity, let's just use the tree representation for now
            return self.root.to_ascii()