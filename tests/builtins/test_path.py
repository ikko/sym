import pytest
from symbol import Symbol
from symbol.builtins.path import SymbolPathMixin

# Apply the mixin to Symbol for testing purposes
# In a real application, this would be handled by apply_builtins
Symbol.path_to = SymbolPathMixin.path_to
Symbol.match = SymbolPathMixin.match

@pytest.fixture
def simple_graph():
    # A -> B -> C
    # A -> D
    a = Symbol("A")
    b = Symbol("B")
    c = Symbol("C")
    d = Symbol("D")

    a.append(b)
    b.append(c)
    a.append(d)
    return a, b, c, d

@pytest.fixture
def disconnected_graph():
    # These symbols are not connected to each other, nor to simple_graph
    x = Symbol("X_disconnected")
    y = Symbol("Y_disconnected")
    z = Symbol("Z_disconnected")
    return x, y, z

@pytest.fixture
def cyclic_graph():
    # A -> B -> C -> A (cycle)
    a = Symbol("A_cycle")
    b = Symbol("B_cycle")
    c = Symbol("C_cycle")

    a.append(b)
    b.append(c)
    c.append(a)
    return a, b, c

def test_path_to_direct_path(simple_graph):
    a, b, c, d = simple_graph
    path = a.path_to(c)
    assert path == [a, b, c]

def test_path_to_no_path(simple_graph, disconnected_graph):
    a, b, c, d = simple_graph
    _, _, z = disconnected_graph # z is not connected to a
    path = a.path_to(z)
    assert path == []

def test_path_to_self(simple_graph):
    a, _, _, _ = simple_graph
    path = a.path_to(a)
    assert path == [a]

def test_path_to_with_cycle(cyclic_graph):
    a, b, c = cyclic_graph
    # Path from A to C should still be found, DFS handles visited nodes
    path = a.path_to(c)
    assert path == [a, b, c]

def test_match_dfs(simple_graph):
    a, b, c, d = simple_graph
    # Predicate: name starts with 'B' or 'C'
    predicate = lambda sym: sym.name.startswith("B") or sym.name.startswith("C")
    matched_symbols = list(a.match(predicate, traversal='dfs'))
    # DFS order: A, B, C, D. Matches: B, C
    assert matched_symbols == [b, c]

def test_match_bfs(simple_graph):
    a, b, c, d = simple_graph
    # Predicate: name starts with 'B' or 'D'
    predicate = lambda sym: sym.name.startswith("B") or sym.name.startswith("D")
    matched_symbols = list(a.match(predicate, traversal='bfs'))
    # BFS order: A, B, D, C. Matches: B, D
    assert matched_symbols == [b, d]

def test_match_no_match(simple_graph):
    a, _, _, _ = simple_graph
    predicate = lambda sym: sym.name == "Z"
    matched_symbols = list(a.match(predicate))
    assert matched_symbols == []

def test_match_all_match(simple_graph):
    a, b, c, d = simple_graph
    predicate = lambda sym: True
    matched_symbols = list(a.match(predicate, traversal='dfs'))
    assert set(matched_symbols) == {a, b, c, d}
