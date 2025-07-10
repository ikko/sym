"""This module provides functions for performing arithmetic operations on time-related objects.

It supports addition and subtraction of datetime.datetime and datetime.timedelta objects,
providing a convenient way to manipulate time-based data.
"""
import datetime
from typing import Union

def add_time_objects(obj1: Union[datetime.datetime, datetime.timedelta], obj2: Union[datetime.datetime, datetime.timedelta]) -> Union[datetime.datetime, datetime.timedelta]:
    """
    what: Adds two time-related objects.
    why: To perform arithmetic operations on datetime and timedelta.
    how: Handles combinations of datetime and timedelta types.
    when: When combining time durations or shifting datetimes.
    by (caller(s)): External code.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Adding time values.
    how, what, why and when to improve: Handle more complex time objects.
    """
    if isinstance(obj1, datetime.datetime) and isinstance(obj2, datetime.timedelta):
        return obj1 + obj2
    elif isinstance(obj1, datetime.timedelta) and isinstance(obj2, datetime.datetime):
        return obj2 + obj1
    elif isinstance(obj1, datetime.timedelta) and isinstance(obj2, datetime.timedelta):
        return obj1 + obj2
    else:
        raise TypeError(f"Unsupported operand types for +: {type(obj1)} and {type(obj2)}")

def subtract_time_objects(obj1: Union[datetime.datetime, datetime.timedelta], obj2: Union[datetime.datetime, datetime.timedelta]) -> Union[datetime.datetime, datetime.timedelta]:
    """
    what: Subtracts two time-related objects.
    why: To perform arithmetic operations on datetime and timedelta.
    how: Handles combinations of datetime and timedelta types.
    when: When calculating time differences or shifting datetimes.
    by (caller(s)): External code.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Subtracting time values.
    how, what, why and when to improve: Handle more complex time objects.
    """
    if isinstance(obj1, datetime.datetime) and isinstance(obj2, datetime.timedelta):
        return obj1 - obj2
    elif isinstance(obj1, datetime.datetime) and isinstance(obj2, datetime.datetime):
        return obj1 - obj2
    elif isinstance(obj1, datetime.timedelta) and isinstance(obj2, datetime.timedelta):
        return obj1 - obj2
    else:
        raise TypeError(f"Unsupported operand types for -: {type(obj1)} and {type(obj2)}")

# More arithmetic operations (multiplication, division, etc.) can be added here as needed.