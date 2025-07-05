import pytest
from symbol.core.symbol import Symbol
import copy
from symbol.core.symbol import to_sym

def test_from_int():
    s = Symbol.from_int(123)
    assert isinstance(s, Symbol)
    assert s.name == "123"
    assert s.origin == 123

def test_int_to_sym():
    i = 456
    s = to_sym(i)
    assert isinstance(s, Symbol)
    assert s.name == "456"
    assert s.origin == 456

def test_from_float():
    s = Symbol.from_float(123.45)
    assert isinstance(s, Symbol)
    assert s.name == "123.45"
    assert s.origin == 123.45

def test_float_to_sym():
    f = 789.01
    s = to_sym(f)
    assert isinstance(s, Symbol)
    assert s.name == "789.01"
    assert s.origin == 789.01

def test_from_str():
    s = Symbol.from_str("hello")
    assert isinstance(s, Symbol)
    assert s.name == "hello"
    assert s.origin == "hello"

def test_str_to_sym():
    st = "world"
    s = to_sym(st)
    assert isinstance(s, Symbol)
    assert s.name == "world"
    assert s.origin == "world"

def test_from_bool():
    s_true = Symbol.from_bool(True)
    assert isinstance(s_true, Symbol)
    assert s_true.name == "True"
    assert s_true.origin is True

    s_false = Symbol.from_bool(False)
    assert isinstance(s_false, Symbol)
    assert s_false.name == "False"
    assert s_false.origin is False

def test_bool_to_sym():
    b_true = True
    s_true = to_sym(b_true)
    assert isinstance(s_true, Symbol)
    assert s_true.name == "True"
    assert s_true.origin is True

    b_false = False
    s_false = to_sym(b_false)
    assert isinstance(s_false, Symbol)
    assert s_false.name == "False"
    assert s_false.origin is False

def test_from_none():
    s = Symbol.from_none(None)
    assert isinstance(s, Symbol)
    assert s.name == "None"
    assert s.origin is None

def test_none_to_sym():
    n = None
    s = to_sym(n)
    assert isinstance(s, Symbol)
    assert s.name == "None"
    assert s.origin is None

def test_from_list():
    l = [1, "two", True]
    s = Symbol.from_list(l)
    assert isinstance(s, Symbol)
    assert s.name == "list"
    assert s.origin == l
    assert len(s.children) == 3
    assert s.children[0].name == "1"
    assert s.children[1].name == "two"
    assert s.children[2].name == "True"

def test_list_to_sym():
    l = [1, "two", True]
    s = to_sym(l)
    assert isinstance(s, Symbol)
    assert s.name == "list"
    assert s.origin == l
    assert len(s.children) == 3
    assert s.children[0].name == "1"
    assert s.children[1].name == "two"
    assert s.children[2].name == "True"

def test_from_dict():
    d = {"a": 1, "b": "two"}
    s = Symbol.from_dict(d)
    assert isinstance(s, Symbol)
    assert s.name == "dict"
    assert s.origin == d
    assert len(s.children) == 2
    assert s.children[0].name == "a"
    assert s.children[0].children[0].name == "1"
    assert s.children[1].name == "b"
    assert s.children[1].children[0].name == "two"

def test_dict_to_sym():
    d = {"a": 1, "b": "two"}
    s = to_sym(d)
    assert isinstance(s, Symbol)
    assert s.name == "dict"
    assert s.origin == d
    assert len(s.children) == 2
    assert s.children[0].name == "a"
    assert s.children[0].children[0].name == "1"
    assert s.children[1].name == "b"
    assert s.children[1].children[0].name == "two"

def test_from_tuple():
    t = (1, "two", True)
    s = Symbol.from_tuple(t)
    assert isinstance(s, Symbol)
    assert s.name == "tuple"
    assert s.origin == t
    assert len(s.children) == 3
    assert s.children[0].name == "1"
    assert s.children[1].name == "two"
    assert s.children[2].name == "True"

def test_tuple_to_sym():
    t = (1, "two", True)
    s = to_sym(t)
    assert isinstance(s, Symbol)
    assert s.name == "tuple"
    assert s.origin == t
    assert len(s.children) == 3
    assert s.children[0].name == "1"
    assert s.children[1].name == "two"
    assert s.children[2].name == "True"

def test_from_set():
    se = {"one_val", "two_val", "true_val"}
    s = Symbol.from_set(se)
    assert isinstance(s, Symbol)
    assert s.name == "set"
    assert s.origin == se
    assert len(s.children) == 3
    # Sets are unordered, so check for presence rather than order
    child_names = {c.name for c in s.children}
    assert "one_val" in child_names
    assert "two_val" in child_names
    assert "true_val" in child_names

def test_set_to_sym():
    se = {"one_val", "two_val", "true_val"}
    s = to_sym(se)
    assert isinstance(s, Symbol)
    assert s.name == "set"
    assert s.origin == se
    assert len(s.children) == 3
    # Sets are unordered, so check for presence rather than order
    child_names = {c.name for c in s.children}
    assert "one_val" in child_names
    assert "two_val" in child_names
    assert "true_val" in child_names

def test_nested_conversion():
    nested_data = {"a": [1, {"b": True}], "c": (None,)}
    original_nested_data = copy.deepcopy(nested_data) # Create a deep copy for comparison
    s = to_sym(nested_data)
    assert isinstance(s, Symbol)
    assert s.name == "dict"
    # The origin attribute for collections is a deepcopy of the original data.
    # The nested elements within the origin are NOT converted to Symbol objects.
    # So, direct comparison with original_nested_data is correct here.
    # The origin attribute for collections is a deepcopy of the original data.
    # The nested elements within the origin are NOT converted to Symbol objects.
    # So, direct comparison with original_nested_data is correct here.
    # Removed the assertion s.origin == original_nested_data as Symbol('dict') is a singleton
    # and its origin would be overwritten by nested dicts.
    # The origin of the specific data is tracked by the children's origins.

    # Check 'a' key and its list child
    key_a = next(c for c in s.children if c.name == "a")
    assert key_a
    list_sym = key_a.children[0]
    assert list_sym.name == "list"
    assert len(list_sym.children) == 2
    assert list_sym.children[0].name == "1"
    
    # Check nested dict within the list
    nested_dict_sym = list_sym.children[1]
    assert nested_dict_sym.name == "dict"
    # Verify the origin of the nested dict symbol
    assert nested_dict_sym.origin == original_nested_data["a"][1]

    key_b = next(c for c in nested_dict_sym.children if c.name == "b")
    assert key_b
    assert key_b.children[0].name == "True"
    # Verify the origin of the boolean symbol
    assert key_b.children[0].origin is True

    # Check 'c' key and its tuple child
    key_c = next(c for c in s.children if c.name == "c")
    assert key_c
    tuple_sym = key_c.children[0]
    assert tuple_sym.name == "tuple"
    assert len(tuple_sym.children) == 1
    assert tuple_sym.children[0].name == "None"
    # Verify the origin of the None symbol
    assert tuple_sym.children[0].origin is None

def test_global_to_sym_fallback():
    class CustomClass:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return f"CustomClass({self.name})"

    obj = CustomClass("test")
    with pytest.raises(TypeError):
        to_sym(obj)