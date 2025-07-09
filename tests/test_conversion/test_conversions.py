import pytest
from sym import Symbol
import copy
from sym.core.sym import to_sym

def test_from_int():
    s = Symbol.from_object(123)
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
    s = Symbol.from_object(123.45)
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
    s = Symbol.from_object("hello")
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
    s_true = Symbol.from_object(True)

    s_false = Symbol.from_object(False)
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

@pytest.mark.skip(reason="Not implemented")
def test_from_none():
    s = Symbol.from_object(None)
    assert isinstance(s, Symbol)
    assert s.name == "None"
    assert s.origin is None

@pytest.mark.skip(reason="Not implemented")
def test_none_to_sym():
    n = None
    s = to_sym(n)
    assert isinstance(s, Symbol)
    assert s.name == "None"
    assert s.origin is None

def test_from_list():
    l = [1, "two", True]
    s = Symbol.from_object(l)
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
    s = Symbol.from_object(d)
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
    s = Symbol.from_object(t)
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
    s = Symbol.from_object(se)
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



def test_global_to_sym_fallback():
    class CustomClass:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return f"CustomClass({self.name})"

    obj = CustomClass("test")
    with pytest.raises(TypeError):
        to_sym(obj)
