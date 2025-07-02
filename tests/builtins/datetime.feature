Feature: Symbol Datetime Functionality

  As a developer working with time-based data in Symbol
  I want to parse, access, and manipulate datetime information
  So that I can effectively manage temporal aspects of my symbolic systems

  Scenario: Parsing timestamps from Symbol names
    Given a Symbol with a valid ISO format datetime name (e.g., "2023-01-15T10:30:00")
    When the timestamp is parsed
    Then it should correctly convert to a datetime object with the specified date and time
    Given a Symbol with a valid ISO format date-only name (e.g., "2023-03-20")
    When the timestamp is parsed
    Then it should correctly convert to a datetime object with the specified date and time defaulting to midnight
    Given a Symbol with an invalid format name (e.g., "invalid-date")
    When the timestamp is parsed
    Then it should default to today's date with time set to midnight

  Scenario: Accessing datetime properties of a Symbol
    Given a Symbol named "2023-04-22T14:45:30"
    When its datetime properties are accessed
    Then its `as_date` property should return the correct date
    And its `as_time` property should return the correct time
    And its `as_datetime` property should return the correct full datetime
    And its `day` property should return the correct day
    And its `hour` property should return the correct hour
    And its `minute` property should return the correct minute
    And its `second` property should return the correct second
    Given a Symbol named "2023-05-01" (date-only)
    When its datetime properties are accessed
    Then its `as_date` property should return the correct date
    And its `as_time` property should return midnight
    And its `as_datetime` property should return the correct datetime with midnight time

  Scenario: Retrieving chronological head and tail views of Symbols
    Given multiple Symbols with distinct chronological timestamps (early, middle, late)
    When the `head` property is accessed on any of these Symbols
    Then a `SymbolHeadTailView` instance should be returned
    And iterating over this view should yield Symbols in chronological order (early to late)
    When the `tail` property is accessed on any of these Symbols
    Then a `SymbolHeadTailView` instance should be returned
    And iterating over this view should yield Symbols in reverse chronological order (late to early)

  Scenario: Calculating time periods between Symbols
    Given two Symbols representing a start and an end time (e.g., "2023-01-01T10:00:00" and "2023-01-01T11:30:00")
    When the `period`, `as_period`, `duration`, `as_duration`, `delta`, or `as_delta` properties are accessed
    Then they should all return the correct `timedelta` representing the duration between the start and end Symbols
    Given a single Symbol
    When its period properties are accessed
    Then they should return a `timedelta` of zero
