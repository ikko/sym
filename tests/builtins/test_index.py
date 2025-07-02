import pytest
from symbol.core.symbol import Symbol
from symbol.builtins.index import SymbolIndex, IndexNode

@pytest.fixture
def owner_symbol():
    return Symbol("owner_index")

@pytest.fixture
def empty_symbol_index(owner_symbol):
    return SymbolIndex(owner_symbol)

def test_symbol_index_instantiation(owner_symbol):
    index = SymbolIndex(owner_symbol)
    assert index.owner == owner_symbol
    assert index.root is None
    assert index._function_map == {}

def test_symbol_index_insertion(empty_symbol_index):
    s1 = Symbol("sym1")
    s2 = Symbol("sym2")
    s3 = Symbol("sym3")

    empty_symbol_index.insert(s2, 50) # Root
    assert empty_symbol_index.root is not None
    assert empty_symbol_index.root.symbol == s2
    assert empty_symbol_index._function_map["sym2"].symbol == s2

    empty_symbol_index.insert(s1, 25) # Left child
    assert empty_symbol_index.root.left.symbol == s1
    assert empty_symbol_index._function_map["sym1"].symbol == s1

    empty_symbol_index.insert(s3, 75) # Right child
    assert empty_symbol_index.root.right.symbol == s3
    assert empty_symbol_index._function_map["sym3"].symbol == s3

    # Test inserting with callable weight
    s4 = Symbol("sym4")
    def dynamic_weight(sym):
        return len(sym.name) * 2
    empty_symbol_index.insert(s4, dynamic_weight)
    assert empty_symbol_index._function_map["sym4"].weight == dynamic_weight
    assert empty_symbol_index._function_map["sym4"].eval_weight() == 8

def test_symbol_index_traverse_inorder(empty_symbol_index):
    s_nodes = [
        (Symbol("sym_d"), 40),
        (Symbol("sym_b"), 20),
        (Symbol("sym_f"), 60),
        (Symbol("sym_a"), 10),
        (Symbol("sym_c"), 30),
        (Symbol("sym_e"), 50),
        (Symbol("sym_g"), 70),
    ]
    # Insert in an order that creates a balanced-ish tree for predictable traversal
    # Root: sym_d (40)
    # Left: sym_b (20) -> Left: sym_a (10), Right: sym_c (30)
    # Right: sym_f (60) -> Left: sym_e (50), Right: sym_g (70)
    insert_order = [s_nodes[0], s_nodes[1], s_nodes[2], s_nodes[3], s_nodes[4], s_nodes[5], s_nodes[6]]
    for sym, weight in insert_order:
        empty_symbol_index.insert(sym, weight)

    expected_inorder = [
        Symbol("sym_a"), Symbol("sym_b"), Symbol("sym_c"), Symbol("sym_d"),
        Symbol("sym_e"), Symbol("sym_f"), Symbol("sym_g")
    ]
    actual_inorder = empty_symbol_index.traverse(order="in")
    assert actual_inorder == expected_inorder

def test_symbol_index_traverse_preorder(empty_symbol_index):
    s_nodes = [
        (Symbol("sym_d"), 40),
        (Symbol("sym_b"), 20),
        (Symbol("sym_f"), 60),
        (Symbol("sym_a"), 10),
        (Symbol("sym_c"), 30),
        (Symbol("sym_e"), 50),
        (Symbol("sym_g"), 70),
    ]
    insert_order = [s_nodes[0], s_nodes[1], s_nodes[2], s_nodes[3], s_nodes[4], s_nodes[5], s_nodes[6]]
    for sym, weight in insert_order:
        empty_symbol_index.insert(sym, weight)

    expected_preorder = [
        Symbol("sym_d"), Symbol("sym_b"), Symbol("sym_a"), Symbol("sym_c"),
        Symbol("sym_f"), Symbol("sym_e"), Symbol("sym_g")
    ]
    actual_preorder = empty_symbol_index.traverse(order="pre")
    assert actual_preorder == expected_preorder

def test_symbol_index_traverse_postorder(empty_symbol_index):
    s_nodes = [
        (Symbol("sym_d"), 40),
        (Symbol("sym_b"), 20),
        (Symbol("sym_f"), 60),
        (Symbol("sym_a"), 10),
        (Symbol("sym_c"), 30),
        (Symbol("sym_e"), 50),
        (Symbol("sym_g"), 70),
    ]
    insert_order = [s_nodes[0], s_nodes[1], s_nodes[2], s_nodes[3], s_nodes[4], s_nodes[5], s_nodes[6]]
    for sym, weight in insert_order:
        empty_symbol_index.insert(sym, weight)

    expected_postorder = [
        Symbol("sym_a"), Symbol("sym_c"), Symbol("sym_b"), Symbol("sym_e"),
        Symbol("sym_g"), Symbol("sym_f"), Symbol("sym_d")
    ]
    actual_postorder = empty_symbol_index.traverse(order="post")
    assert actual_postorder == expected_postorder

def test_symbol_index_map_and_filter(empty_symbol_index):
    s_nodes = [
        (Symbol("apple"), 10),
        (Symbol("banana"), 20),
        (Symbol("cherry"), 30),
    ]
    for sym, weight in s_nodes:
        empty_symbol_index.insert(sym, weight)

    # Test map
    mapped_names = empty_symbol_index.map(lambda s: s.name.upper())
    assert mapped_names == ["APPLE", "BANANA", "CHERRY"]

    # Test filter
    filtered_symbols = empty_symbol_index.filter(lambda s: "a" in s.name)
    assert filtered_symbols == [Symbol("apple"), Symbol("banana")]

def test_symbol_index_ascii_representation(empty_symbol_index):
    s_nodes = [
        (Symbol("root"), 50),
        (Symbol("left"), 25),
        (Symbol("right"), 75),
    ]
    for sym, weight in s_nodes:
        empty_symbol_index.insert(sym, weight)

    expected_ascii = """    - right
- root
    - left"""
    assert empty_symbol_index.ascii() == expected_ascii
    assert empty_symbol_index.to_ascii() == expected_ascii
