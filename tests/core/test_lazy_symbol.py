import pytest
from symb import Symbol
from core.lazy_symb import LazySymbol

def test_lazy_symb_evaluation():
    # Create a list that will be converted to a Symbol with LazySymbol children
    my_list = [1, 2, 3]

    # Convert the list to a Symbol. This should return a concrete Symbol.
    list_symb = Symbol.from_object(my_list)

    # The list_symb itself should be a Symbol instance
    assert isinstance(list_symb, Symbol)

    # Its children should be LazySymbol instances
    assert len(list_symb.children) == 3
    assert all(isinstance(child, LazySymbol) for child in list_symb.children)

    # Access an attribute of the first child to trigger its evaluation
    first_child_lazy = list_symb.children[0]
    _ = first_child_lazy.name

    # Now, the first child should be a concrete Symbol instance
    assert isinstance(first_child_lazy._symb, Symbol)
    assert first_child_lazy._symb.name == "1"

    # The other children should still be LazySymbol instances
    assert isinstance(list_symb.children[1], LazySymbol)
    assert isinstance(list_symb.children[2], LazySymbol)
