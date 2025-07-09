# Bidirectional Type Conversion in Symbol

This document outlines the mechanisms for converting standard Python types to `Symbol` objects and vice-versa, enhancing the framework's interoperability and ease of use.

## Concept

The `Symbol` framework provides a seamless way to represent native Python data structures as `Symbol` objects, allowing them to participate in the graph-based data model. This is achieved through:

1.  **`Symbol.from_<type>` Class Methods**: Factory methods on the `Symbol` class that convert a given Python object into a `Symbol` instance. These methods handle the creation of the `Symbol`'s name and the assignment of the original Python object to the `Symbol`'s `origin` attribute.
2.  **`to_sym()` Global Function**: A generic function that dispatches to the appropriate `Symbol.from_<type>` method based on the input object's type. This provides a unified interface for converting various Python objects to `Symbol` instances.

## Supported Types and Examples

The following standard Python types are supported for bidirectional conversion:

### Primitive Types

-   **`int`**
    ```python
    from symb import Symbol, to_sym

    # Using from_int
    s_int = Symbol.from_int(123)
    print(f"Symbol from int: {s_int.name}, Origin: {s_int.origin}") # Output: Symbol from int: 123, Origin: 123

    # Using to_sym
    s_int_2 = to_sym(456)
    print(f"Symbol from int (to_sym): {s_int_2.name}, Origin: {s_int_2.origin}") # Output: Symbol from int (to_sym): 456, Origin: 456
    ```

-   **`float`**
    ```python
    from symb import Symbol, to_sym

    # Using from_float
    s_float = Symbol.from_float(123.45)
    print(f"Symbol from float: {s_float.name}, Origin: {s_float.origin}") # Output: Symbol from float: 123.45, Origin: 123.45

    # Using to_sym
    s_float_2 = to_sym(789.01)
    print(f"Symbol from float (to_sym): {s_float_2.name}, Origin: {s_float_2.origin}") # Output: Symbol from float (to_sym): 789.01, Origin: 789.01
    ```

-   **`str`**
    ```python
    from symb import Symbol, to_sym

    # Using from_str
    s_str = Symbol.from_str("hello")
    print(f"Symbol from str: {s_str.name}, Origin: {s_str.origin}") # Output: Symbol from str: hello, Origin: hello

    # Using to_sym
    s_str_2 = to_sym("world")
    print(f"Symbol from str (to_sym): {s_str_2.name}, Origin: {s_str_2.origin}") # Output: Symbol from str (to_sym): world, Origin: world
    ```

-   **`bool`**
    ```python
    from symb import Symbol, to_sym

    # Using from_bool
    s_bool = Symbol.from_bool(True)
    print(f"Symbol from bool: {s_bool.name}, Origin: {s_bool.origin}") # Output: Symbol from bool: True, Origin: True

    # Using to_sym
    s_bool_2 = to_sym(False)
    print(f"Symbol from bool (to_sym): {s_bool_2.name}, Origin: {s_bool_2.origin}") # Output: Symbol from bool (to_sym): False, Origin: False
    ```

-   **`None`**
    ```python
    from symb import Symbol, to_sym

    # Using from_none
    s_none = Symbol.from_none(None)
    print(f"Symbol from None: {s_none.name}, Origin: {s_none.origin}") # Output: Symbol from None: None, Origin: None

    # Using to_sym
    s_none_2 = to_sym(None)
    print(f"Symbol from None (to_sym): {s_none_2.name}, Origin: {s_none_2.origin}") # Output: Symbol from None (to_sym): None, Origin: None
    ```

### Collection Types

-   **`list`**
    ```python
    from symb import Symbol, to_sym

    my_list = [1, "two", True]
    s_list = Symbol.from_list(my_list)
    print(f"Symbol from list: {s_list.name}, Origin: {s_list.origin}") # Output: Symbol from list: list, Origin: [1, 'two', True]
    print(f"Children: {[c.name for c in s_list.children]}") # Output: Children: ['1', 'two', 'True']

    s_list_2 = to_sym([4, "five", False])
    print(f"Symbol from list (to_sym): {s_list_2.name}, Origin: {s_list_2.origin}") # Output: Symbol from list (to_sym): list, Origin: [4, 'five', False]
    print(f"Children: {[c.name for c in s_list_2.children]}") # Output: Children: ['4', 'five', 'False']
    ```

-   **`dict`**
    ```python
    from symb import Symbol, to_sym

    my_dict = {"a": 1, "b": "two"}
    s_dict = Symbol.from_dict(my_dict)
    print(f"Symbol from dict: {s_dict.name}, Origin: {s_dict.origin}") # Output: Symbol from dict: dict, Origin: {'a': 1, 'b': 'two'}
    print(f"Children: {[c.name for c in s_dict.children]}") # Output: Children: ['a', 'b']

    s_dict_2 = to_sym({"x": 10, "y": "twenty"})
    print(f"Symbol from dict (to_sym): {s_dict_2.name}, Origin: {s_dict_2.origin}") # Output: Symbol from dict (to_sym): dict, Origin: {'x': 10, 'y': 'twenty'}
    print(f"Children: {[c.name for c in s_dict_2.children]}") # Output: Children: ['x', 'y']
    ```

-   **`tuple`**
    ```python
    from symb import Symbol, to_sym

    my_tuple = (1, "two", True)
    s_tuple = Symbol.from_tuple(my_tuple)
    print(f"Symbol from tuple: {s_tuple.name}, Origin: {s_tuple.origin}") # Output: Symbol from tuple: tuple, Origin: (1, 'two', True)
    print(f"Children: {[c.name for c in s_tuple.children]}") # Output: Children: ['1', 'two', 'True']

    s_tuple_2 = to_sym((4, "five", False))
    print(f"Symbol from tuple (to_sym): {s_tuple_2.name}, Origin: {s_tuple_2.origin}") # Output: Symbol from tuple (to_sym): tuple, Origin: (4, 'five', False)
    print(f"Children: {[c.name for c in s_tuple_2.children]}") # Output: Children: ['4', 'five', 'False']
    ```

-   **`set`**
    ```python
    from symb import Symbol, to_sym

    my_set = {"one_val", "two_val", "true_val"}
    s_set = Symbol.from_set(my_set)
    print(f"Symbol from set: {s_set.name}, Origin: {s_set.origin}") # Output: Symbol from set: set, Origin: {'one_val', 'two_val', 'true_val'}
    print(f"Children: {[c.name for c in s_set.children]}") # Output: Children: ['one_val', 'two_val', 'true_val'] (order may vary)

    s_set_2 = to_sym({"four_val", "five_val", "false_val"})
    print(f"Symbol from set (to_sym): {s_set_2.name}, Origin: {s_set_2.origin}") # Output: Symbol from set (to_sym): set, Origin: {'four_val', 'five_val', 'false_val'}
    print(f"Children: {[c.name for c in s_set_2.children]}") # Output: Children: ['four_val', 'five_val', 'false_val'] (order may vary)
    ```

### Nested Conversions

The `to_sym()` function and `Symbol.from_<type>` methods handle nested data structures recursively, ensuring that all elements are converted into `Symbol` instances and their `origin` attributes are correctly preserved.

```python
from symb import Symbol, to_sym

nested_data = {"a": [1, {"b": True}], "c": (None,)}
s = to_sym(nested_data)

print(f"Top-level Symbol: {s.name}, Origin: {s.origin}")
# Expected Output:
# Top-level Symbol: dict, Origin: {'a': [1, {'b': True}], 'c': (None,)}

# Accessing nested Symbols
key_a = next(c for c in s.children if c.name == "a")
list_sym = key_a.children[0]
print(f"List Symbol: {list_sym.name}, Origin: {list_sym.origin}")
# Expected Output:
# List Symbol: list, Origin: [1, {'b': True}]

nested_dict_sym = list_sym.children[1]
print(f"Nested Dict Symbol: {nested_dict_sym.name}, Origin: {nested_dict_sym.origin}")
# Expected Output:
# Nested Dict Symbol: dict, Origin: {'b': True}

key_b = next(c for c in nested_dict_sym.children if c.name == "b")
print(f"Boolean Symbol: {key_b.children[0].name}, Origin: {key_b.children[0].origin}")
# Expected Output:
# Boolean Symbol: True, Origin: True
```
