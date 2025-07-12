import pytest
import anyio
from symb import Symbol
from symb.builtins.visual import SymbolRender

# Apply the mixin to Symbol for testing purposes
# In a real application, this would be handled by apply_builtins
Symbol.to_mmd = SymbolRender(Symbol("dummy")).to_mmd # Assign a dummy instance for method access
Symbol.from_mmd = SymbolRender.from_mmd # Assign the class method

@pytest.fixture
def simple_symb_tree():
    Symbol._pool.clear() # Clear pool before creating new symbols
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

def test_to_mmd_simple_tree(simple_symb_tree):
    a, b, c, d = simple_symb_tree
    
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

def test_from_mmd_simple_tree(simple_symb_tree):
    a_orig, b_orig, c_orig, d_orig = simple_symb_tree
    mermaid_output = SymbolRender(a_orig).to_mmd(mode="tree")
    
    # Import the Mermaid string back into a Symbol graph
    a_reconstructed = SymbolRender.from_mmd(mermaid_output)

    # Assert that the reconstructed graph matches the original
    # This is a simplified check, a more robust one would involve recursive traversal
    assert a_reconstructed.name == a_orig.name
    assert len(a_reconstructed.children) == len(a_orig.children)
    assert sorted([s.name for s in a_reconstructed.children]) == sorted([s.name for s in a_orig.children])

    # Check a child's children
    b_reconstructed = next((s for s in a_reconstructed.children if s.name == b_orig.name), None)
    assert b_reconstructed is not None
    assert len(b_reconstructed.children) == len(b_orig.children)
    assert sorted([s.name for s in b_reconstructed.children]) == sorted([s.name for s in b_orig.children])

def test_to_mmd_simple_graph():
    Symbol._pool.clear() # Clear pool before creating new symbols
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

def test_from_mmd_simple_graph():
    Symbol._pool.clear() # Clear pool before creating original symbols
    a_orig = Symbol("A_graph")
    b_orig = Symbol("B_graph")
    c_orig = Symbol("C_graph")
    d_orig = Symbol("D_graph")

    a_orig.append(b_orig)
    b_orig.append(c_orig)
    c_orig.append(d_orig)
    d_orig.append(a_orig)

    mermaid_output = SymbolRender(a_orig).to_mmd(mode="graph")
    
    Symbol._pool.clear() # Clear pool again before reconstruction to isolate symbols
    a_reconstructed_root = SymbolRender.from_mmd(mermaid_output) # This will populate Symbol._pool

    # Now, retrieve all reconstructed symbols from the pool
    reconstructed_symbols = Symbol._pool

    # Verify each original symbol's children against its reconstructed counterpart
    original_symbols = {"A_graph": a_orig, "B_graph": b_orig, "C_graph": c_orig, "D_graph": d_orig}

    for name_in_mermaid_id, orig_sym in original_symbols.items():
        # The reconstructed symbol will have the name with spaces, not underscores
        reconstructed_sym_name = name_in_mermaid_id.replace('_', ' ')
        reconstructed_sym = reconstructed_symbols.get(reconstructed_sym_name)
        assert reconstructed_sym is not None, f"Reconstructed symbol {reconstructed_sym_name} not found in pool."

        # Check children
        # The children of orig_sym will have names like "B_graph", "C_graph"
        # The children of reconstructed_sym will have names like "B graph", "C graph"
        # So we need to compare the "cleaned" names of original children with reconstructed children
        orig_children_names_cleaned = sorted([s.name.replace('_', ' ') for s in orig_sym.children])
        reconstructed_children_names = sorted([s.name for s in reconstructed_sym.children])
        
        assert reconstructed_children_names == orig_children_names_cleaned, \
            f"Mismatch in children names for {reconstructed_sym_name}: Expected {orig_children_names_cleaned}, got {reconstructed_children_names}"



@pytest.mark.skip(reason="Graphviz 'dot' executable not found. Please install Graphviz and add it to your system's PATH.")
@pytest.mark.anyio
async def test_a_to_svg_simple_tree(simple_symb_tree):
    a, _, _, _ = simple_symb_tree
    try:
        svg_output = await SymbolRender(a).a_to_svg(mode="tree")
        assert "<svg" in svg_output
        assert "A" in svg_output
        assert "B" in svg_output
        assert "C" in svg_output
        assert "D" in svg_output
    except ImportError as e:
        pytest.skip(f"Graphviz not installed: {repr(e)}")



