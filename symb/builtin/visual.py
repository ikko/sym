"""This module provides visualization capabilities for Symbol objects.

It allows for rendering Symbol graphs to various formats, such as DOT, SVG, PNG, and Mermaid.
"""
from __future__ import annotations
from typing import Literal
import anyio

try:
    import graphviz
    _GRAPHVIZ_AVAILABLE = True
except ImportError:
    _GRAPHVIZ_AVAILABLE = False

from core.protocols import SymbolVisualProtocol


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

    @classmethod
    def from_mmd(cls, mmd_string: str) -> 'Symbol':
        from core.symb import Symbol # Import here to avoid circular dependency

        lines = mmd_string.strip().split('\n')
        if not lines:
            raise ValueError("Empty Mermaid string provided.")

        header = lines[0].strip()
        if header not in ["graph TD", "graph LR"]:
            raise ValueError(f"Unsupported Mermaid graph type: {header}. Only 'graph TD' and 'graph LR' are supported.")

        symbols = {} # Map Mermaid ID to Symbol object
        
        def get_or_create_symbol(mermaid_id: str) -> Symbol:
            if mermaid_id in symbols:
                return symbols[mermaid_id]

            # Clean the Mermaid ID to get the actual Symbol name
            clean_name = mermaid_id.replace('_', ' ')
            # Handle node declarations like 'node_id(Node Name)'
            if '(' in clean_name and clean_name.endswith(')'):
                last_paren_idx = clean_name.rfind('(')
                display_name = clean_name[last_paren_idx + 1 : -1]
                if display_name:
                    clean_name = display_name
                else:
                    clean_name = clean_name[:last_paren_idx].strip()

            # Create the Symbol with the cleaned name
            new_sym = Symbol(clean_name)
            symbols[mermaid_id] = new_sym # Store using Mermaid ID
            return new_sym

        # Process relationships
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            # Handle 'A --> B' and 'A -- text --> B'
            if '-->' in line:
                parts = line.split('-->')
                source_part = parts[0].strip()
                target_part = parts[1].strip()

                # Check for text in relationship: 'A -- text --> B'
                if '--' in source_part and source_part.count('--') == 1:
                    sub_parts = source_part.split('--')
                    source_name = sub_parts[0].strip()
                    relation_text = sub_parts[1].strip()
                    
                    source_sym = get_or_create_symbol(source_name)
                    target_sym = get_or_create_symbol(target_part)
                    source_sym.relate(target_sym, how=relation_text)
                else:
                    source_sym = get_or_create_symbol(source_part)
                    target_sym = get_or_create_symbol(target_part)
                    source_sym.append(target_sym)
            # Handle node declarations like 'node_id(Node Name)'
            elif '(' in line and line.endswith(')'):
                get_or_create_symbol(line)
            else:
                # Just a node name, ensure it's created
                get_or_create_symbol(line)

        # Determine root symbols (those with no parents among the parsed symbols)
        all_symbols = set(symbols.values())
        child_symbols = set()
        for sym in all_symbols:
            for child in sym.children:
                if child in all_symbols: # Only consider children that were part of this graph
                    child_symbols.add(child)
            # Also consider symbols related via 'relate' as children for root determination
            for how, related_syms in sym.relations.items():
                if not how.startswith('_inverse_'):
                    for related_sym in related_syms:
                        if related_sym in all_symbols:
                            child_symbols.add(related_sym)

        root_symbols = [sym for sym in all_symbols if sym not in child_symbols]

        if not root_symbols:
            # If no clear root (e.g., a circular graph or single node), return any symbol
            if all_symbols:
                return next(iter(all_symbols))
            else:
                raise ValueError("No symbols found in the Mermaid string.")
        
        # For simplicity, return the first root. In a more complex scenario,
        # we might want to return a list of roots or a composite symbol.
        return root_symbols[0]

    def to_ascii(self, mode: Literal["tree", "graph"] = "tree") -> str:
        # This will be handled by the Symbol's own to_ascii method, or a dedicated GraphTraversal
        # For now, a placeholder or direct call to Symbol's method
        if mode == "tree":
            return self.root.to_ascii()
        else:
            # For generic graph, we might need a more sophisticated ASCII renderer
            # For simplicity, let's just use the tree representation for now
            return self.root.to_ascii()
