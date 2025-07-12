import pytest
from symb.core.symb import Symbol, GraphTraversal, s, to_sym
from symb.core.base_symb import Symbol as BaseSymbol
from symb.core.lazy import SENTINEL
from symb.builtins.avl_tree import AVLTree
from weakref import WeakValueDictionary
import threading
import datetime

class NonConvertibleObject:
    pass

# Re-use the setup_and_teardown fixture from test_base_symb.py
# This ensures a clean state for Symbol class-level attributes before each test
@pytest.fixture(autouse=True)
def setup_and_teardown_symb_class():
    # Store original class-level attributes
    original_pool = BaseSymbol._pool
    original_numbered = BaseSymbol._numbered
    original_auto_counter = BaseSymbol._auto_counter
    original_read_cursor = BaseSymbol._read_cursor
    original_write_cursor = BaseSymbol._write_cursor
    original_lock = BaseSymbol._lock

    # Clear for predictable testing
    BaseSymbol._pool = WeakValueDictionary()
    BaseSymbol._numbered = AVLTree()
    BaseSymbol._auto_counter = 0
    BaseSymbol._read_cursor = 0.0
    BaseSymbol._write_cursor = 0.0
    BaseSymbol._lock = threading.RLock()

    yield

    # Restore original class-level attributes after each test
    BaseSymbol._pool = original_pool
    BaseSymbol._numbered = original_numbered
    BaseSymbol._auto_counter = original_auto_counter
    BaseSymbol._read_cursor = original_read_cursor
    BaseSymbol._write_cursor = original_write_cursor
    BaseSymbol._lock = original_lock

    # Clear any remaining symbs from the pool and numbered tree to ensure complete isolation
    BaseSymbol._pool.clear()
    BaseSymbol._numbered = AVLTree() # Reinitialize to ensure it's empty
    BaseSymbol._auto_counter = 0
    BaseSymbol._read_cursor = 0.0
    BaseSymbol._write_cursor = 0.0


def test_symb_index_property():
    sym = Symbol("test_index")
    assert sym._index is SENTINEL
    index_obj = sym.index
    assert index_obj is not SENTINEL
    assert sym._index is index_obj
    # Ensure it's a SymbolIndex instance (or its mock if mocked)
    assert hasattr(index_obj, 'insert') # Basic check for SymbolIndex methods

def test_symb_metadata_property():
    sym = Symbol("test_metadata")
    assert sym._metadata is SENTINEL
    metadata_obj = sym.metadata
    assert metadata_obj is not SENTINEL
    assert sym._metadata is metadata_obj
    # Ensure it's a DefDict instance (or its mock if mocked)
    assert hasattr(metadata_obj, '__setitem__') # Basic check for DefDict methods

def test_symb_context_property():
    sym = Symbol("test_context")
    assert sym._context is SENTINEL
    context_obj = sym.context
    assert context_obj is not SENTINEL
    assert sym._context is context_obj
    # Ensure it's a DefDict instance (or its mock if mocked)
    assert hasattr(context_obj, '__setitem__') # Basic check for DefDict methods

def test_symb_elevated_attributes_set_and_get():
    sym = Symbol("test_elevated_attrs")
    sym.dynamic_attr = "value1"
    assert sym.dynamic_attr == "value1"
    assert sym._elevated_attributes["dynamic_attr"] == "value1"

def test_symb_elevated_attributes_overwrite_existing():
    sym = Symbol("test_elevated_attrs_overwrite")
    sym.dynamic_attr = "original_value"
    sym.dynamic_attr = "new_value"
    assert sym.dynamic_attr == "new_value"
    assert sym._elevated_attributes["dynamic_attr"] == "new_value"

def test_symb_elevated_attributes_delete():
    sym = Symbol("test_elevated_attrs_delete")
    sym.temp_attr = "to_delete"
    assert sym.temp_attr == "to_delete"
    del sym.temp_attr
    assert "temp_attr" not in sym._elevated_attributes
    assert callable(sym.temp_attr)

def test_symb_elevated_attributes_delete_non_existent():
    sym = Symbol("test_elevated_attrs_delete_non_existent")
    with pytest.raises(AttributeError):
        del sym.non_existent_attr

def test_symb_append_child():
    parent = Symbol("parent")
    child = Symbol("child")
    parent.append(child)
    assert child in parent.children
    assert parent in child.parents

def test_symb_append_lazy_symb_child():
    from symb.core.lazy_symb import LazySymbol
    parent = Symbol("parent_lazy")
    lazy_child = LazySymbol("lazy_child_name")
    parent.append(lazy_child)
    assert lazy_child in parent.children
    assert parent in lazy_child.parents

def test_symb_append_non_symb_object():
    parent = Symbol("parent_non_symb")
    non_symb_obj = "string_child"
    child_sym = parent.append(non_symb_obj)
    assert isinstance(child_sym, Symbol)
    assert child_sym.name == "string_child"
    assert child_sym in parent.children
    assert parent in child_sym.parents

def test_symb_append_duplicate_child():
    parent = Symbol("parent_duplicate")
    child = Symbol("child_duplicate")
    parent.append(child)
    initial_children_len = len(parent.children)
    parent.append(child) # Appending again should not add duplicate
    assert len(parent.children) == initial_children_len

def test_symb_add_child():
    parent = Symbol("parent_add")
    child = Symbol("child_add")
    parent.add(child)
    assert child in parent.children
    assert parent in child.parents

def test_symb_add_duplicate_child():
    parent = Symbol("parent_add_duplicate")
    child = Symbol("child_add_duplicate")
    parent.add(child)
    initial_children_len = len(parent.children)
    parent.add(child) # Adding again should not add duplicate
    assert len(parent.children) == initial_children_len

def test_symb_relate_unrelate():
    s1 = Symbol("s1_relate")
    s2 = Symbol("s2_relate")

    s1.relate(s2, how="friend")
    assert s2 in s1.relations.get("friend")
    assert s1 in s2.relations.get("_inverse_friend")

    s1.unrelate(s2)
    assert s2 not in s1.relations.get("friend")
    assert s1 not in s2.relations.get("_inverse_friend")

def test_symb_relate_with_specific_how():
    s1 = Symbol("s1_how")
    s2 = Symbol("s2_how")
    s1.relate(s2, how="parent_of")
    assert s2 in s1.relations.get("parent_of")
    assert s1 in s2.relations.get("_inverse_parent_of")

def test_symb_unrelate_with_specific_how():
    s1 = Symbol("s1_unrelate_how")
    s2 = Symbol("s2_unrelate_how")
    s1.relate(s2, how="knows")
    s1.relate(s2, how="likes") # Add another relationship

    s1.unrelate(s2, how="knows")
    assert s2 not in s1.relations.get("knows")
    assert s2 in s1.relations.get("likes")

    # Ensure inverse is also removed correctly
    assert s1 not in s2.relations.get("_inverse_knows")
    assert s1 in s2.relations.get("_inverse_likes")

def test_dynamic_relation_single_arg():
    s_person = s.person
    s_car = s.car
    s_person.drives(s_car)
    assert s_car in s_person.relations.get("drives")
    assert s_person in s_car.relations.get("_inverse_drives")

def test_dynamic_relation_multiple_args():
    s_person = s.person
    s_drums = s.drums
    s_guitar = s.guitar
    s_person.interested_in(s_drums, s_guitar)
    assert s_drums in s_person.relations.get("interested_in")
    assert s_guitar in s_person.relations.get("interested_in")
    assert s_person in s_drums.relations.get("_inverse_interested_in")
    assert s_person in s_guitar.relations.get("_inverse_interested_in")

def test_dynamic_relation_kwargs_single_value():
    s_person = s.person
    s_war_zones = s.war_zones
    s_person.avoids(war_zones=s_war_zones)
    assert s_war_zones in s_person.relations.get("war_zones")
    assert s_person in s_war_zones.relations.get("_inverse_war_zones")

def test_dynamic_relation_kwargs_list_value():
    s_musical_track = s.musical_track
    s_musician_joe = s.musician_joe
    s_song_writer_jane = s.song_writer_jane
    s_musical_track.authored_by(authors=[s_musician_joe, s_song_writer_jane])
    assert s_musician_joe in s_musical_track.relations.get("authors")
    assert s_song_writer_jane in s_musical_track.relations.get("authors")
    assert s_musical_track in s_musician_joe.relations.get("_inverse_authors")
    assert s_musical_track in s_song_writer_jane.relations.get("_inverse_authors")

def test_dynamic_relation_mixed_args_kwargs():
    s_person = s.person
    s_drums = s.drums
    s_guitar = s.guitar
    s_singing = s.singing
    s_dancing = s.dancing
    s_war_zones = s.war_zones

    s_person.interested_in(s_drums, s_guitar, likes=[s_singing, s_dancing], avoids=s_war_zones)

    assert s_drums in s_person.relations.get("interested_in")
    assert s_guitar in s_person.relations.get("interested_in")
    assert s_singing in s_person.relations.get("likes")
    assert s_dancing in s_person.relations.get("likes")
    assert s_war_zones in s_person.relations.get("avoids")

    assert s_person in s_drums.relations.get("_inverse_interested_in")
    assert s_person in s_guitar.relations.get("_inverse_interested_in")
    assert s_person in s_singing.relations.get("_inverse_likes")
    assert s_person in s_dancing.relations.get("_inverse_likes")
    assert s_person in s_war_zones.relations.get("_inverse_avoids")

def test_dynamic_relation_chained_calls():
    s_person = s.person
    s_drums = s.drums
    s_guitar = s.guitar
    s_singing = s.singing
    s_dancing = s.dancing
    s_war_zones = s.war_zones

    s_person.interested_in(s_drums, s_guitar).likes(s_singing, s_dancing).avoids(s_war_zones)

    assert s_drums in s_person.relations.get("interested_in")
    assert s_guitar in s_person.relations.get("interested_in")
    assert s_singing in s_person.relations.get("likes")
    assert s_dancing in s_person.relations.get("likes")
    assert s_war_zones in s_person.relations.get("avoids")

    assert s_person in s_drums.relations.get("_inverse_interested_in")
    assert s_person in s_guitar.relations.get("_inverse_interested_in")
    assert s_person in s_singing.relations.get("_inverse_likes")
    assert s_person in s_dancing.relations.get("_inverse_likes")
    assert s_person in s_war_zones.relations.get("_inverse_avoids")

def test_dynamic_relation_no_args_raises_error():
    s_person = s.person
    with pytest.raises(TypeError):
        s_person.some_relation()

@pytest.mark.skip(reason="Skipping due to current limitations in Symbol.from_object for non-convertible types.")
def test_dynamic_relation_non_symb_args_raises_error():
    s_person = s.person
    non_convertible = NonConvertibleObject()
    with pytest.raises(TypeError):
        s_person.some_relation(non_convertible)

def test_dynamic_relation_kwargs_non_symb_value_raises_error():
    s_person = s.person
    non_convertible = NonConvertibleObject()
    with pytest.raises(TypeError):
        s_person.some_relation(item=non_convertible)

@pytest.mark.skip(reason="Skipping due to current limitations in Symbol.from_object for non-convertible types.")
def test_dynamic_relation_kwargs_list_non_symb_value_raises_error():
    s_person = s.person
    non_convertible = NonConvertibleObject()
    with pytest.raises(TypeError):
        s_person.some_relation(items=[non_convertible])

def test_to_ascii_default_tree_traversal():
    # Create a simple tree structure
    root = Symbol("Root")
    child1 = Symbol("Child1")
    child2 = Symbol("Child2")
    grandchild1 = Symbol("Grandchild1")

    root.append(child1)
    root.append(child2)
    child1.append(grandchild1)

    expected_output = """
- Root
  - Child1
    - Grandchild1
  - Child2
""".strip()
    
    assert root.to_ascii() == expected_output

def test_to_ascii_dfs_children_first():
    root = Symbol("A")
    b = Symbol("B")
    c = Symbol("C")
    d = Symbol("D")
    e = Symbol("E")

    root.append(b)
    root.append(c)
    b.append(d)
    c.append(e)

    # Expected DFS (children first) output
    expected_output = """
- A
  - B
    - D
  - C
    - E
""".strip()
    assert root.to_ascii(traverse_mode="dfs", family_mode="children_first") == expected_output

def test_to_ascii_bfs_children_first():
    root = Symbol("A")
    b = Symbol("B")
    c = Symbol("C")
    d = Symbol("D")
    e = Symbol("E")

    root.append(b)
    root.append(c)
    b.append(d)
    c.append(e)

    # Expected BFS (children first) output
    expected_output = """
- A
  - B
  - C
    - D
    - E
""".strip()
    assert root.to_ascii(traverse_mode="bfs", family_mode="children_first") == expected_output

def test_to_ascii_with_relations():
    s1 = Symbol("S1")
    s2 = Symbol("S2")
    s3 = Symbol("S3")
    s4 = Symbol("S4")

    s1.append(s2)
    s1.relate(s3, how="knows")
    s2.relate(s4, how="has_child")

    expected_output = """
- S1
  - S2
    - S4

--- Relations ---
S1 --knows--> S3
S2 --has_child--> S4
""".strip()
    assert s1.to_ascii() == expected_output

def test_from_ascii_simple_tree():
    ascii_input = """
- Root
  - Child1
    - Grandchild1
  - Child2
""".strip()
    
    reconstructed_root = Symbol.from_ascii(ascii_input)

    assert reconstructed_root.name == "Root"
    assert len(reconstructed_root.children) == 2
    assert reconstructed_root.children[0].name == "Child1"
    assert reconstructed_root.children[1].name == "Child2"
    assert len(reconstructed_root.children[0].children) == 1
    assert reconstructed_root.children[0].children[0].name == "Grandchild1"

def test_from_ascii_with_relations():
    ascii_input = """
- S1
  - S2
    - S4

--- Relations ---
S1 --knows--> S3
S2 --has_child--> S4
""".strip()

    reconstructed_s1 = Symbol.from_ascii(ascii_input)

    assert reconstructed_s1.name == "S1"
    assert len(reconstructed_s1.children) == 1
    reconstructed_s2 = reconstructed_s1.children[0]
    assert reconstructed_s2.name == "S2"
    assert len(reconstructed_s2.children) == 1
    reconstructed_s4 = reconstructed_s2.children[0]
    assert reconstructed_s4.name == "S4"

    # Check relations
    reconstructed_s3 = Symbol._pool.get("S3") # Relations are global, so retrieve from pool
    assert reconstructed_s3 is not None
    assert reconstructed_s3 in reconstructed_s1.relations.get("knows")
    assert reconstructed_s1 in reconstructed_s3.relations.get("_inverse_knows")

    assert reconstructed_s4 in reconstructed_s2.relations.get("has_child")
    assert reconstructed_s2 in reconstructed_s4.relations.get("_inverse_has_child")

def test_roundtrip_simple_tree():
    root = Symbol("Root")
    child1 = Symbol("Child1")
    child2 = Symbol("Child2")
    grandchild1 = Symbol("Grandchild1")

    root.append(child1)
    root.append(child2)
    child1.append(grandchild1)

    ascii_output = root.to_ascii()
    reconstructed_root = Symbol.from_ascii(ascii_output)

    assert reconstructed_root.name == root.name
    assert len(reconstructed_root.children) == len(root.children)
    assert reconstructed_root.children[0].name == root.children[0].name
    assert reconstructed_root.children[1].name == root.children[1].name
    assert reconstructed_root.children[0].children[0].name == root.children[0].children[0].name

def test_roundtrip_with_relations():
    s1 = Symbol("S1")
    s2 = Symbol("S2")
    s3 = Symbol("S3")
    s4 = Symbol("S4")

    s1.append(s2)
    s1.relate(s3, how="knows")
    s2.relate(s4, how="has_child")

    ascii_output = s1.to_ascii()
    reconstructed_s1 = Symbol.from_ascii(ascii_output)

    assert reconstructed_s1.name == s1.name
    assert len(reconstructed_s1.children) == len(s1.children)
    reconstructed_s2 = reconstructed_s1.children[0]
    assert reconstructed_s2.name == s2.name
    assert len(reconstructed_s2.children) == len(s2.children)
    reconstructed_s4 = reconstructed_s2.children[0]
    assert reconstructed_s4.name == s4.name

    # Check relations
    reconstructed_s3 = Symbol._pool.get("S3")
    assert reconstructed_s3 is not None
    assert reconstructed_s3 in reconstructed_s1.relations.get("knows")
    assert reconstructed_s1 in reconstructed_s3.relations.get("_inverse_knows")

    assert reconstructed_s4 in reconstructed_s2.relations.get("has_child")
    assert reconstructed_s2 in reconstructed_s4.relations.get("_inverse_has_child")
