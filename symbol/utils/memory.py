import sys
import inspect
from typing import Dict, List, Any, Tuple

from ..core.base_symbol import Symbol as BaseSymbol
from ..core.symbol import Symbol

def get_object_size(obj: Any) -> int:
    """
    what: Recursively calculates the size of an object.
    why: To determine the memory footprint of complex Python objects.
    how: Uses BFS traversal, `sys.getsizeof`, and tracks visited objects.
    when: When memory usage analysis is needed.
    by (caller(s)): analyze_symbol_memory_and_methods.
    how often: Infrequently.
    how much: Depends on object graph complexity.
    what is it like: Measuring an object's total size.
    how, what, why and when to improve: Handle more complex object types, optimize performance.
    """
    marked = {id(obj)}
    total_size = 0

    # Add to queue for BFS traversal
    q = [obj]
    while q:
        current_obj = q.pop(0)
        total_size += sys.getsizeof(current_obj)

        # Add contents to queue
        if isinstance(current_obj, dict):
            for key, value in current_obj.items():
                if id(key) not in marked:
                    marked.add(id(key))
                    q.append(key)
                if id(value) not in marked:
                    marked.add(id(value))
                    q.append(value)
        elif isinstance(current_obj, (list, tuple, set, frozenset)):
            for item in current_obj:
                if id(item) not in marked:
                    marked.add(id(item))
                    q.append(item)
        elif hasattr(current_obj, '__dict__'):
            for attr_name, attr_value in current_obj.__dict__.items():
                if id(attr_value) not in marked:
                    marked.add(id(attr_value))
                    q.append(attr_value)
    return total_size

def get_public_methods_by_module(target_class: type) -> Dict[str, List[str]]:
    """
    what: Lists public methods of a class by module.
    why: To understand the origin of methods in a class.
    how: Iterates through `dir()`, inspects methods, gets module name.
    when: When analyzing class structure or debugging method origins.
    by (caller(s)): analyze_symbol_memory_and_methods.
    how often: Infrequently.
    how much: Depends on class complexity.
    what is it like: Mapping a class's capabilities.
    how, what, why and when to improve: Handle more method types, optimize for large classes.
    """
    methods_by_module: Dict[str, List[str]] = defaultdict(list)
    
    for name in dir(target_class):
        if not name.startswith('_'): # Public methods
            attr = getattr(target_class, name)
            if inspect.isfunction(attr) or inspect.ismethod(attr) or isinstance(attr, (staticmethod, classmethod, property)):
                # Try to get the original function if it's a static/class method or property
                if isinstance(attr, (staticmethod, classmethod)):
                    original_func = attr.__func__
                elif isinstance(attr, property):
                    original_func = attr.fget # Get the getter function
                else:
                    original_func = attr

                # Get the module name
                module_name = inspect.getmodule(original_func)
                if module_name:
                    module_name_str = module_name.__name__
                    methods_by_module[module_name_str].append(name)
                else:
                    methods_by_module["<unknown_module>"].append(name)
    
    # Sort methods within each module
    for module, methods in methods_by_module.items():
        methods_by_module[module] = sorted(list(set(methods))) # Use set to remove duplicates and then sort

    return dict(sorted(methods_by_module.items()))

def analyze_symbol_memory_and_methods(symbol_instance: Symbol) -> Tuple[int, Dict[str, List[str]]]:
    """
    what: Analyzes Symbol memory and lists public methods.
    why: To provide a comprehensive overview of a Symbol's runtime characteristics.
    how: Calls `get_object_size` and `get_public_methods_by_module`.
    when: When detailed Symbol analysis is needed.
    by (caller(s)): External analysis scripts.
    how often: Infrequently.
    how much: Depends on Symbol complexity.
    what is it like: Generating a diagnostic report.
    how, what, why and when to improve: Add more metrics, integrate with profiling tools.
    """
    memory_size = get_object_size(symbol_instance)
    public_methods = get_public_methods_by_module(symbol_instance.__class__)
    return memory_size, public_methods

def print_analysis_report(title: str, memory_size: int, public_methods: Dict[str, List[str]]):
    """
    what: Prints a formatted analysis report.
    why: To display memory and method analysis results clearly.
    how: Formats and prints memory size and grouped public methods.
    when: After analyzing a Symbol's memory and methods.
    by (caller(s)): External analysis scripts.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Presenting a summary.
    how, what, why and when to improve: More customizable formatting, export to file.
    """
    print(f"--- {title} ---")
    print(f"Memory Footprint: {memory_size} bytes")
    print("Public Methods (grouped by module):")
    if not public_methods:
        print("  (None)")
    else:
        for module, methods in public_methods.items():
            print(f"  {module}:")
            for method in methods:
                print(f"    - {method}")
    print("-" * (len(title) + 8))
    print()
