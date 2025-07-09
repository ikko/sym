import pytest
from collections import defaultdict
from symbol.core.maturing import DefDict, deep_del, _apply_merge_strategy
from symbol import Symbol
import copy

# Fixture for DefDict
@pytest.fixture
def def_dict():
    return DefDict()

# Fixture for _apply_merge_strategy
@pytest.fixture
def merge_data():
    return {
        "current_dict": {"a": 1, "b": {"c": 2}, "d": [1, 2]},
        "new_dict": {"b": {"e": 3}, "f": 4, "d": [3, 4]},
        "simple_value": 10,
        "new_simple_value": 20,
        "list_value": [1, 2],
        "new_list_value": [3, 4],
        "callable_value": lambda x: x * 2
    }

# --- DefDict Tests ---

def test_def_dict_instantiation(def_dict):
    assert isinstance(def_dict, defaultdict)
    assert def_dict.default_factory is not None

def test_def_dict_nested_assignment_and_retrieval(def_dict):
    def_dict["level1"]["level2"] = "value"
    assert def_dict["level1"]["level2"] == "value"
    assert isinstance(def_dict["level1"], defaultdict)

def test_def_dict_delitem(def_dict, caplog):
    def_dict["test_key"] = "test_value"
    assert "test_key" in def_dict
    del def_dict["test_key"]
    assert "test_key" not in def_dict
    assert "Deleted key 'test_key' from DefDict. Attempting deep_del on its value." in caplog.text

def test_def_dict_delitem_non_existent(def_dict):
    with pytest.raises(KeyError, match="Key 'non_existent_key' not found in DefDict."):
        del def_dict["non_existent_key"]

# --- _apply_merge_strategy Tests ---

def test_merge_strategy_overwrite(merge_data):
    result = _apply_merge_strategy(merge_data["current_dict"], merge_data["new_dict"], 'overwrite')
    assert result == merge_data["new_dict"]

def test_merge_strategy_copy(merge_data):
    result = _apply_merge_strategy(merge_data["simple_value"], merge_data["new_simple_value"], 'copy')
    assert result == merge_data["new_simple_value"]
    # For immutable types like int, copy.copy returns the original object, so 'is not' is not applicable.
    # assert result is not merge_data["new_simple_value"] # Ensure it's a copy

def test_merge_strategy_deepcopy(merge_data):
    result = _apply_merge_strategy(merge_data["current_dict"], merge_data["new_dict"], 'deepcopy')
    assert result == merge_data["new_dict"]
    assert result is not merge_data["new_dict"] # Ensure it's a deepcopy
    assert result["b"] is not merge_data["new_dict"]["b"]

def test_merge_strategy_patch(merge_data):
    s1 = Symbol("sym1")
    s2 = Symbol("sym2")
    s1.append(Symbol("child1"))
    s2.append(Symbol("child2"))
    s2.append(Symbol("child3"))

    # Patching s1 with s2 should add s2's children to s1
    result = _apply_merge_strategy(s1, s2, 'patch')
    assert result is s1
    assert Symbol("child2") in s1.children
    assert Symbol("child3") in s1.children

def test_merge_strategy_patch_non_symbol(merge_data, caplog):
    result = _apply_merge_strategy(merge_data["simple_value"], merge_data["new_simple_value"], 'patch')
    assert result == merge_data["new_simple_value"]
    assert "Patch strategy only applies to Symbol objects. Overwriting instead." in caplog.text

def test_merge_strategy_pipe(merge_data):
    current = 5
    new_callable = lambda x: x + 10
    result = _apply_merge_strategy(current, new_callable, 'pipe')
    assert result == 15

def test_merge_strategy_pipe_non_callable(merge_data, caplog):
    current = 5
    new_value = 10
    result = _apply_merge_strategy(current, new_value, 'pipe')
    assert result == new_value
    assert "Pipe strategy requires new_value to be callable. Overwriting instead." in caplog.text

def test_merge_strategy_update(merge_data):
    current = {"a": 1, "b": 2}
    new = {"b": 3, "c": 4}
    result = _apply_merge_strategy(current, new, 'update')
    assert result == {"a": 1, "b": 3, "c": 4}
    assert result is current # Should modify in place

def test_merge_strategy_update_non_mapping(merge_data, caplog):
    current = [1, 2]
    new = {"a": 1}
    result = _apply_merge_strategy(current, new, 'update')
    assert result == new
    assert "Update strategy only applies to mappings. Overwriting instead." in caplog.text

def test_merge_strategy_extend(merge_data):
    current = [1, 2]
    new = [3, 4]
    result = _apply_merge_strategy(current, new, 'extend')
    assert result == [1, 2, 3, 4]
    assert result is current # Should modify in place

def test_merge_strategy_extend_non_list(merge_data, caplog):
    current = {"a": 1}
    new = [1, 2]
    result = _apply_merge_strategy(current, new, 'extend')
    assert result == new
    assert "Extend strategy only applies to lists. Overwriting instead." in caplog.text

def test_merge_strategy_smooth_simple_dict(merge_data):
    current = {"a": 1, "b": 2}
    new = {"b": 3, "c": 4}
    result = _apply_merge_strategy(current, new, 'smooth')
    assert result == {"a": 1, "b": 2, "b_new": 3, "c": 4}

def test_merge_strategy_smooth_nested_dict(merge_data):
    current = {"a": 1, "b": {"c": 2, "d": 3}}
    new = {"b": {"c": 4, "e": 5}, "f": 6}
    result = _apply_merge_strategy(current, new, 'smooth')
    assert result == {"a": 1, "b": {"c": 2, "c_new": 4, "d": 3, "e": 5}, "f": 6}

def test_merge_strategy_smooth_lists(merge_data):
    current = {"a": [1, 2]}
    new = {"a": [3, 4]}
    result = _apply_merge_strategy(current, new, 'smooth')
    assert result == {"a": [1, 2, 3, 4]}

def test_merge_strategy_smooth_non_mapping_conflict_overwrite(merge_data):
    current = {"a": 1}
    new = {"a": 2}
    result = _apply_merge_strategy(current, new, 'smooth', non_mapping_conflict_strategy='overwrite')
    assert result == {"a": 2}

def test_merge_strategy_smooth_non_mapping_conflict_keep_current(merge_data):
    current = {"a": 1}
    new = {"a": 2}
    result = _apply_merge_strategy(current, new, 'smooth', non_mapping_conflict_strategy='keep_current')
    assert result == {"a": 1}

def test_merge_strategy_smooth_non_mapping_conflict_raise_error(merge_data):
    current = {"a": 1}
    new = {"a": 2}
    with pytest.raises(ValueError, match="Conflict for key 'a': Cannot merge non-mapping types with 'raise_error' strategy."):
        _apply_merge_strategy(current, new, 'smooth', non_mapping_conflict_strategy='raise_error')

def test_merge_strategy_smooth_non_mapping_conflict_add_sibling(merge_data):
    current = {"a": 1}
    new = {"a": 2}
    result = _apply_merge_strategy(current, new, 'smooth', non_mapping_conflict_strategy='add_sibling')
    assert result == {"a": 1, "a_new": 2}

def test_merge_strategy_smooth_mixed_types_overwrite(merge_data):
    current = {"a": {"b": 1}}
    new = {"a": [2, 3]}
    result = _apply_merge_strategy(current, new, 'smooth')
    assert result == {"a": [2, 3]}

def test_merge_strategy_unknown(merge_data, caplog):
    current = {"a": 1}
    new = {"a": 2}
    result = _apply_merge_strategy(current, new, 'unknown_strategy')
    assert result == new
    assert "Unknown merge strategy 'unknown_strategy'. Overwriting instead." in caplog.text

# --- deep_del Tests ---

def test_deep_del_existing_attribute(caplog):
    class TestObj:
        def __init__(self):
            self.attr = "value"
    obj = TestObj()
    assert hasattr(obj, "attr")
    deep_del(obj, "attr")
    assert not hasattr(obj, "attr")
    assert "Deleted attribute 'attr' from" in caplog.text

def test_deep_del_non_existent_attribute(caplog):
    class TestObj:
        pass
    obj = TestObj()
    deep_del(obj, "non_existent_attr")
    assert "Attempted to deep_del non-existent attribute 'non_existent_attr' from" in caplog.text
