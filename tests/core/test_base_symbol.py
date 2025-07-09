import pytest
import threading
from weakref import WeakValueDictionary
from symb.core.base_symb import Symbol, _to_symb, AVLTree

@pytest.fixture(autouse=True)
def setup_and_teardown_base_symb():
    # Store original class-level attributes
    original_pool = Symbol._pool
    original_numbered = Symbol._numbered
    original_auto_counter = Symbol._auto_counter
    original_read_cursor = Symbol._read_cursor
    original_write_cursor = Symbol._write_cursor
    original_lock = Symbol._lock

    # Clear for predictable testing
    Symbol._pool = WeakValueDictionary()
    Symbol._numbered = AVLTree()
    Symbol._auto_counter = 0
    Symbol._read_cursor = 0.0
    Symbol._write_cursor = 0.0
    Symbol._lock = threading.RLock()

    yield

    # Restore original class-level attributes after each test
    Symbol._pool = original_pool
    Symbol._numbered = original_numbered
    Symbol._auto_counter = original_auto_counter
    Symbol._read_cursor = original_read_cursor
    Symbol._write_cursor = original_write_cursor
    Symbol._lock = original_lock

def test_symb_creation_and_interning():
    s1 = Symbol("test_symb")
    s2 = Symbol("test_symb")
    s3 = Symbol("another_symb")

    assert s1 is s2
    assert s1 is not s3
    assert s1.name == "test_symb"
    assert s3.name == "another_symb"
    assert s1.origin is None
    assert s3.origin is None

def test_symb_creation_with_origin():
    obj = {"data": 123}
    s = Symbol("test_origin", origin=obj)
    assert s.name == "test_origin"
    assert s.origin is obj

def test_symb_type_error_for_non_string_name():
    with pytest.raises(TypeError, match="Symbol name must be a string"):
        Symbol(123)
    with pytest.raises(TypeError, match="Symbol name must be a string"):
        Symbol(None)

def test_symb_position_assignment():
    s1 = Symbol("pos_test_1")
    s2 = Symbol("pos_test_2")
    s3 = Symbol("pos_test_3")

    assert s1._position == 0.0
    assert s2._position == 1.0
    assert s3._position == 2.0

    # Verify write cursor advanced
    assert Symbol._write_cursor == 3.0

def test_symb_pool_and_numbered_insertion():
    s1 = Symbol("pool_test_1")
    s2 = Symbol("pool_test_2")

    assert "pool_test_1" in Symbol._pool
    assert Symbol._pool["pool_test_1"] is s1
    assert "pool_test_2" in Symbol._pool
    assert Symbol._pool["pool_test_2"] is s2

    # Verify insertion into AVLTree
    inorder_traversal = Symbol._numbered.traverse_inorder()
    assert len(inorder_traversal) == 2
    assert inorder_traversal[0] is s1
    assert inorder_traversal[1] is s2

def test_symb_repr_and_str():
    s = Symbol("repr_str_test")
    assert repr(s) == "Symbol('repr_str_test')"
    assert str(s) == "repr_str_test"

def test_symb_equality_and_hashing():
    s1 = Symbol("eq_hash_test")
    s2 = Symbol("eq_hash_test")
    s3 = Symbol("another_eq_hash_test")

    assert s1 == s2
    assert s1 != s3
    assert hash(s1) == hash(s2)
    assert hash(s1) != hash(s3)

def test_symb_less_than_comparison():
    s1 = Symbol("lt_test_1")
    s2 = Symbol("lt_test_2")
    s3 = Symbol("lt_test_3")

    assert s1 < s2
    assert s2 < s3
    assert s1 < s3
    assert not (s2 < s1)



def test_to_symb_existing_symb():
    s_orig = Symbol("existing")
    s_converted = _to_symb(s_orig)
    assert s_converted is s_orig

def test_to_symb_from_string():
    s_converted = _to_symb("from_string")
    assert isinstance(s_converted, Symbol)
    assert s_converted.name == "from_string"

def test_to_symb_from_object_with_name_attribute():
    class HasName:
        def __init__(self, name):
            self.name = name
    obj = HasName("object_with_name")
    s_converted = _to_symb(obj)
    assert isinstance(s_converted, Symbol)
    assert s_converted.name == "object_with_name"

def test_to_symb_type_error_for_unconvertible_type():
    with pytest.raises(TypeError, match="Cannot convert .* instance of .* to Symbol"):
        _to_symb(123)
    with pytest.raises(TypeError, match="Cannot convert .* instance of .* to Symbol"):
        _to_symb([1, 2])
    with pytest.raises(TypeError, match="Cannot convert .* instance of .* to Symbol"):
        _to_symb(None)
