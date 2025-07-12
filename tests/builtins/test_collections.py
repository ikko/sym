import pytest
from symb import Symbol
from symb.builtin.collections import OrderedSymbolSet

def test_ordered_symb_set_creation_and_add():
    # Test creation with no initial symbs
    s_set = OrderedSymbolSet()
    assert len(s_set) == 0

    # Test adding a single symb
    sym1 = Symbol("sym1")
    s_set.add(sym1)
    assert len(s_set) == 1
    assert sym1 in s_set

    # Test adding multiple symbs
    sym2 = Symbol("sym2")
    sym3 = Symbol("sym3")
    s_set.add(sym2)
    s_set.add(sym3)
    assert len(s_set) == 3
    assert sym2 in s_set
    assert sym3 in s_set

    # Test adding an existing symb (should not increase size)
    s_set.add(sym1)
    assert len(s_set) == 3

    # Test creation with initial symbs
    sym4 = Symbol("sym4")
    sym5 = Symbol("sym5")
    s_set2 = OrderedSymbolSet([sym4, sym5])
    assert len(s_set2) == 2
    assert sym4 in s_set2
    assert sym5 in s_set2

def test_ordered_symb_set_iteration_length_and_containment():
    sym1 = Symbol("alpha")
    sym2 = Symbol("beta")
    sym3 = Symbol("gamma")
    s_set = OrderedSymbolSet([sym1, sym2, sym3])

    # Test length
    assert len(s_set) == 3

    # Test iteration order (should be insertion order)
    expected_order = [sym1, sym2, sym3]
    actual_order = list(s_set)
    assert actual_order == expected_order

    # Test containment
    assert sym1 in s_set
    assert Symbol("alpha") in s_set # Should work due to Symbol interning
    assert Symbol("non_existent") not in s_set

    # Test iteration after adding more elements
    sym4 = Symbol("delta")
    s_set.add(sym4)
    expected_order_after_add = [sym1, sym2, sym3, sym4]
    assert list(s_set) == expected_order_after_add

    # Test iteration after removing elements (if remove method exists)
    # Assuming a remove method will be added later if needed for full coverage
