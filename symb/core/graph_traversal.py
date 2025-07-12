from typing import Literal


class GraphTraversal:
    def __init__(self, root: 'Symbol',
                 traverse_mode: Literal["dfs", "bfs"] = "dfs",
                 family_mode: Literal["children_first", "parents_first"] = "children_first",
                 graph_mode: Literal["dfs", "bfs"] = "dfs"):
        self.root = root
        self.traverse_mode = traverse_mode
        self.family_mode = family_mode
        self.graph_mode = graph_mode
        self.visited = set()
        self.result = []

    def traverse(self):
        from collections import deque

        if self.traverse_mode == "dfs":
            collection = [self.root]  # Use as a stack
            pop_method = collection.pop
            append_method = collection.append
        elif self.traverse_mode == "bfs":
            collection = deque([self.root])  # Use as a queue
            pop_method = collection.popleft
            append_method = collection.append
        else:
            raise ValueError(f"Unknown traverse_mode: {self.traverse_mode}")

        while collection:
            symb = pop_method()
            if symb in self.visited:
                continue
            self.visited.add(symb)
            self.result.append(symb)

            neighbors = []

            # Family relationships
            if self.family_mode == "children_first":
                neighbors.extend(symb.children)
                # Add parents if they haven't been visited yet and are not the root
                for parent in symb.parents:
                    if parent not in self.visited and parent != self.root:
                        neighbors.append(parent)
            elif self.family_mode == "parents_first":
                # Add parents first
                for parent in symb.parents:
                    if parent not in self.visited and parent != self.root:
                        neighbors.append(parent)
                neighbors.extend(symb.children)
            else:
                raise ValueError(f"Unknown family_mode: {self.family_mode}")

            # General relations
            for how, related_syms in symb.relations.items():
                if not how.startswith('_inverse_'):
                    for related_sym in related_syms:
                        if related_sym not in self.visited:
                            neighbors.append(related_sym)

            # Sort neighbors for consistent traversal order (important for testing)
            # Prioritize unvisited nodes
            unvisited_neighbors = sorted([n for n in neighbors if n not in self.visited], key=lambda s: s.name)

            # For DFS, we append in reverse order to process in sorted order
            if self.traverse_mode == "dfs":
                for neighbor in reversed(unvisited_neighbors):
                    append_method(neighbor)
            else: # BFS
                for neighbor in unvisited_neighbors:
                    append_method(neighbor)
        return self.result

    def to_ascii(self) -> str:
        lines = []
        visited_ascii = set()
        from collections import deque

        # Collect all symbols and their relations first
        all_symbols_in_traversal_order = self.traverse()

        # First pass: print symbols with indentation
        # We need to re-traverse to get indentation correct, or store it during traverse()
        # For simplicity, let's re-implement a basic DFS/BFS for printing with indentation
        # that respects the overall traversal order determined by self.traverse()

        # To get correct indentation, we need to know the parent-child relationships
        # from the traversal path. This is tricky with a flat list from self.traverse().
        # Let's modify to_ascii to do its own traversal for printing, but still respect
        # the traversal modes.

        if self.traverse_mode == "dfs":
            collection = [(self.root, 0)]  # (symbol, depth)
            pop_method = collection.pop
            append_method = lambda item: collection.append(item)
        elif self.traverse_mode == "bfs":
            collection = deque([(self.root, 0)])
            pop_method = collection.popleft
            append_method = lambda item: collection.append(item)
        else:
            raise ValueError(f"Unknown traverse_mode: {self.traverse_mode}")

        printed_symbols = set()
        relations_to_print = set() # Store (source, relation_type, target)

        while collection:
            symb, depth = pop_method()

            if symb in printed_symbols:
                continue
            printed_symbols.add(symb)

            lines.append(f"{"  " * depth}- {symb.name}")

            neighbors_to_process = []

            # Family relationships
            if self.family_mode == "children_first":
                for child in symb.children:
                    neighbors_to_process.append((child, depth + 1))
                for parent in symb.parents:
                    # Only add parents if they are part of the current traversal path and not already printed
                    if parent != self.root and parent not in printed_symbols:
                        neighbors_to_process.append((parent, depth + 1))
            elif self.family_mode == "parents_first":
                for parent in symb.parents:
                    if parent != self.root and parent not in printed_symbols:
                        neighbors_to_process.append((parent, depth + 1))
                for child in symb.children:
                    neighbors_to_process.append((child, depth + 1))
            else:
                raise ValueError(f"Unknown family_mode: {self.family_mode}")

            # General relations - collect for later printing
            for how, related_syms in symb.relations.items():
                if not how.startswith('_inverse_'):
                    for related_sym in related_syms:
                        relations_to_print.add((symb.name, how, related_sym.name))

            sorted_neighbors = sorted(neighbors_to_process, key=lambda x: x[0].name)

            if self.traverse_mode == "dfs":
                for neighbor_info in reversed(sorted_neighbors):
                    append_method(neighbor_info)
            else:
                for neighbor_info in sorted_neighbors:
                    append_method(neighbor_info)

        # Second pass: print relations
        if relations_to_print:
            lines.append("") # Add a blank line for separation
            lines.append("--- Relations ---")
            for source, how, target in sorted(list(relations_to_print)):
                lines.append(f"{source} --{how}--> {target}")

        return "\n".join(lines)
