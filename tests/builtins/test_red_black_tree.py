import pytest
from builtin.red_black_tree import RedBlackTree, RedBlackNode, RED, BLACK
from core.base_symb import BaseSymbol as Symbol

@pytest.fixture
def empty_rb_tree():
    return RedBlackTree()

@pytest.fixture
def populated_rb_tree():
    tree = RedBlackTree()
    s1 = Symbol("A")
    s2 = Symbol("B")
    s3 = Symbol("C")
    s4 = Symbol("D")
    s5 = Symbol("E")
    s6 = Symbol("F")
    s7 = Symbol("G")

    # Insert in an order that creates a somewhat balanced tree
    tree.insert(s4, 40.0)
    tree.insert(s2, 20.0)
    tree.insert(s6, 60.0)
    tree.insert(s1, 10.0)
    tree.insert(s3, 30.0)
    tree.insert(s5, 50.0)
    tree.insert(s7, 70.0)
    return tree, s1, s2, s3, s4, s5, s6, s7

def test_rb_tree_insert_and_traverse_inorder(empty_rb_tree):
    tree = empty_rb_tree
    s1 = Symbol("Node1")
    s2 = Symbol("Node2")
    s3 = Symbol("Node3")
    s4 = Symbol("Node4")
    s5 = Symbol("Node5")

    tree.insert(s1, 10.0)
    tree.insert(s2, 20.0)
    tree.insert(s3, 5.0)
    tree.insert(s4, 15.0)
    tree.insert(s5, 25.0)

    inorder = tree.traverse_inorder()
    assert inorder == [s3, s1, s4, s2, s5]

def test_rb_tree_to_ascii(empty_rb_tree):
    tree = empty_rb_tree
    s1 = Symbol("Node1")
    s2 = Symbol("Node2")
    s3 = Symbol("Node3")

    tree.insert(s1, 10.0)
    tree.insert(s2, 20.0)
    tree.insert(s3, 5.0)

    # The exact ASCII output depends on the internal structure after balancing
    # This is a basic check to ensure it produces some output without errors
    ascii_output = tree.to_ascii()
    assert isinstance(ascii_output, str)
    assert len(ascii_output) > 0
    assert "Node1" in ascii_output
    assert "Node2" in ascii_output
    assert "Node3" in ascii_output

def test_rb_tree_search(populated_rb_tree):
    tree, s1, s2, s3, s4, s5, s6, s7 = populated_rb_tree

    assert tree.search(40.0).symb is s4
    assert tree.search(10.0).symb is s1
    assert tree.search(70.0).symb is s7
    assert tree.search(99.0) is None

def test_rb_tree_remove_leaf_node(populated_rb_tree):
    tree, s1, s2, s3, s4, s5, s6, s7 = populated_rb_tree
    tree.remove(10.0) # Remove s1 (leaf)
    inorder = tree.traverse_inorder()
    assert s1 not in inorder
    assert tree.search(10.0) is None
    assert len(inorder) == 6

def test_rb_tree_remove_node_with_one_child(populated_rb_tree):
    tree, s1, s2, s3, s4, s5, s6, s7 = populated_rb_tree
    tree.remove(20.0) # Remove s2 (has one child, s3)
    inorder = tree.traverse_inorder()
    assert s2 not in inorder
    assert tree.search(20.0) is None
    assert len(inorder) == 6

def test_rb_tree_remove_node_with_two_children(populated_rb_tree):
    tree, s1, s2, s3, s4, s5, s6, s7 = populated_rb_tree
    tree.remove(40.0) # Remove s4 (root, has two children)
    inorder = tree.traverse_inorder()
    assert s4 not in inorder
    assert tree.search(40.0) is None
    assert len(inorder) == 6

def test_rb_tree_remove_root_node(populated_rb_tree):
    tree, s1, s2, s3, s4, s5, s6, s7 = populated_rb_tree
    tree.remove(40.0) # Remove s4 (root)
    assert tree.root.symb is not s4
    assert tree.search(40.0) is None

def test_rb_tree_remove_non_existent_node(populated_rb_tree):
    tree, s1, s2, s3, s4, s5, s6, s7 = populated_rb_tree
    initial_len = len(tree.traverse_inorder())
    tree.remove(99.0) # Remove non-existent
    assert len(tree.traverse_inorder()) == initial_len

def test_rb_tree_remove_from_empty_tree(empty_rb_tree):
    tree = empty_rb_tree
    tree.remove(10.0) # Should not raise error
    assert tree.root is None
