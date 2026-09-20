Feature: OnniProject_AM25R1_Automation - Application Authentication Tests

  Background:
    Given user is on the login page

  #@smoke @Login
  Scenario: Login to application, verify home page URL and logout - Scenario 1
    When user enters credentials
    And user clicks login button
    Then user should be logged in successfully
    And user should verify the home page URL
    When user clicks logout button
    Then user should be logged out

      @smoke @Login
  Scenario: Login to application, verify home page URL and logout - Scenario 2
    When user enters credentials
    And user clicks login button
#    Then user should be logged in successfully
#    And user should verify the home page URL
#    When user clicks logout button
#    Then user should be logged out

          @smoke @Login
  Scenario: Login to application, verify home page URL and logout - scenario 3
    When user enters credentials
#    And user clicks login button
#    Then user should be logged in successfully
#    And user should verify the home page URL
#    When user clicks logout button
#    Then user should be logged out

