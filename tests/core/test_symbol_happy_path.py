import pytest
from symbol import Symbol
from symbol.core.symbol import SymbolNamespace



def test_symbol_creation_and_interning():
    # Test basic creation
    s1 = Symbol("test_symbol_1")
    assert isinstance(s1, Symbol)
    assert s1.name == "test_symbol_1"

    # Test interning (same name should return the same instance)
    s2 = Symbol("test_symbol_1")
    assert s1 is s2

    s3 = Symbol("test_symbol_2")
    assert s1 is not s3
    assert s3.name == "test_symbol_2"

def test_symbol_equality_and_hashing():
    s1 = Symbol("equal_symbol")
    s2 = Symbol("equal_symbol")
    s3 = Symbol("another_symbol")

    # Test equality
    assert s1 == s2
    assert not (s1 == s3)

    # Test hashing
    assert hash(s1) == hash(s2)
    assert hash(s1) != hash(s3)

def test_symbol_string_representation():
    s = Symbol("repr_symbol")
    assert str(s) == "repr_symbol"
    assert repr(s) == f"Symbol('{s.name}')"

def test_symbol_basic_graph_operations():
    parent = Symbol("parent")
    child1 = Symbol("child1")
    child2 = Symbol("child2")

    # Test append
    parent.append(child1)
    assert child1 in parent.children
    assert parent in child1.parents

    # Test add (should not add duplicate)
    parent.add(child1)
    assert len(parent.children) == 1

    parent.add(child2)
    assert child2 in parent.children
    assert parent in child2.parents
    assert len(parent.children) == 2

def test_symbol_namespace():
    # Test attribute access
    sym_attr = SymbolNamespace().my_attribute_symbol
    assert isinstance(sym_attr, Symbol)
    assert sym_attr.name == "my_attribute_symbol"

    # Test item access
    sym_item = SymbolNamespace()["my_item_symbol"]
    assert isinstance(sym_item, Symbol)
    assert sym_item.name == "my_item_symbol"

    # Test that attribute and item access for the same name return the same instance
    sym_attr_2 = SymbolNamespace().shared_symbol
    sym_item_2 = SymbolNamespace()["shared_symbol"]
    assert sym_attr_2 is sym_item_2
