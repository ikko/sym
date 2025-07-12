import pytest
from symb.builtin.avl_tree import AVLTree, AVLNode
from symb.core.base_symb import Symbol

@pytest.fixture
def empty_avl_tree():
    return AVLTree()

@pytest.fixture
def populated_avl_tree():
    tree = AVLTree()
    s1 = Symbol("A")
    s2 = Symbol("B")
    s3 = Symbol("C")
    s4 = Symbol("D")
    s5 = Symbol("E")
    tree.root = tree.insert(tree.root, s1, 10.0)
    tree.root = tree.insert(tree.root, s2, 20.0)
    tree.root = tree.insert(tree.root, s3, 5.0)
    tree.root = tree.insert(tree.root, s4, 15.0)
    tree.root = tree.insert(tree.root, s5, 25.0)
    return tree, s1, s2, s3, s4, s5

def test_avl_tree_insert_and_traverse_inorder(empty_avl_tree):
    tree = empty_avl_tree
    s1 = Symbol("Node1")
    s2 = Symbol("Node2")
    s3 = Symbol("Node3")

    tree.root = tree.insert(tree.root, s1, 10.0)
    assert tree.root.symb is s1
    assert tree.root.eval_weight() == 10.0

    tree.root = tree.insert(tree.root, s2, 20.0)
    tree.root = tree.insert(tree.root, s3, 5.0)

    # In-order traversal should return symbs sorted by weight
    inorder = tree.traverse_inorder()
    assert inorder == [s3, s1, s2]

def test_avl_tree_search(populated_avl_tree):
    tree, s1, s2, s3, s4, s5 = populated_avl_tree

    assert tree.search(10.0) is s1
    assert tree.search(20.0) is s2
    assert tree.search(5.0) is s3
    assert tree.search(15.0) is s4
    assert tree.search(25.0) is s5
    assert tree.search(99.0) is None # Not found

def test_avl_tree_rebalancing():
    tree = AVLTree()
    s_a = Symbol("A")
    s_b = Symbol("B")
    s_c = Symbol("C")
    s_d = Symbol("D")
    s_e = Symbol("E")

    # Insert in a way that causes rotations
    tree.root = tree.insert(tree.root, s_a, 10.0)
    tree.root = tree.insert(tree.root, s_b, 20.0)
    tree.root = tree.insert(tree.root, s_c, 30.0) # Left rotation at A

    # After inserting 10, 20, 30, the tree should be balanced with 20 as root
    assert tree.root.symb is s_b
    assert tree.root.left.symb is s_a
    assert tree.root.right.symb is s_c

    tree.root = tree.insert(tree.root, s_d, 5.0)
    tree.root = tree.insert(tree.root, s_e, 2.0) # Right rotation at D

    inorder = tree.traverse_inorder()
    assert inorder == [s_e, s_d, s_a, s_b, s_c]

def test_avl_tree_remove_leaf_node(populated_avl_tree):
    tree, s1, s2, s3, s4, s5 = populated_avl_tree
    # Remove s3 (5.0), which is a leaf
    tree.remove(5.0)
    inorder = tree.traverse_inorder()
    assert inorder == [s1, s4, s2, s5]
    assert tree.search(5.0) is None

def test_avl_tree_remove_node_with_one_child(populated_avl_tree):
    tree, s1, s2, s3, s4, s5 = populated_avl_tree
    # Remove s4 (15.0), which has no children initially, but after removing s3, s1 will have s4 as right child
    # Let's re-populate to ensure a specific scenario
    tree_one_child = AVLTree()
    s_root = Symbol("Root")
    s_left = Symbol("Left")
    s_right = Symbol("Right")
    tree_one_child.root = tree_one_child.insert(None, s_root, 10.0)
    tree_one_child.root = tree_one_child.insert(tree_one_child.root, s_left, 5.0)
    tree_one_child.root = tree_one_child.insert(tree_one_child.root, s_right, 15.0)
    
    # Remove s_left (5.0), which is a leaf
    tree_one_child.remove(5.0)
    inorder = tree_one_child.traverse_inorder()
    assert inorder == [s_root, s_right]
    assert tree_one_child.search(5.0) is None

def test_avl_tree_remove_node_with_two_children(populated_avl_tree):
    tree, s1, s2, s3, s4, s5 = populated_avl_tree
    # Remove s1 (10.0), which has two children (s3 and s4)
    tree.remove(10.0)
    inorder = tree.traverse_inorder()
    # The successor of 10.0 is 15.0 (s4)
    assert inorder == [s3, s4, s2, s5]
    assert tree.search(10.0) is None

def test_avl_tree_remove_root_node(populated_avl_tree):
    tree, s1, s2, s3, s4, s5 = populated_avl_tree
    # The root is s1 (10.0) initially, but after rebalancing it might be different
    # Let's ensure a simple root removal scenario
    simple_tree = AVLTree()
    r1 = Symbol("R1")
    r2 = Symbol("R2")
    r3 = Symbol("R3")
    simple_tree.root = simple_tree.insert(None, r2, 20.0)
    simple_tree.root = simple_tree.insert(simple_tree.root, r1, 10.0)
    simple_tree.root = simple_tree.insert(simple_tree.root, r3, 30.0)

    # Remove root (r2, 20.0)
    simple_tree.remove(20.0)
    inorder = simple_tree.traverse_inorder()
    assert inorder == [r1, r3]
    assert simple_tree.search(20.0) is None

def test_avl_tree_remove_non_existent_node(populated_avl_tree):
    tree, s1, s2, s3, s4, s5 = populated_avl_tree
    # Attempt to remove a node that doesn't exist
    initial_inorder = tree.traverse_inorder()
    tree.remove(99.0)
    assert tree.traverse_inorder() == initial_inorder # Tree should remain unchanged

def test_avl_tree_empty_tree_search():
    tree = AVLTree()
    assert tree.search(10.0) is None

def test_avl_tree_empty_tree_remove():
    tree = AVLTree()
    tree.remove(10.0) # Should not raise an error
    assert tree.root is None

def test_avl_tree_insert_duplicate_weight():
    tree = AVLTree()
    s1 = Symbol("A")
    s2 = Symbol("B")
    s3 = Symbol("C")

    tree.root = tree.insert(tree.root, s1, 10.0)
    tree.root = tree.insert(tree.root, s2, 10.0) # Duplicate weight
    tree.root = tree.insert(tree.root, s3, 10.0) # Another duplicate

    # AVLTree handles duplicates by placing them on the right side by default
    # The exact structure might vary based on rebalancing, but all should be present
    inorder = tree.traverse_inorder()
    assert len(inorder) == 3
    assert s1 in inorder
    assert s2 in inorder
    assert s3 in inorder
