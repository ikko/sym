import pytest
from symbol.core.symbol import Symbol, s

def test_symbol_creation_and_interning():
    # Test basic Symbol creation
    s1 = Symbol("test_symbol")
    assert isinstance(s1, Symbol)
    assert s1.name == "test_symbol"

    # Test interning: creating a Symbol with the same name should return the same instance
    s2 = Symbol("test_symbol")
    assert s1 is s2

    # Test case sensitivity
    s3 = Symbol("Test_Symbol")
    assert s1 is not s3
    assert s3.name == "Test_Symbol"

    # Test Symbol with different types of names (e.g., numbers, special characters)
    s4 = Symbol("123")
    assert s4.name == "123"
    s5 = Symbol("symbol-with_dashes")
    assert s5.name == "symbol-with_dashes"
    s6 = Symbol("another symbol")
    assert s6.name == "another symbol"

def test_symbol_equality_and_hashing():
    s1 = Symbol("apple")
    s2 = Symbol("apple")
    s3 = Symbol("banana")

    # Test equality
    assert s1 == s2
    assert s1 != s3

    # Test hashing
    assert hash(s1) == hash(s2)
    assert hash(s1) != hash(s3)

    # Test with different types
    assert s1 != "apple"
    assert s1 != 123

def test_symbol_string_representation():
    s = Symbol("test_repr")
    assert str(s) == "test_repr"
    assert repr(s) == "Symbol('test_repr')"

def test_symbol_basic_graph_operations():
    parent = Symbol("parent")
    child1 = Symbol("child1")
    child2 = Symbol("child2")
    grandchild = Symbol("grandchild")

    # Test append
    parent.append(child1)
    assert child1 in parent.children
    assert parent in child1.parents
    assert len(parent.children) == 1
    assert len(child1.parents) == 1

    # Test adding an existing child (should not duplicate)
    parent.append(child1)
    assert len(parent.children) == 1
    assert len(child1.parents) == 1

    # Test add (should behave like append for new children)
    parent.add(child2)
    assert child2 in parent.children
    assert parent in child2.parents
    assert len(parent.children) == 2
    assert len(child2.parents) == 1

    # Test add for existing child (should not duplicate)
    parent.add(child2)
    assert len(parent.children) == 2
    assert len(child2.parents) == 1

    # Test chaining appends
    parent.append(grandchild).append(child1) # child1 is already there, should not add again
    assert grandchild in parent.children
    assert parent in grandchild.parents
    assert len(parent.children) == 3 # child1, child2, grandchild

    # Test children and parents properties
    assert set(parent.children) == {child1, child2, grandchild}
    assert set(child1.parents) == {parent}
    assert set(child2.parents) == {parent}
    assert set(grandchild.parents) == {parent}

    # Test adding a child that is already a parent of another symbol
    another_parent = Symbol("another_parent")
    another_child = Symbol("another_child")
    another_parent.append(another_child)
    child1.append(another_parent) # child1 becomes parent of another_parent
    assert another_parent in child1.children
    assert child1 in another_parent.parents
    assert len(child1.children) == 1
    assert len(another_parent.parents) == 1 # child1 is the only parent

def test_symbol_namespace():
    # Test creation via attribute access
    sym_attr = s.my_attribute_symbol
    assert isinstance(sym_attr, Symbol)
    assert sym_attr.name == "my_attribute_symbol"

    # Test creation via item access
    sym_item = s["my_item_symbol"]
    assert isinstance(sym_item, Symbol)
    assert sym_item.name == "my_item_symbol"

    # Test interning through namespace
    sym_attr_2 = s.my_attribute_symbol
    assert sym_attr is sym_attr_2

    sym_item_2 = s["my_item_symbol"]
    assert sym_item is sym_item_2

    # Test that SymbolNamespace is read-only
    with pytest.raises(TypeError):
        s.new_symbol = "value"
    with pytest.raises(TypeError):
        s["another_new_symbol"] = "value"
