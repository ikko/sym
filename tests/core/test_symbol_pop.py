
import pytest
from symbol.core.symbol import Symbol

def test_pop_reparents_children():
    # Create a simple hierarchy: grandparent -> parent -> child
    grandparent = Symbol("grandparent")
    parent = Symbol("parent")
    child = Symbol("child")

    grandparent.append(parent)
    parent.append(child)

    # Verify initial relationships
    assert parent in grandparent.children
    assert child in parent.children
    assert grandparent in parent.parents
    assert parent in child.parents

    # Pop the parent
    popped_symbol = parent.pop()

    # Verify that the parent was popped
    assert popped_symbol.name == "parent"

    # Verify that the child is now a child of the grandparent
    assert parent not in grandparent.children
    assert child in grandparent.children
    assert grandparent in child.parents
    assert parent not in child.parents
