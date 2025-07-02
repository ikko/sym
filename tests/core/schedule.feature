Feature: Scheduler Functionality

  As a developer using the Symbol library's scheduling capabilities
  I want to ensure the scheduler can be instantiated
  So that I can utilize it for managing time-based operations

  Scenario: Scheduler instantiation
    Given the Scheduler class is available
    When a new instance of Scheduler is created
    Then the scheduler object should not be null
