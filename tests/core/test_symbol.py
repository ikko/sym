import pytest
from symbol.core.symbol import Symbol, GraphTraversal, s, to_sym
from symbol.core.base_symbol import Symbol as BaseSymbol
from symbol.core.lazy import SENTINEL
from symbol.builtins.avl_tree import AVLTree
from weakref import WeakValueDictionary
import threading
import datetime

# Re-use the setup_and_teardown fixture from test_base_symbol.py
# This ensures a clean state for Symbol class-level attributes before each test
@pytest.fixture(autouse=True)
def setup_and_teardown_symbol_class():
    # Store original class-level attributes
    original_pool = BaseSymbol._pool
    original_numbered = BaseSymbol._numbered
    original_auto_counter = BaseSymbol._auto_counter
    original_read_cursor = BaseSymbol._read_cursor
    original_write_cursor = BaseSymbol._write_cursor
    original_lock = BaseSymbol._lock

    # Clear for predictable testing
    BaseSymbol._pool = WeakValueDictionary()
    BaseSymbol._numbered = AVLTree()
    BaseSymbol._auto_counter = 0
    BaseSymbol._read_cursor = 0.0
    BaseSymbol._write_cursor = 0.0
    BaseSymbol._lock = threading.RLock()

    yield

    # Restore original class-level attributes after each test
    BaseSymbol._pool = original_pool
    BaseSymbol._numbered = original_numbered
    BaseSymbol._auto_counter = original_auto_counter
    BaseSymbol._read_cursor = original_read_cursor
    BaseSymbol._write_cursor = original_write_cursor
    BaseSymbol._lock = original_lock

    # Clear any remaining symbols from the pool and numbered tree to ensure complete isolation
    BaseSymbol._pool.clear()
    BaseSymbol._numbered = AVLTree() # Reinitialize to ensure it's empty
    BaseSymbol._auto_counter = 0
    BaseSymbol._read_cursor = 0.0
    BaseSymbol._write_cursor = 0.0


def test_symbol_index_property():
    sym = Symbol("test_index")
    assert sym._index is SENTINEL
    index_obj = sym.index
    assert index_obj is not SENTINEL
    assert sym._index is index_obj
    # Ensure it's a SymbolIndex instance (or its mock if mocked)
    assert hasattr(index_obj, 'insert') # Basic check for SymbolIndex methods

def test_symbol_metadata_property():
    sym = Symbol("test_metadata")
    assert sym._metadata is SENTINEL
    metadata_obj = sym.metadata
    assert metadata_obj is not SENTINEL
    assert sym._metadata is metadata_obj
    # Ensure it's a DefDict instance (or its mock if mocked)
    assert hasattr(metadata_obj, '__setitem__') # Basic check for DefDict methods

def test_symbol_context_property():
    sym = Symbol("test_context")
    assert sym._context is SENTINEL
    context_obj = sym.context
    assert context_obj is not SENTINEL
    assert sym._context is context_obj
    # Ensure it's a DefDict instance (or its mock if mocked)
    assert hasattr(context_obj, '__setitem__') # Basic check for DefDict methods

def test_symbol_elevated_attributes_set_and_get():
    sym = Symbol("test_elevated_attrs")
    sym.dynamic_attr = "value1"
    assert sym.dynamic_attr == "value1"
    assert sym._elevated_attributes["dynamic_attr"] == "value1"

def test_symbol_elevated_attributes_overwrite_existing():
    sym = Symbol("test_elevated_attrs_overwrite")
    sym.dynamic_attr = "original_value"
    sym.dynamic_attr = "new_value"
    assert sym.dynamic_attr == "new_value"
    assert sym._elevated_attributes["dynamic_attr"] == "new_value"

def test_symbol_elevated_attributes_delete():
    sym = Symbol("test_elevated_attrs_delete")
    sym.temp_attr = "to_delete"
    assert sym.temp_attr == "to_delete"
    del sym.temp_attr
    with pytest.raises(AttributeError):
        _ = sym.temp_attr
    assert "temp_attr" not in sym._elevated_attributes

def test_symbol_elevated_attributes_delete_non_existent():
    sym = Symbol("test_elevated_attrs_delete_non_existent")
    with pytest.raises(AttributeError):
        del sym.non_existent_attr

def test_symbol_append_child():
    parent = Symbol("parent")
    child = Symbol("child")
    parent.append(child)
    assert child in parent.children
    assert parent in child.parents

def test_symbol_append_lazy_symbol_child():
    from symbol.core.lazy_symbol import LazySymbol
    parent = Symbol("parent_lazy")
    lazy_child = LazySymbol("lazy_child_name")
    parent.append(lazy_child)
    assert lazy_child in parent.children
    assert parent in lazy_child.parents

def test_symbol_append_non_symbol_object():
    parent = Symbol("parent_non_symbol")
    non_symbol_obj = "string_child"
    child_sym = parent.append(non_symbol_obj)
    assert isinstance(child_sym, Symbol)
    assert child_sym.name == "string_child"
    assert child_sym in parent.children
    assert parent in child_sym.parents

def test_symbol_append_duplicate_child():
    parent = Symbol("parent_duplicate")
    child = Symbol("child_duplicate")
    parent.append(child)
    initial_children_len = len(parent.children)
    parent.append(child) # Appending again should not add duplicate
    assert len(parent.children) == initial_children_len

def test_symbol_add_child():
    parent = Symbol("parent_add")
    child = Symbol("child_add")
    parent.add(child)
    assert child in parent.children
    assert parent in child.parents

def test_symbol_add_duplicate_child():
    parent = Symbol("parent_add_duplicate")
    child = Symbol("child_add_duplicate")
    parent.add(child)
    initial_children_len = len(parent.children)
    parent.add(child) # Adding again should not add duplicate
    assert len(parent.children) == initial_children_len

def test_symbol_relate_unrelate():
    s1 = Symbol("s1_relate")
    s2 = Symbol("s2_relate")

    s1.relate(s2, how="friend")
    assert s2 in s1.related_to
    assert "friend" in s1.related_how
    assert s1 in s2.related_to
    assert "_inverse_friend" in s2.related_how

    s1.unrelate(s2)
    assert s2 not in s1.related_to
    assert s1 not in s2.related_to

def test_symbol_relate_with_specific_how():
    s1 = Symbol("s1_how")
    s2 = Symbol("s2_how")
    s1.relate(s2, how="parent_of")
    assert s1.related_how[s1.related_to.index(s2)] == "parent_of"
    assert s2.related_how[s2.related_to.index(s1)] == "_inverse_parent_of"

def test_symbol_unrelate_with_specific_how():
    s1 = Symbol("s1_unrelate_how")
    s2 = Symbol("s2_unrelate_how")
    s1.relate(s2, how="knows")
    s1.relate(s2, how="likes") # Add another relationship

    s1.unrelate(s2, how="knows")
    assert s2 in s1.related_to
    assert "likes" in s1.related_how
    assert "knows" not in s1.related_how

    # Ensure inverse is also removed correctly
    assert s1 in s2.related_to
    assert "_inverse_likes" in s2.related_how
    assert "_inverse_knows" not in s2.related_how


