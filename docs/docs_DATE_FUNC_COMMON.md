# Date and Time Functionalities: `pendulum` vs. `datetime`

This document outlines common functionalities between `pendulum` and `datetime`, as well as functionalities unique to `datetime` that might need consideration for future `pendulum` integration or alternative approaches.

## Common Functionalities (`pendulum` and `datetime`)

Both `pendulum` and `datetime` provide robust capabilities for handling dates and times. Here are some of the core functionalities they share:

- **Object Instantiation:** Creating date/time objects from various inputs (e.g., year, month, day, hour, minute, second, microsecond).
- **Current Time:** Obtaining the current local or UTC time.
- **Timezone Awareness:** Handling timezones, including conversion between timezones.
- **Arithmetic Operations:** Adding or subtracting time durations (e.g., days, hours, minutes).
- **Comparison:** Comparing date/time objects (e.g., `>, <, ==, >=, <=`).
- **Formatting:** Converting date/time objects to string representations using format codes (e.g., `strftime`).
- **Parsing:** Converting string representations to date/time objects (e.g., `strptime`).
- **Accessing Components:** Retrieving individual components like year, month, day, hour, minute, second, weekday.
- **Timestamps:** Converting to and from Unix timestamps.

## `datetime`-Specific Functionalities (and `pendulum` equivalents/considerations)

While `pendulum` aims to be a drop-in replacement for `datetime` in many scenarios, there might be subtle differences or functionalities where `datetime` offers a direct method that `pendulum` handles differently or requires a slightly different approach.

- **`datetime.timedelta`:** `pendulum` uses its own `pendulum.Duration` and `pendulum.Period` objects for time differences, which are generally more powerful and intuitive. Direct `timedelta` objects might need conversion or re-evaluation when migrating.
- **`datetime.tzinfo`:** `pendulum` has a more integrated and simplified approach to timezones, often making direct manipulation of `tzinfo` objects less necessary.
- **`datetime.date` and `datetime.time`:** `pendulum` primarily operates with `DateTime` objects that encapsulate both date and time. While `pendulum` can extract date and time components, direct `date` or `time` objects from `datetime` might require explicit conversion or handling if strict type adherence is necessary.
- **`datetime.datetime.fromtimestamp()` with `tz` argument:** `pendulum` handles timezone conversion during timestamp creation more seamlessly, often inferring or allowing explicit timezone specification without a separate `tz` argument in `fromtimestamp`.
- **`datetime.datetime.utcfromtimestamp()`:** `pendulum`'s `from_timestamp()` method can be used with `tz='UTC'` to achieve the same effect.
- **`datetime.datetime.fromordinal()`:** `pendulum` does not have a direct equivalent for creating a datetime object from a proleptic Gregorian ordinal. This might require a custom conversion function if this functionality is critical.
- **`datetime.datetime.isocalendar()`:** `pendulum` provides `week_of_year` and `day_of_week` properties that can be used to reconstruct the ISO calendar tuple.
- **`datetime.datetime.isoweekday()`:** `pendulum` has `day_of_week` which returns 1 for Monday, 7 for Sunday, similar to `isoweekday()`.
- **`datetime.datetime.toordinal()`:** `pendulum` does not have a direct equivalent. This might require a custom conversion function if this functionality is critical.
- **`datetime.datetime.utctimetuple()`:** `pendulum` objects can be converted to `datetime` objects using `.in_timezone('UTC')._datetime` and then `utctimetuple()` can be called.
- **`datetime.datetime.dst()` and `datetime.datetime.tzname()`:** `pendulum` handles DST and timezone names internally. While these properties exist on the underlying `datetime` object, direct access might not be idiomatic `pendulum` usage.
