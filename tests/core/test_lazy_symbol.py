import pytest
from symbol import Symbol
from symbol.core.lazy_symbol import LazySymbol

def test_lazy_symbol_evaluation():
    # Create a list that will be converted to a Symbol with LazySymbol children
    my_list = [1, 2, 3]

    # Convert the list to a Symbol. This should return a concrete Symbol.
    list_symbol = Symbol.from_object(my_list)

    # The list_symbol itself should be a Symbol instance
    assert isinstance(list_symbol, Symbol)

    # Its children should be LazySymbol instances
    assert len(list_symbol.children) == 3
    assert all(isinstance(child, LazySymbol) for child in list_symbol.children)

    # Access an attribute of the first child to trigger its evaluation
    first_child_lazy = list_symbol.children[0]
    _ = first_child_lazy.name

    # Now, the first child should be a concrete Symbol instance
    assert isinstance(first_child_lazy._symbol, Symbol)
    assert first_child_lazy._symbol.name == "1"

    # The other children should still be LazySymbol instances
    assert isinstance(list_symbol.children[1], LazySymbol)
    assert isinstance(list_symbol.children[2], LazySymbol)
