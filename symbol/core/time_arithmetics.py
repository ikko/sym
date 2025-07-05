"""This module provides functions for performing arithmetic operations on time-related objects.

It supports addition and subtraction of pendulum.DateTime and pendulum.Duration objects,
providing a convenient way to manipulate time-based data.
"""
import pendulum
from typing import Union

def add_time_objects(obj1: Union[pendulum.DateTime, pendulum.Duration], obj2: Union[pendulum.DateTime, pendulum.Duration]) -> Union[pendulum.DateTime, pendulum.Duration]:
    """Adds two time-related objects (DateTime or Duration)."""
    if isinstance(obj1, pendulum.DateTime) and isinstance(obj2, pendulum.Duration):
        return obj1 + obj2
    elif isinstance(obj1, pendulum.Duration) and isinstance(obj2, pendulum.DateTime):
        return obj2 + obj1
    elif isinstance(obj1, pendulum.Duration) and isinstance(obj2, pendulum.Duration):
        return obj1 + obj2
    else:
        raise TypeError(f"Unsupported operand types for +: {type(obj1)} and {type(obj2)}")

def subtract_time_objects(obj1: Union[pendulum.DateTime, pendulum.Duration], obj2: Union[pendulum.DateTime, pendulum.Duration]) -> Union[pendulum.DateTime, pendulum.Duration]:
    """Subtracts two time-related objects (DateTime or Duration)."""
    if isinstance(obj1, pendulum.DateTime) and isinstance(obj2, pendulum.Duration):
        return obj1 - obj2
    elif isinstance(obj1, pendulum.DateTime) and isinstance(obj2, pendulum.DateTime):
        return obj1 - obj2
    elif isinstance(obj1, pendulum.Duration) and isinstance(obj2, pendulum.Duration):
        return obj1 - obj2
    else:
        raise TypeError(f"Unsupported operand types for -: {type(obj1)} and {type(obj2)}")

# More arithmetic operations (multiplication, division, etc.) can be added here as needed.