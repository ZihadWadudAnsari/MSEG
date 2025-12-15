# MSEG Test Plan - Completed
## Manchester Stock Exchange System - Test Results

---

## 6.1 Test Plan

| Number | Task Name | Test Date | Tested By | Expected Results |
|--------|-----------|-----------|-----------|------------------|
| FR1 | View queue of pending applications | 21/11/2025 | Tester | Pending applications list displays correctly. |
| FR2 | Approve valid application | 21/11/2025 | Tester | Application status updates to approved and listing is created. |
| FR3 | Reject application with reason | 21/11/2025 | Tester | Application is rejected and reason is stored. |
| FR4 | Run integrity check on submission | 21/11/2025 | Tester | Missing fields, duplicate tickers, and odd valuations are flagged. |
| FR5 | Perform regulatory compliance review | 21/11/2025 | Tester | Compliance results show pass or specific rule failures. |
| FR6 | Remove stock listing | 21/11/2025 | Tester | Listing is marked removed and no longer appears as active. |
| FR7 | View and filter active listings | 21/11/2025 | Tester | Listings load with working sort and filters. |
| FR8 | Select multiple stocks for analysis | 21/11/2025 | Tester | Multiple selections are accepted for one analysis run. |
| FR9 | Show time-framed returns (1M/3M/6M) | 21/11/2025 | Tester | Returns display for each chosen period correctly. |
| FR10 | Valuation comparison table | 21/11/2025 | Tester | Table shows current values and growth per stock. |
| FR11 | Sector benchmarking | 21/11/2025 | Tester | Stock return is compared against its sector average. |
| FR12 | Performance consistency score | 21/11/2025 | Tester | Score is calculated and shown per stock. |
| NR1 | Privacy controls in data storage | 21/11/2025 | Tester | Only required personal/company data is stored. |
| NR3 | Performance of core screens | 21/11/2025 | Tester | Listings and review screens load within two seconds. |
| NR4 | Usable, accessible interfaces | 21/11/2025 | Tester | Labels, filters, and tables are clear and accessible. |

---

## 6.2 Test Cases

### Test Case TC1: View List of Approved/Pending/Rejected Applications

**Test Plan ID**: FR1
**Test Case No**: TC1
**Test Description**: Retrieve all Approved, Pending and Rejected Applications.

**Test Case Procedure**:
1. Login as Stock Manager.
2. Select Application portal, this calls applications_pending_all(), applications_approved_all() and applications_rejected_all().
3. Verify returned list contains all correct status applications.

**Test Data**: Username: manager1, Password: pass123
**Expected Result**: Function returns list of tuples containing applications with status='pending', 'approved' and 'rejected'.
**Actual Result**: All applications are under correct status list.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC2: Approve Valid Application (Status Update)

**Test Plan ID**: FR2
**Test Case No**: TC2
**Test Description**: Verify application status changes to 'Approved' in database.

**Test Case Procedure**:
1. Login as a Company.
2. Submit test application with status='pending'.
3. Login as Stock Manager.
4. Approve that test application.
5. Verify status is set to 'approved' status on company application portal.

**Test Data**: Company Username: Crusties, Company Password: Pass1234, Manager Username: manager1, Manager Password: pass123.
**Expected Result**: Application status in portal is updated to 'approved'
**Actual Result**: Crusties application status is updated to 'Approved'.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC3: Approve Valid Application (Stock Creation)

**Test Plan ID**: FR2
**Test Case No**: TC3
**Test Description**: Verify stock is created when application is approved

**Test Case Procedure**:
1. Login as a Stock Manager.
2. Approve a Stock.
3. Verify new stock has been created on stock market page.

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: New stock record created from application onto the stock market page
**Actual Result**: Crusties stock created and listed on stock market.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC4: Reject Application with Reasons

**Test Plan ID**: FR3
**Test Case No**: TC4
**Test Description**: Verify application status changes to 'rejected' with notes.

**Test Case Procedure**:
1. Login as a Stock Manager.
2. Reject Application & Input Rejection Note.
3. Login as Company.
4. Verify application to verify status='rejected' and rejection notes are present.

**Test Data**: Manager Username: manager1, Manager Password: pass123, Company Username: aps, Company Password: Pass1234
**Expected Result**: Application status='rejected' and contains rejection reason submitted by the stock manager.
**Actual Result**: APS Application status set to "rejected" and includes rejection note.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC5: Reject Application Without Reason

**Test Plan ID**: FR3
**Test Case No**: TC5
**Test Description**: Verify rejection fails without reason.

**Test Case Procedure**:
1. Login as a Stock Manager.
2. Attempt to reject pending application.
3. Leave reason field empty.

**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Result**: System shows error: 'Please provide a rejection note.' Status remains 'pending'.
**Actual Result**: Error Message was displayed & Status remained 'Pending'.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC6: Integrity Check - Ticker Format Validation

**Test Plan ID**: FR4
**Test Case No**: TC6
**Test Description**: Verify ticker must be 3-4 capital letters only

**Test Case Procedure**:
1. Login on Company Account.
2. Select New Application.
3. Test invalid tickers: "AB" (too short), "ABCDE" (too long), "ab12" (lowercase/numbers).
4. Verify validation function rejects these inputs.

**Test Data**: Company Username: company1, Company Password: pass456
**Expected Result**: With each instance, the error ticker message would be displayed.
**Actual Result**: On all three Invalid tickers instances, the error ticker message displayed; "Proposed Ticker must be 3 to 4 capital LETTERS only"
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC7: Integrity Check - Duplicate Ticker Prevention

**Test Plan ID**: FR4
**Test Case No**: TC7
**Test Description**: Verify system prevents duplicate ticker symbols.

**Test Case Procedure**:
1. Login on Company Account.
2. Select New Application.
3. Create Stock with ticker "NVDA".
4. Attempt to create application with same ticker "NVDA".

**Test Data**: Company Username: company1, Company Password: pass456, Proposed Ticker: NVDA
**Expected Result**: An error message would be displayed about ticker being in used already.
**Actual Result**: Error Message displayed; "The ticker symbol 'NVDA' is already listed in the stock market. Please choose a different ticker."
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC8: Integrity Check - Minimum Valuation

**Test Plan ID**: FR4
**Test Case No**: TC8
**Test Description**: Verify valuation must be a minimum of at least 100 million.

**Test Case Procedure**:
1. Login on Company Account.
2. Select New Application.
3. Enter valuation of 50,000,000.
4. Attempt to submit application.

**Test Data**: Company Username: company1, Company Password: pass456, Proposed Valuation: 50000000
**Expected Result**: An error message would be displayed that a minimum 100 million valuation is required.
**Actual Result**: Error Message displayed; "The proposed valuation is below 100 million. This does not meet the minimum MSEG listing requirements"
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC9: Integrity Check - Maximum Valuation

**Test Plan ID**: FR4
**Test Case No**: TC9
**Test Description**: Verify valuation cannot exceed 500 billion.

**Test Case Procedure**:
1. Login on Company Account.
2. Select New Application.
3. Enter valuation of 600,000,000,000.
4. Attempt to submit application.

**Test Data**: Company Username: company1, Company Password: pass456, Proposed Valuation: 600000000000
**Expected Result**: An error message would be displayed that a valuation cannot exceed 500 billion.
**Actual Result**: Error Message displayed; "The proposed valuation exceeds 500 billion. This valuation appears to be inflated and does not meet MSEG listing requirements."
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC10: Integrity Check - Required Fields

**Test Plan ID**: FR4
**Test Case No**: TC10
**Test Description**: Verify all required inputs and attachments are provided.

**Test Case Procedure**:
1. Login on Company Account.
2. Select New Application.
3. Attempt to submit application with one or more fields empty.

**Test Data**: Company Username: company1, Company Password: pass456
**Expected Result**: An error message would be displayed that all fields must be filled.
**Actual Result**: Error Messages "Please upload legal, financial, and corporate governance documents.", "Please input Proposed Shares.", "Please input Proposed Ticker." and "Please upload legal, financial, and corporate governance documents." displayed.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC11: Regulatory Compliance - Minimum Incorporation Age

**Test Plan ID**: FR5
**Test Case No**: TC11
**Test Description**: Verify company must be incorporated for at least 3 years

**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option.
2. Enter incorporation date less than 3 years ago.
3. Attempt to submit registration.

**Test Data**: Incorporation Date: 2024-01-01
**Expected Result**: An error message would be displayed that the company must be incorporated at least 3 years ago.
**Actual Result**: Error message displayed; "The company does not meet the minimum age requirement for MSEG listing. Companies must be incorporated for at least 3 years to comply with MSEG regulatory standards."
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC12: Regulatory Compliance - Duplicate Registration Number

**Test Plan ID**: FR5
**Test Case No**: TC12
**Test Description**: Verify duplicate registration numbers are prevented

**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option.
2. Enter company with registration number "12345678".
3. Attempt to submit another company with same registration number.

**Test Data**: Company Name: Crusties, Registration No: 12237364
**Expected Result**: There should be an error message generated that the registration number already exists.
**Actual Result**: Error Message displayed; "That registration number already exists"
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC13: Regulatory Compliance - Companies House Verification

**Test Plan ID**: FR5
**Test Case No**: TC13
**Test Description**: Verify system only approves companies that exists in Companies House registry

**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option.
2. Verify function returns False for invalid company.
3. Submit valid company name from Companies House registry.

**Test Data**: Company Name: test, Registration No: 00000000 | Company Name: Crusties, Registration No: 12237364
**Expected Result**: Company account has been created and added onto the users text file.
**Actual Result**: Crusties account creation successful and add to the users.txt file.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC14: Regulatory Compliance - Date Format Validation

**Test Plan ID**: FR5
**Test Case No**: TC14
**Test Description**: Verify incorporation date must be in YYYY-MM-DD format

**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option.
2. Enter invalid date formats.
3. Attempt to submit registration with each invalid format.

**Test Data**: Invalid Date formats: "01/01/2020", "2020-1-1", "50-01-2020"
**Expected Result**: There should be an error message generated that the date format is incorrect.
**Actual Result**: Error Message Displayed
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC15: Regulatory Compliance - Date Range Validation

**Test Plan ID**: FR5
**Test Case No**: TC15
**Test Description**: Verify incorporation date must be between 1850 and today

**Test Case Procedure**:
1. Login on Company Account.
2. Enter dates above and below the valid range years.
3. Attempt to submit registration with both invalid years.

**Test Data**: Out of range dates; "1-1-1800" and "1-1-2300"
**Expected Result**: There should be an error message generated that the incorporation date is invalid.
**Actual Result**: Error Message Displayed
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC16: Remove Stock Listing

**Test Plan ID**: FR6
**Test Case No**: TC16
**Test Description**: Verify stock are deleted from the stock market.

**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page and select a stock to delete
3. Attempt to delete stock with the 'Delete' function

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: The stock would be deleted from the stock market page.
**Actual Result**: The NVDA stock is deleted from the stock market page with the confirmation message of "Selected stocks deleted".
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC17: View All Active Stock Listings

**Test Plan ID**: FR7
**Test Case No**: TC17
**Test Description**: Verify only accepted stocks are on the stock market.

**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page to view all stocks
3. Verify these are only stocks that are accepted

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: Stocks that are accepted are on the stock market page.
**Actual Result**: All accepted stocks appear on the stock market page.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC18: Select Stocks for Analysis

**Test Plan ID**: FR8
**Test Case No**: TC18
**Test Description**: Verify multiple stocks can be selected for analysis

**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page to select more than one stocks.
3. Attempt to select Stock Analysis function

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: Stock Analysis tab option should be presented to the user.
**Actual Result**: New Tab "Select Analysis Type" for the selected stocks is presented.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC19: Display Time-Framed Returns

**Test Plan ID**: FR9
**Test Case No**: TC19
**Test Description**: Verify stocks are accepted onto the stock market with market data

**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Application Page, to accept company
3. Verify on Stock Market Page that company is displayed with relevant time-framed returns

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: The accepted company displays all the relevant time framed returns.
**Actual Result**: The NVDA and Crusties company displays the three different time framed returns on a separate tab.
**Pass/Fail**: PASS
**Screenshot**: Figure 18. Manchester Stock Exchange System Application – Time-Framed Returns Analysis Output

---

### Test Case TC20: Valuation Comparison Table

**Test Plan ID**: FR10
**Test Case No**: TC20
**Test Description**: Verify multiple stocks can be selected for analysis

**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page to select stocks for valuation comparison analysis
3. Attempt to conduct the valuation comparison analysis.

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: A new tab of the valuation comparison table of the two stocks should be presented.
**Actual Result**: New tab of NVDA and Crusties stock valuation comparison table is presented.
**Pass/Fail**: PASS
**Screenshot**: Available at Figure 20. Manchester Stock Exchange System Application – Valuation Comparison Analysis Output

---

### Test Case TC21: Sector Benchmarking

**Test Plan ID**: FR11
**Test Case No**: TC21
**Test Description**: Verify multiple stocks can be selected for analysis

**Test Case Procedure**:
1. Login as Stock Manager.
2. Navigate to Stock Market page to select stocks for sector benchmarking analysis.
3. Attempt to conduct the sector benchmarking analysis.

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: A new tab of the sector benchmarking analysis of the two stocks should be presented.
**Actual Result**: New tab of NVDA and Crusties of sector benchmarking analysis is presented.
**Pass/Fail**: PASS
**Screenshot**: Available at Figure 22. Manchester Stock Exchange System Application – Sector Benchmarking Analysis Output

---

### Test Case TC22: Performance Consistency Score

**Test Plan ID**: FR12
**Test Case No**: TC22
**Test Description**: Verify multiple stocks can be selected for analysis

**Test Case Procedure**:
1. Login as Stock Manager.
2. Navigate to Stock Market page to select stocks for performance consistency score analysis.
3. Attempt to conduct the performance consistency score analysis.

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: A new tab of the performance consistency score for the two stocks should be presented.
**Actual Result**: New tab of NVDA and Crusties of performance consistency score analysis is presented.
**Pass/Fail**: PASS
**Screenshot**: Available at Figure 24. Manchester Stock Exchange System Application – Performance Consistency Analysis Output

---

### Test Case TC23: Privacy Controls - Password Encryption

**Test Plan ID**: NR1
**Test Case No**: TC23
**Test Description**: Verify that passwords are encrypted when stored.

**Test Case Procedure**:
1. Create a Company Account
2. Verify the password is encrypted by navigating to the Application users file data file.

**Test Data**: Company Username: crusties, Company password: Test1234.
**Expected Result**: The password under the data file should be encrypted.
**Actual Result**: The password for Crusties company in the users.txt file was encrypted.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC24: Performance of Core Screens

**Test Plan ID**: NR3
**Test Case No**: TC24
**Test Description**: Verify multiple stocks can be selected for analysis

**Test Case Procedure**:
1. Login as Stock Manager.
2. Verify both main two pages loads under two seconds by navigating to the Application & Stock Market page

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: Both main pages would load under two seconds upon selecting on them.
**Actual Result**: Application and Stock Market page both loads up with all information immediately upon selecting them.
**Pass/Fail**: PASS
**Screenshot**: Available

---

### Test Case TC25: Accessible Interface - Dark Mode

**Test Plan ID**: NR4
**Test Case No**: TC25
**Test Description**: Verify dark mode works when function selected.

**Test Case Procedure**:
1. Select the "Dark Mode" function
2. Verify this works across all pages by navigating through different Pages

**Test Data**: Manager Username: manager1, Manager Password: pass123.
**Expected Result**: The entire page would go dark mode and includes other pages within the application.
**Actual Result**: The login, application and stock market page can be in dark mode.
**Pass/Fail**: PASS
**Screenshot**: Available

---

## Test Summary

**Total Test Cases Executed**: 25
**Passed**: 25
**Failed**: 0
**Pass Rate**: 100%

### Test Coverage by Requirement:

| Requirement | Test Cases | Status |
|-------------|------------|--------|
| FR1 - View pending applications | TC1 | PASS |
| FR2 - Approve applications | TC2, TC3 | PASS |
| FR3 - Reject applications | TC4, TC5 | PASS |
| FR4 - Integrity checks | TC6, TC7, TC8, TC9, TC10 | PASS |
| FR5 - Regulatory compliance | TC11, TC12, TC13, TC14, TC15 | PASS |
| FR6 - Remove stock listing | TC16 | PASS |
| FR7 - View active listings | TC17 | PASS |
| FR8 - Select stocks for analysis | TC18 | PASS |
| FR9 - Time-framed returns | TC19 | PASS |
| FR10 - Valuation comparison | TC20 | PASS |
| FR11 - Sector benchmarking | TC21 | PASS |
| FR12 - Performance consistency | TC22 | PASS |
| NR1 - Privacy controls | TC23 | PASS |
| NR3 - Performance | TC24 | PASS |
| NR4 - Accessibility | TC25 | PASS |

---

**Test Date**: 21/11/2025
**Tested By**: Tester
**Status**: All tests completed successfully

---

*End of Test Plan*
