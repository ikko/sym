import pytest
from sym import Symbol
from sym.core.lazy_sym import LazySymbol

def test_lazy_sym_evaluation():
    # Create a list that will be converted to a Symbol with LazySymbol children
    my_list = [1, 2, 3]

    # Convert the list to a Symbol. This should return a concrete Symbol.
    list_sym = Symbol.from_object(my_list)

    # The list_sym itself should be a Symbol instance
    assert isinstance(list_sym, Symbol)

    # Its children should be LazySymbol instances
    assert len(list_sym.children) == 3
    assert all(isinstance(child, LazySymbol) for child in list_sym.children)

    # Access an attribute of the first child to trigger its evaluation
    first_child_lazy = list_sym.children[0]
    _ = first_child_lazy.name

    # Now, the first child should be a concrete Symbol instance
    assert isinstance(first_child_lazy._sym, Symbol)
    assert first_child_lazy._sym.name == "1"

    # The other children should still be LazySymbol instances
    assert isinstance(list_sym.children[1], LazySymbol)
    assert isinstance(list_sym.children[2], LazySymbol)
