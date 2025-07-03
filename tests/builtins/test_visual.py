import pytest
from symbol.core.symbol import Symbol
from symbol.builtins.visual import SymbolRender

# Apply the mixin to Symbol for testing purposes
# In a real application, this would be handled by apply_builtins
Symbol.to_mmd = SymbolRender(Symbol("dummy")).to_mmd # Assign a dummy instance for method access

@pytest.fixture
def simple_symbol_tree():
    # A
    # |\
    # B C
    # |
    # D
    a = Symbol("A")
    b = Symbol("B")
    c = Symbol("C")
    d = Symbol("D")

    a.append(b)
    a.append(c)
    b.append(d)
    print(f"A children: {[c.name for c in a.children]}") # Debug print
    print(f"B children: {[c.name for c in b.children]}") # Debug print
    return a, b, c, d

def test_to_mmd_simple_tree(simple_symbol_tree):
    a, b, c, d = simple_symbol_tree
    
    # When to_mmd is called on the root Symbol
    mermaid_output = SymbolRender(a).to_mmd(mode="tree")

    # Then a valid Mermaid diagram string representing the tree should be returned
    expected_output = (
        "graph TD\n"
        "A --> B\n"
        "A --> C\n"
        "B --> D"
    )
    assert mermaid_output == expected_output

def test_to_mmd_simple_graph():
    # A --> B
    # ^   |
    # |   v
    # D <-- C
    a = Symbol("A_graph")
    b = Symbol("B_graph")
    c = Symbol("C_graph")
    d = Symbol("D_graph")

    a.append(b)
    b.append(c)
    c.append(d)
    d.append(a)

    mermaid_output = SymbolRender(a).to_mmd(mode="graph")

    # Mermaid graph mode uses LR by default, and does not deduplicate edges in output
    # The order of edges might vary based on traversal, so we check for presence
    expected_lines = [
        "graph LR",
        "A_graph --> B_graph",
        "B_graph --> C_graph",
        "C_graph --> D_graph",
        "D_graph --> A_graph"
    ]
    
    actual_lines = mermaid_output.splitlines()
    assert len(actual_lines) == len(expected_lines)
    for line in expected_lines:
        assert line in actual_lines

