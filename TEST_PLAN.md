# MSEG Test Plan
## Manchester Stock Exchange System - Comprehensive Test Cases

---

## FUNCTIONAL REQUIREMENTS TESTING

### FR1: View Queue of Pending Applications

#### TC1: Retrieve All Pending Applications (Unit Test)
**Test Case ID**: FR1-TC1
**Test Case Description**: Retrieve all Approved, Pending and Rejected Applications.
**Test Case Procedure**:
1. Login as Stock Manager
2. Select Application portal, this calls applications_pending_all(), applications_approved_all() and applications_rejected_all().
3. Verify returned list contains all correct status applications.
**Test Data**: Username: manager1, Password: pass123
**Expected Output**: Function returns list of tuples containing applications with status='pending', 'approved' and 'rejected'.
**Actual Result**: All applications are under correct status list.
**Pass/Fail**: PASS

---

#### TC27: End-to-End Application Submission and Approval (Integration Test)
**Test Case ID**: FR1-FR2-INT-TC27
**Test Case Description**: Verify complete workflow from submission to approval
**Test Case Procedure**:
1. Login as Company
2. Navigate to My Applications
3. Create New Application with all required fields and attachments
4. Submit application
5. Verify success message appears
6. Logout and Login as Stock Manager
7. Navigate to Manager Portal
8. Verify application appears in Pending list
9. Select application and click "Approve"
10. Verify application moves to Approved list
11. Navigate to Stock Market
12. Verify new stock appears in listing
**Test Data**: Company Username: company1, Company Password: pass456; Manager Username: manager1, Manager Password: pass123
**Expected Output**: Application successfully moves through workflow from submission to approval, creating new stock listing
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC42: Company Submits Application - Manager Approves - Stock Appears (System Test)
**Test Case ID**: FR1-FR2-SYS-TC42
**Test Case Description**: End-to-end system test of successful application flow
**Test Case Procedure**:
1. Launch MSEG application
2. Click "Sign Up" as Company
3. Fill all registration fields:
   - Company Name, Registration Number, Username, Password, Incorporation Date
4. Submit registration
5. Login with new credentials
6. Navigate to My Applications
7. Create New Application with:
   - Proposed Ticker (3-4 capital letters)
   - Proposed Shares (positive number)
   - Proposed Valuation (100M - 500B)
   - Select Sector
8. Attach at least one document
9. Submit application
10. Verify success message appears
11. Logout and Login as Stock Manager
12. Navigate to Manager Portal
13. Verify application appears in Pending list
14. Click on application to view details
15. Click "Approve" button
16. Verify application moves to Approved list
17. Navigate to Stock Market page
18. Verify new stock appears in listing with all data
19. Verify return percentages (24hr, 1M, 6M, 1Y) are displayed
20. Logout and login as Company
21. Navigate to Stock Market
22. Verify stock is visible
**Test Data**: New Company: Registration No (8 digits), Username (unique), Password, Incorporation Date (at least 3 years ago); Manager Username: manager1, Manager Password: pass123
**Expected Output**: Complete workflow from registration → application → approval → stock listing succeeds
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR2: Approve Valid Application

#### TC2: Application Approval Status Update (Unit Test)
**Test Case ID**: FR2-TC2
**Test Case Description**: Verify application status changes to 'Approved' in database.
**Test Case Procedure**:
1. Login as a Company
2. Submit test application with status='pending'
3. Login as Stock Manager
4. Approve that test application
5. Verify status is set to 'approved' status on company application portal
**Test Data**: Company Username: Crusties, Company Password: Pass1234, Manager Username: manager1, Manager Password: pass123
**Expected Output**: Application status in portal is updated to 'approved'
**Actual Result**: Crusties application status is updated to 'Approved'.
**Pass/Fail**: PASS

---

#### TC3: Stock Creation from Approved Application (Unit Test)
**Test Case ID**: FR2-TC3
**Test Case Description**: Verify stock is created when application is approved
**Test Case Procedure**:
1. Login as a Stock Manager.
2. Approve a Stock.
3. Verify new stock has been created on stock market page.
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: New stock record created from application onto the stock market page
**Actual Result**: Crusties stock created and listed on stock market.
**Pass/Fail**: PASS

---

#### TC4: Stock Price History Generation (Unit Test)
**Test Case ID**: FR2-TC4
**Test Case Description**: Verify 366 days of price history is generated for new stock
**Test Case Procedure**:
1. Login as Stock Manager
2. Approve an application to create a new stock
3. Navigate to Stock Market page
4. Verify stock displays with price history data (24hr, 1M, 6M, 1Y returns)
5. Verify prices show realistic variation
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Stock displays with complete price history showing returns for all time periods
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR3: Reject Application with Reasons

#### TC5: Application Rejection Status Update (Unit Test)
**Test Case ID**: FR3-TC5
**Test Case Description**: Verify application status changes to 'rejected' with notes.
**Test Case Procedure**:
1. Login as a Stock Manager
2. Reject Application & Input Rejection Note
3. Login as Company
4. Verify application to verify status='rejected' and rejection notes are present
**Test Data**: Manager Username: manager1, Manager Password: pass123, Company Username: aps, Company Password: Pass1234
**Expected Output**: Application status='rejected' and contains rejection reason submitted by the stock manager.
**Actual Result**: APS Application status set to "rejected" and includes rejection note.
**Pass/Fail**: PASS

---

#### TC6: Rejection Fails Without Reason (Unit Test)
**Test Case ID**: FR3-TC6
**Test Case Description**: Verify rejection fails without reason.
**Test Case Procedure**:
1. Login as a Stock Manager
2. Attempt to reject pending application
3. Leave reason field empty.
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: System shows error: 'Please provide a rejection note.' Status remains 'pending'.
**Actual Result**: Error Message was displayed & Status remained 'Pending'.
**Pass/Fail**: PASS

---

#### TC28: End-to-End Application Submission and Rejection (Integration Test)
**Test Case ID**: FR1-FR3-INT-TC28
**Test Case Description**: Verify complete workflow from submission to rejection with notes
**Test Case Procedure**:
1. Login as Company
2. Navigate to My Applications
3. Create and submit new application with all required data
4. Logout and Login as Stock Manager
5. Navigate to Manager Portal
6. Verify application appears in Pending list
7. Select application and click "Reject"
8. Enter rejection notes in text box
9. Save rejection
10. Verify application moves to Rejected list
11. Logout and Login as Company
12. Verify application shows rejected status with rejection notes
**Test Data**: Company Username: company1, Company Password: pass456; Manager Username: manager1, Manager Password: pass123
**Expected Output**: Application successfully rejected with notes visible to both manager and company
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC43: Company Submits Application - Manager Rejects - No Stock Created (System Test)
**Test Case ID**: FR1-FR3-SYS-TC43
**Test Case Description**: End-to-end system test of application rejection flow
**Test Case Procedure**:
1. Launch MSEG application
2. Login as Company
3. Navigate to My Applications
4. Submit new application with all required data
5. Logout and Login as Stock Manager
6. Navigate to Manager Portal
7. Select application from Pending list
8. Click "Reject" button
9. Enter rejection reason in notes field
10. Save rejection
11. Verify application moves to Rejected list
12. Navigate to Stock Market page
13. Verify rejected application's ticker does NOT appear in stock listing
14. Logout and Login as Company
15. Navigate to My Applications
16. Verify application shows rejected status
17. View rejection notes
**Test Data**: Company Username: company1, Company Password: pass456; Manager Username: manager1, Manager Password: pass123
**Expected Output**: Rejected application does not create stock, rejection notes are visible to company
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR4: Integrity Check (Missing Fields, Duplicates, Unrealistic Valuations)

#### TC6: Ticker Format Validation (Unit Test)
**Test Case ID**: FR4-TC6
**Test Case Description**: Verify ticker must be 3-4 capital letters only
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Test invalid tickers: "AB" (too short), "ABCDE" (too long), "ab12" (lowercase/numbers)
4. Verify validation function rejects these inputs
**Test Data**: Company Username: company1, Company Password: pass456
**Expected Output**: With each instance, the error ticker message would be displayed.
**Actual Result**: On all three Invalid tickers instances, the error ticker message displayed; "Proposed Ticker must be 3 to 4 capital LETTERS only"
**Pass/Fail**: PASS

---

#### TC7: Duplicate Ticker Prevention (Unit Test)
**Test Case ID**: FR4-TC7
**Test Case Description**: Verify system prevents duplicate ticker symbols.
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Create Stock with ticker "NVDA"
4. Attempt to create application with same ticker "NVDA"
**Test Data**: Company Username: company1, Company Password: pass456, Proposed Ticker: NVDA
**Expected Output**: An error message would be displayed about ticker being in used already.
**Actual Result**: Error Message displayed; "The ticker symbol 'NVDA' is already listed in the stock market. Please choose a different ticker."
**Pass/Fail**: PASS

---

#### TC8: Valuation Lower Bound Check (Unit Test)
**Test Case ID**: FR4-TC8
**Test Case Description**: Verify valuation must be a minimum of at least 100 million.
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Enter valuation of 50,000,000
4. Attempt to submit application
**Test Data**: Company Username: company1, Company Password: pass456, Proposed Valuation: 50000000
**Expected Output**: An error message would be displayed that a minimum 100 million valuation is required.
**Actual Result**: Error Message displayed; "The proposed valuation is below 100 million. This does not meet the minimum MSEG listing requirements"
**Pass/Fail**: PASS

---

#### TC9: Valuation Upper Bound Check (Unit Test)
**Test Case ID**: FR4-TC9
**Test Case Description**: Verify valuation cannot exceed 500 billion.
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Enter valuation of 600,000,000,000
4. Attempt to submit application
**Test Data**: Company Username: company1, Company Password: pass456, Proposed Valuation: 600000000000
**Expected Output**: An error message would be displayed that a valuation cannot exceed 500 billion.
**Actual Result**: Error Message displayed; "The proposed valuation exceeds 500 billion. This valuation appears to be inflated and does not meet MSEG listing requirements."
**Pass/Fail**: PASS

---

#### TC10: Missing Required Fields (Unit Test)
**Test Case ID**: FR4-TC10
**Test Case Description**: Verify all required inputs and attachments are provided.
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Attempt to submit application with one or more fields empty.
**Test Data**: Company Username: company1, Company Password: pass456
**Expected Output**: An error message would be displayed that all fields must be filled.
**Actual Result**: Error Messages "Please upload legal, financial, and corporate governance documents.", "Please input Proposed Shares.", "Please input Proposed Ticker." and "Please upload legal, financial, and corporate governance documents." displayed.
**Pass/Fail**: PASS

---

#### TC11: Attachment Requirement (Unit Test)
**Test Case ID**: FR4-TC11
**Test Case Description**: Verify at least one attachment is required
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Fill all fields but do not attach any documents
4. Attempt to submit application
**Test Data**: Company Username: company1, Company Password: pass456
**Expected Output**: Error message about missing attachments would be displayed
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC30: Attachment Storage and Retrieval (Integration Test)
**Test Case ID**: FR4-INT-TC30
**Test Case Description**: Verify documents attached to applications are stored and retrievable
**Test Case Procedure**:
1. Login as Company
2. Navigate to My Applications
3. Create New Application and attach PDF file
4. Submit application
5. Logout and Login as Stock Manager
6. Navigate to Manager Portal
7. Select the application
8. View application details
9. Verify attachments are listed
10. Click "Open" button to view attachment
11. Verify file opens correctly
**Test Data**: Company Username: company1, Company Password: pass456; Manager Username: manager1, Manager Password: pass123
**Expected Output**: Attachments are stored and viewable by manager from application details
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC44: Duplicate Ticker Submission Blocked (System Test)
**Test Case ID**: FR4-SYS-TC44
**Test Case Description**: Verify system prevents duplicate ticker at submission time
**Test Case Procedure**:
1. Login as Company
2. Navigate to My Applications
3. Create New Application with ticker that already exists in stock market (e.g., "AAPL")
4. Attempt to submit application
5. Verify error message about duplicate ticker is displayed
6. Change ticker to unique value
7. Submit application successfully
**Test Data**: Company Username: company1, Company Password: pass456; Duplicate Ticker: existing ticker; Unique Ticker: new ticker
**Expected Output**: Duplicate ticker rejected with error message, unique ticker accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC45: Unrealistic Valuation Blocked (System Test)
**Test Case ID**: FR4-SYS-TC45
**Test Case Description**: Verify valuations outside 100M-500B range are rejected
**Test Case Procedure**:
1. Login as Company
2. Navigate to My Applications
3. Create New Application with valuation 50,000,000 (50M - too low)
4. Attempt to submit
5. Verify error message about minimum 100 million requirement
6. Change valuation to 600,000,000,000 (600B - too high)
7. Attempt to submit
8. Verify error message about maximum 500 billion limit
9. Change valuation to 250,000,000 (250M - valid)
10. Submit successfully
**Test Data**: Company Username: company1, Company Password: pass456; Invalid Valuations: 50000000, 600000000000; Valid Valuation: 250000000
**Expected Output**: Out-of-range valuations rejected with error messages, valid valuation accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR5: Regulatory Compliance Review

#### TC12: Company Incorporation Date Validation (Unit Test)
**Test Case ID**: FR5-TC12
**Test Case Description**: Verify company must be incorporated for at least 3 years
**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option
2. Enter incorporation date less than 3 years ago
3. Attempt to submit registration
**Test Data**: Incorporation Date: 2024-01-01
**Expected Output**: An error message would be displayed that the company must be incorporated at least 3 years ago.
**Actual Result**: Error message displayed; "The company does not meet the minimum age requirement for MSEG listing. Companies must be incorporated for at least 3 years to comply with MSEG regulatory standards."
**Pass/Fail**: PASS

---

#### TC13: Company Registration Number Uniqueness (Unit Test)
**Test Case ID**: FR5-TC13
**Test Case Description**: Verify duplicate registration numbers are prevented
**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option
2. Enter company with registration number "12345678"
3. Attempt to submit another company with same registration number
**Test Data**: Company Name: Crusties, Registration No: 12237364
**Expected Output**: There should be an error message generated that the registration number already exists.
**Actual Result**: Error Message displayed; "That registration number already exists"
**Pass/Fail**: PASS

---

#### TC14: Companies House API Verification (Unit Test)
**Test Case ID**: FR5-TC14
**Test Case Description**: Verify system only approves companies that exists in Companies House registry
**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option
2. Verify function returns False for invalid company
3. Submit valid company name from Companies House registry.
**Test Data**: Company Name: test, Registration No: 00000000; Company Name: Crusties, Registration No: 12237364
**Expected Output**: Invalid company returns error, valid company is accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC15: Incorporation Date Format Validation (Unit Test)
**Test Case ID**: FR5-TC15
**Test Case Description**: Verify incorporation date must be in YYYY-MM-DD format
**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option
2. Enter invalid date formats: "01/01/2020", "2020-1-1", "20-01-2020"
3. Attempt to submit registration with each invalid format
4. Enter valid format "2020-01-01" and verify acceptance
**Test Data**: Invalid formats: "01/01/2020", "2020-1-1", "20-01-2020"; Valid format: "2020-01-01"
**Expected Output**: Invalid formats rejected with error message, valid format accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC16: Incorporation Date Range Validation (Unit Test)
**Test Case ID**: FR5-TC16
**Test Case Description**: Verify incorporation date must be between 1850 and today
**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option
2. Enter incorporation date "1800-01-01" (too old)
3. Attempt to submit registration
4. Enter future date "2026-12-31"
5. Attempt to submit registration
**Test Data**: Invalid dates: "1800-01-01", "2026-12-31"
**Expected Output**: Error message stating date must be between 1850 and today's date
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC29: Companies House Integration with Offline Fallback (Integration Test)
**Test Case ID**: FR5-INT-TC29
**Test Case Description**: Verify system falls back to offline dataset when API unavailable
**Test Case Procedure**:
1. Disable network connection or remove API key file
2. On Login Portal, Select Company then Sign-Up Option
3. Enter valid company name and number from offline dataset
4. Submit registration
5. Verify registration succeeds using offline validation
6. Check that system shows message about using offline verification
**Test Data**: Company from offline dataset (name and registration number)
**Expected Output**: System validates company using offline dataset when API unavailable, registration succeeds
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC46: Company Registration with Invalid Incorporation Date (System Test)
**Test Case ID**: FR5-SYS-TC46
**Test Case Description**: Verify company registration validates incorporation date
**Test Case Procedure**:
1. Launch MSEG application
2. On Login Portal, Select Company then Sign-Up Option
3. Fill all registration fields
4. Set incorporation date to recent date (less than 3 years ago, e.g., 2023-01-01)
5. Attempt to submit registration
6. Verify error message about minimum 3 years requirement
7. Change date to valid date (at least 3 years ago, e.g., 2020-01-01)
8. Submit registration successfully
9. Verify company account is created
**Test Data**: Company Name, Registration No, Username, Password; Invalid Date: 2023-01-01; Valid Date: 2020-01-01
**Expected Output**: Recent incorporation date rejected with error, older date accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC47: Companies House Verification (Online API) (System Test)
**Test Case ID**: FR5-SYS-TC47
**Test Case Description**: Verify online Companies House API verification works
**Test Case Procedure**:
1. Ensure internet connection is available
2. Launch MSEG application
3. On Login Portal, Select Company then Sign-Up Option
4. Enter invalid company name "NonexistentCompanyXYZ123" and number "00000000"
5. Attempt to submit registration
6. Verify error message stating company not found in Companies House registry
7. Enter valid company name and registration number from Companies House
8. Submit registration successfully
**Test Data**: Invalid Company: "NonexistentCompanyXYZ123", "00000000"; Valid Company from Companies House registry
**Expected Output**: Invalid company rejected with error, valid company accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC48: Companies House Verification (Offline Fallback) (System Test)
**Test Case ID**: FR5-SYS-TC48
**Test Case Description**: Verify offline dataset validation when API unavailable
**Test Case Procedure**:
1. Disable internet connection
2. Launch MSEG application
3. On Login Portal, Select Company then Sign-Up Option
4. Enter company name and registration number from offline dataset
5. Submit registration
6. Verify system displays message about using offline verification
7. Verify registration succeeds
**Test Data**: Company name and number from offline dataset
**Expected Output**: System uses offline validation when API unavailable, registration succeeds
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR6: Remove Stock Listing

#### TC17: Stock Deletion Function (Unit Test)
**Test Case ID**: FR6-TC17
**Test Case Description**: Verify stock can be deleted from system
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Select a stock using checkbox
4. Click "Delete Selected" button
5. Confirm deletion
6. Verify stock no longer appears in stock listing
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Stock is removed from the stock market listing
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC31: Stock Deletion Cascade to Prices (Integration Test)
**Test Case ID**: FR6-INT-TC31
**Test Case Description**: Verify deleting stock removes it completely from system
**Test Case Procedure**:
1. Login as Stock Manager
2. Approve an application to create a new stock with price history
3. Navigate to Stock Market page
4. Verify stock appears in listing with return percentages (24hr, 1M, 6M, 1Y)
5. Select stock checkbox
6. Click "Delete Selected" button
7. Confirm deletion
8. Verify stock no longer appears in stock listing
9. Refresh page to confirm stock remains deleted
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Stock and all associated price history are completely removed from system
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC49: Delete Stock with Confirmation (System Test)
**Test Case ID**: FR6-SYS-TC49
**Test Case Description**: Verify stock deletion requires confirmation and removes stock
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify stocks are displayed
4. Select a stock checkbox
5. Click "Delete Selected" button
6. Verify confirmation dialog appears
7. Click "Cancel" or "No"
8. Verify stock is still in listing
9. Select stock checkbox again
10. Click "Delete Selected"
11. Click "Yes" or "Confirm" to confirm deletion
12. Verify stock no longer appears in listing
13. Refresh page to confirm deletion is permanent
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Deletion requires confirmation, cancelling preserves stock, confirming removes stock permanently
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC50: Delete Multiple Stocks Simultaneously (System Test)
**Test Case ID**: FR6-SYS-TC50
**Test Case Description**: Verify multiple stocks can be deleted at once
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Select checkboxes for 3 different stocks
4. Click "Delete Selected"
5. Confirm deletion
6. Verify all 3 stocks are removed from listing
7. Refresh page to confirm deletion is permanent
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: All selected stocks deleted in single operation
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR7: View All Active Stock Listings

#### TC18: Retrieve All Stocks (Unit Test)
**Test Case ID**: FR7-TC18
**Test Case Description**: Verify system displays all stocks with prices and sectors
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify all approved stocks are displayed
4. Verify each stock shows ticker, price, sector, and return percentages
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: All stocks displayed with ticker, current price, sector, and performance data
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC32: Sector Filter Application (Integration Test)
**Test Case ID**: FR7-INT-TC32
**Test Case Description**: Verify sector filter correctly filters displayed stocks
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify all stocks from different sectors are displayed
4. Click "Filter by Sector" button
5. Select only "Technology" checkbox
6. Click "Apply Filter"
7. Verify only Technology sector stocks are displayed
8. Click "Clear Filter"
9. Verify all stocks are displayed again
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Filter shows only selected sector stocks, clear filter restores all stocks
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC33: Multi-Sector Filter (Integration Test)
**Test Case ID**: FR7-INT-TC33
**Test Case Description**: Verify multiple sectors can be selected simultaneously
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify stocks from multiple sectors are displayed
4. Click "Filter by Sector"
5. Select "Technology" and "Healthcare" checkboxes
6. Click "Apply Filter"
7. Verify only Technology and Healthcare stocks are displayed
8. Verify stocks from other sectors are hidden
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Only stocks from selected sectors (Technology and Healthcare) are visible
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC51: Stock Listing Displays All Fields (System Test)
**Test Case ID**: FR7-SYS-TC51
**Test Case Description**: Verify stock listing table shows all required information
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify table displays columns: Ticker, Price, Sector, 24hr %, 1M %, 6M %, 1Y %
4. Verify all stocks display data in each column
5. Verify price is formatted with decimal places
6. Verify percentages show + or - signs
7. Verify positive returns shown in green, negative in red (if color coded)
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Stock listing displays all required fields with proper formatting
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC52: Filter by Single Sector (System Test)
**Test Case ID**: FR7-SYS-TC52
**Test Case Description**: Verify sector filtering works correctly for single sector
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify stocks from multiple sectors are displayed
4. Click "Filter by Sector" button
5. Select only one sector (e.g., "Healthcare")
6. Click "Apply Filter"
7. Verify only stocks from selected sector are displayed
8. Verify stocks from other sectors are hidden
9. Click "Clear Filter"
10. Verify all stocks are displayed again
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Filter correctly shows only selected sector stocks, clear filter restores all stocks
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC53: Filter by Multiple Sectors (System Test)
**Test Case ID**: FR7-SYS-TC53
**Test Case Description**: Verify multiple sectors can be filtered simultaneously
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify stocks from multiple sectors are displayed
4. Click "Filter by Sector"
5. Select multiple sectors (e.g., "Technology" and "Finance")
6. Click "Apply Filter"
7. Verify only stocks from selected sectors are displayed
8. Verify stocks from other sectors are hidden
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Multiple sector selection shows stocks from all selected sectors only
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC54: Stock Listing as Company (Read-Only Mode) (System Test)
**Test Case ID**: FR7-SYS-TC54
**Test Case Description**: Verify company users see stocks in read-only mode without management features
**Test Case Procedure**:
1. Login as Company
2. Navigate to Stock Market page
3. Verify stock listing displays with all data (ticker, price, sector, returns)
4. Verify NO checkboxes appear next to stocks
5. Verify NO "Delete Selected" button is visible
6. Verify NO "Analysis" menu is available
7. Verify Filter by Sector functionality works
8. Verify stocks are view-only (cannot modify or delete)
**Test Data**: Company Username: company1, Company Password: pass456
**Expected Output**: Company users can view stocks but cannot modify, delete, or analyze them
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR8-FR12: Stock Analysis Functions

#### TC19: Time-framed Returns Calculation (1 Month) (Unit Test)
**Test Case ID**: FR8-TC19
**Test Case Description**: Verify 1-month return calculation is displayed correctly
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. View a stock's 1M % (1-month return) column
4. Verify the percentage is displayed
5. Verify the value shows positive (+) or negative (-) sign
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: 1-month return percentage is displayed with correct sign
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC20: Time-framed Returns Calculation (6 Months) (Unit Test)
**Test Case ID**: FR8-TC20
**Test Case Description**: Verify 6-month return calculation is displayed correctly
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. View a stock's 6M % (6-month return) column
4. Verify the percentage is displayed
5. Verify the value shows positive (+) or negative (-) sign
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: 6-month return percentage is displayed with correct sign
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC21: Time-framed Returns Calculation (1 Year) (Unit Test)
**Test Case ID**: FR8-TC21
**Test Case Description**: Verify 1-year return calculation is displayed correctly
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. View a stock's 1Y % (1-year return) column
4. Verify the percentage is displayed
5. Verify the value shows positive (+) or negative (-) sign
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: 1-year return percentage is displayed with correct sign
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC22: 24-Hour Change Calculation (Unit Test)
**Test Case ID**: FR8-TC22
**Test Case Description**: Verify 24-hour price change is displayed correctly
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. View a stock's 24hr % (24-hour change) column
4. Verify the percentage is displayed
5. Verify the value shows positive (+) or negative (-) sign
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: 24-hour change percentage is displayed with correct sign
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC34: Select Multiple Stocks for Analysis (Integration Test)
**Test Case ID**: FR8-INT-TC34
**Test Case Description**: Verify multiple stocks can be selected via checkboxes
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Click checkboxes for 3 different stocks
4. Verify checkboxes show as selected
5. Click "Select All" button
6. Verify all stock checkboxes are selected
7. Click "Deselect All" button
8. Verify all stock checkboxes are cleared
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Checkbox interface allows multiple stock selection for analysis
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC35: Time-framed Returns Report Generation (Integration Test)
**Test Case ID**: FR9-INT-TC35
**Test Case Description**: Verify time-framed returns report displays data for selected stocks
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Select 3 stocks via checkboxes
4. Click "Analysis" menu
5. Click "Time-framed Returns"
6. Verify report window opens
7. Verify report shows 1M, 6M, 1Y returns for all 3 selected stocks
8. Verify percentages are displayed with + or - signs
9. Click "Save as TXT" button
10. Verify report is saved to file
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Report displays returns for all selected stocks and can be exported to TXT
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC36: Valuation Comparison Report (Integration Test)
**Test Case ID**: FR10-INT-TC36
**Test Case Description**: Verify valuation comparison shows current values and growth
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Select multiple stocks via checkboxes
4. Click Analysis → Valuation Comparison
5. Verify report displays: ticker, current price, total valuation, shares, 1Y growth %
6. Verify report is exportable to TXT file
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Report shows valuation data and growth percentages for selected stocks
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC37: Sector Benchmarking Report (Integration Test)
**Test Case ID**: FR11-INT-TC37
**Test Case Description**: Verify sector benchmarking compares stock to sector average
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Verify multiple stocks from different sectors are available
4. Select multiple stocks from Technology and Healthcare sectors
5. Click Analysis → Sector Benchmarking
6. Verify report shows average 1Y return for each sector
7. Verify each stock shows difference from its sector average
8. Verify differences displayed with + or - signs
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Each stock is compared to its sector average, differences are shown
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC38: Performance Consistency Score Calculation (Integration Test)
**Test Case ID**: FR12-INT-TC38
**Test Case Description**: Verify consistency score based on return variance
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Select multiple stocks via checkboxes
4. Click Analysis → Performance Consistency
5. Verify report displays consistency score for each stock
6. Verify stocks with stable returns show higher scores
7. Verify stocks with volatile returns show lower scores
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Stable stocks have higher consistency scores, volatile stocks have lower scores
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC39: Market Report Generation (No Selection Required) (Integration Test)
**Test Case ID**: FR12-INT-TC39
**Test Case Description**: Verify market report analyzes entire market regardless of selection
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page (do NOT select any stocks)
3. Click Analysis → Generate Market Report
4. Verify report displays:
   - Total companies listed
   - Total market valuation
   - Average valuation
   - Sector-wise distribution with percentages
5. Verify report can be exported to TXT file
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Report analyzes all stocks in system, not just selected ones
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC55: Time-framed Returns Analysis for Multiple Stocks (System Test)
**Test Case ID**: FR8-SYS-TC55
**Test Case Description**: End-to-end test of time-framed returns analysis
**Test Case Procedure**:
1. Login as manager
2. Create 3 test stocks with price histories
3. Navigate to Stock Market page
4. Select all 3 stocks via checkboxes
5. Click "Analysis" menu in header
6. Click "Time-framed Returns"
7. Verify report window opens with title "Time-framed Returns Analysis"
8. Verify report shows table with columns: Ticker, 1M %, 6M %, 1Y %
9. Verify all 3 stocks listed with calculated returns
10. Verify percentages formatted with + or - signs
11. Click "Save as TXT" button
12. Choose save location
13. Verify file saved successfully
14. Open saved file and verify content matches display
**Expected Output**: Report displays correct returns for selected stocks, exportable to TXT
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC56: Valuation Comparison Analysis (System Test)
**Test Case ID**: FR10-SYS-TC56
**Test Case Description**: End-to-end test of valuation comparison
**Test Case Procedure**:
1. Login as manager
2. Create 3 stocks with different valuations and growth rates
3. Select all 3 stocks
4. Click Analysis → Valuation Comparison
5. Verify report shows: Ticker, Current Price, Total Valuation, Shares, 1Y Growth %
6. Manually calculate total valuation = current_price × shares
7. Verify calculations match expected values
8. Export report to TXT
9. Verify export successful
**Expected Output**: Report shows accurate valuation data for all selected stocks
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC57: Sector Benchmarking with Mixed Sectors (System Test)
**Test Case ID**: FR11-SYS-TC57
**Test Case Description**: Verify sector benchmarking with stocks from different sectors
**Test Case Procedure**:
1. Login as manager (manager1/pass123)
2. Create stocks:
   - Tech A: 1Y return = 10%
   - Tech B: 1Y return = 20%
   - Healthcare A: 1Y return = 5%
   - Healthcare B: 1Y return = 15%
3. Navigate to StockMarketPage
4. Select all 4 stocks
5. Click Analysis → Sector Benchmarking
6. Verify report calculates:
   - Technology average = 15% (average of 10% and 20%)
   - Healthcare average = 10% (average of 5% and 15%)
7. Verify each stock shows:
   - Tech A: -5% vs sector (10% - 15%)
   - Tech B: +5% vs sector (20% - 15%)
   - Healthcare A: -5% vs sector (5% - 10%)
   - Healthcare B: +5% vs sector (15% - 10%)
**Expected Output**: Each stock correctly compared to its own sector average
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC58: Performance Consistency Score Interpretation (System Test)
**Test Case ID**: FR12-SYS-TC58
**Test Case Description**: Verify consistency score correctly identifies stable vs volatile stocks
**Test Case Procedure**:
1. Login as manager (manager1/pass123)
2. Create 2 stocks:
   - Stable Stock: 1M=5%, 6M=5.2%, 1Y=5.5% (very consistent)
   - Volatile Stock: 1M=30%, 6M=-10%, 1Y=8% (inconsistent)
3. Navigate to StockMarketPage
4. Select both stocks
5. Click Analysis → Performance Consistency
6. Verify Stable Stock has high consistency score (close to 100)
7. Verify Volatile Stock has lower consistency score
8. Verify score formula: 100 - variance
9. Manually calculate variance for both stocks and verify
**Expected Output**: Stable stock has significantly higher consistency score than volatile stock
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC59: Generate Market Report (All Stocks Analysis) (System Test)
**Test Case ID**: FR12-SYS-TC59
**Test Case Description**: Verify market report analyzes entire market without selection
**Test Case Procedure**:
1. Login as manager
2. Create 10 stocks across different sectors with known valuations
3. Navigate to Stock Market page
4. Do NOT select any stocks
5. Click Analysis → Generate Market Report
6. Verify report shows:
   - Total Companies Listed: 10
   - Total Market Valuation: (sum of all 10 stock valuations)
   - Average Valuation: (total / 10)
   - Sector Distribution table with counts and percentages
7. Manually verify all calculations
8. Export report
9. Verify export successful
**Expected Output**: Market report analyzes all stocks regardless of checkbox selection
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## NON-FUNCTIONAL REQUIREMENTS TESTING

### NR1: Privacy - Data Handling

#### TC40: Password Hashing on Storage (Integration Test)
**Test Case ID**: NR1-INT-TC40
**Test Case Description**: Verify passwords are hashed and not stored in plain text
**Test Case Procedure**:
1. On Login Portal, Select Company then Sign-Up Option
2. Register new company user with password "TestPass123"
3. Complete registration
4. Login with the registered username and password "TestPass123"
5. Verify login succeeds
6. Logout
7. Attempt login with incorrect password
8. Verify login fails with error message
**Test Data**: New Company Username, Password: TestPass123
**Expected Output**: Login succeeds with correct password, fails with incorrect password (password is securely stored)
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC60: Password Not Visible in UI (System Test)
**Test Case ID**: NR1-SYS-TC60
**Test Case Description**: Verify passwords are masked in all input fields
**Test Case Procedure**:
1. Launch application
2. Navigate to company signup page
3. Enter password in password field
4. Verify characters appear as dots or asterisks (not plain text)
5. Navigate to login page
6. Enter password
7. Verify password masked
8. Attempt to copy password from field (should copy masked characters)
**Expected Output**: Passwords never displayed in plain text in UI
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC61: No Sensitive Data in Error Messages (System Test)
**Test Case ID**: NR1-SYS-TC61
**Test Case Description**: Verify error messages don't expose sensitive information
**Test Case Procedure**:
1. Attempt login with incorrect username
2. Verify error message is generic: "Invalid username or password"
3. Attempt login with correct username, wrong password
4. Verify same generic error message (does not reveal if username exists)
5. Attempt database operation that fails
6. Verify error message doesn't expose SQL queries or table structure
**Expected Output**: Error messages are user-friendly and don't leak sensitive details
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR2: Data Integrity Validation

#### TC23: Positive Shares Validation (Unit Test)
**Test Case ID**: NR2-TC23
**Test Case Description**: Verify shares outstanding must be positive
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Enter 0 or negative value for Proposed Shares
4. Attempt to submit application
**Test Data**: Company Username: company1, Company Password: pass456; Proposed Shares: 0 or -1000000
**Expected Output**: Error message displayed stating shares must be positive
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC24: Positive Valuation Validation (Unit Test)
**Test Case ID**: NR2-TC24
**Test Case Description**: Verify total valuation must be positive
**Test Case Procedure**:
1. Login on Company Account
2. Select New Application
3. Enter 0 or negative value for Proposed Valuation
4. Attempt to submit application
**Test Data**: Company Username: company1, Company Password: pass456; Proposed Valuation: 0 or -500000000
**Expected Output**: Error message displayed stating valuation must be positive
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC25: Positive Price Validation (Unit Test)
**Test Case ID**: NR2-TC25
**Test Case Description**: Verify stock prices are always positive
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. View all stock prices
4. Verify all prices shown are positive values
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: All stock prices displayed are positive values greater than zero
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC62: Prevent Negative Stock Values Throughout System (System Test)
**Test Case ID**: NR2-SYS-TC62
**Test Case Description**: Verify system prevents negative values at all entry points
**Test Case Procedure**:
1. Login as company
2. Create application with negative shares: -1000000
3. Verify form validation rejects negative value
4. Enter negative valuation: -500000000
5. Verify form validation rejects
6. Enter shares as 0
7. Verify validation requires positive value
8. Directly attempt database insertion with negative values (via Python console)
9. Verify CHECK constraints prevent insertion
**Expected Output**: System prevents negative or zero values at UI and database levels
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR3: Availability - Database Connection

#### TC41: Database Initialization on Startup (Integration Test)
**Test Case ID**: NR3-INT-TC41
**Test Case Description**: Verify system initializes properly on first launch
**Test Case Procedure**:
1. Launch MSEG application for the first time
2. Verify application opens successfully
3. Verify login page is displayed
4. Attempt to login as Stock Manager (manager1/pass123)
5. Verify login succeeds
6. Navigate to Stock Market page
7. Verify all sectors are available in sector dropdown/filter
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Application initializes successfully with all required data available
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC63: Application Starts Without Errors (System Test)
**Test Case ID**: NR3-SYS-TC63
**Test Case Description**: Verify application launches successfully and is available
**Test Case Procedure**:
1. Ensure data directory exists
2. Run command: python main.py
3. Verify application window opens within 5 seconds
4. Verify no error dialogs appear
5. Verify login page displays
6. Verify all UI elements render correctly
7. Check console for any error messages
**Expected Output**: Application starts cleanly and is immediately usable
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC64: Database Recovery After Corruption (System Test)
**Test Case ID**: NR3-SYS-TC64
**Test Case Description**: Verify system handles database corruption gracefully
**Test Case Procedure**:
1. Close application
2. Corrupt database file (write random bytes to data/mseg.db)
3. Launch application
4. Verify error message appears indicating database issue
5. Delete corrupted database
6. Relaunch application
7. Verify system creates new clean database
8. Verify sectors are repopulated
9. Verify application is usable
**Expected Output**: System detects corruption and can recover with fresh database
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR4: Performance

#### TC65: Stock Listing Load Time (System Test)
**Test Case ID**: NR4-SYS-TC65
**Test Case Description**: Verify stock listing loads within 2 seconds under normal load
**Test Case Procedure**:
1. Create 100 test stocks with full price history
2. Login as manager (manager1/pass123)
3. Start timer
4. Navigate to Stock Market page
5. Stop timer when all stocks rendered in table
6. Verify load time < 2 seconds
7. Apply filter
8. Verify filter applies within 2 seconds
**Expected Output**: Stock listing with 100 stocks loads and renders within 2 seconds
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC66: Application Review Page Load Time (System Test)
**Test Case ID**: NR4-SYS-TC66
**Test Case Description**: Verify application review screen loads within 2 seconds
**Test Case Procedure**:
1. Create 50 pending applications
2. Login as manager (manager1/pass123)
3. Start timer
4. Navigate to Manager Portal page
5. Stop timer when all pending applications rendered
6. Verify load time < 2 seconds
7. Select an application
8. Verify details load within 1 second
**Expected Output**: Manager portal loads quickly even with many pending applications
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR5: Usability

#### TC67: Clear Labels and Intuitive Navigation (System Test)
**Test Case ID**: NR5-SYS-TC67
**Test Case Description**: Verify all interface elements have clear, understandable labels
**Test Case Procedure**:
1. Launch application
2. Review all buttons, labels, and menu items on login page
3. Verify all text is clear and unambiguous
4. Login as company
5. Review header navigation menu
6. Verify menu items clearly indicate their function
7. Navigate through all pages
8. Verify form field labels are descriptive
9. Verify button actions are clear (e.g., "Submit Application" not just "Submit")
10. Ask non-technical user to navigate system without instructions
**Expected Output**: All UI elements have clear, intuitive labels; navigation is self-explanatory
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC68: Consistent Filter Behavior Across System (System Test)
**Test Case ID**: NR5-SYS-TC68
**Test Case Description**: Verify filter dialogs work consistently
**Test Case Procedure**:
1. Login as manager
2. Navigate to Stock Market page
3. Open sector filter dialog
4. Verify checkboxes for all sectors present
5. Verify "Apply Filter" and "Clear Filter" buttons visible
6. Apply filter and verify results
7. Clear filter and verify all stocks shown
8. Verify same filter pattern used throughout application
**Expected Output**: Filter interface is consistent and predictable across all uses
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC69: Theme Switching (Light/Dark Mode) (System Test)
**Test Case ID**: NR5-SYS-TC69
**Test Case Description**: Verify theme toggle provides good visibility in both modes
**Test Case Procedure**:
1. Login as company (company1/pass456)
2. Verify application starts in light mode
3. Verify all text is readable against light background
4. Click theme toggle button in header
5. Verify application switches to dark mode
6. Verify all text is readable against dark background
7. Verify colors provide good contrast
8. Navigate through different pages
9. Verify theme persists across page changes
10. Toggle back to light mode
11. Verify smooth transition
**Expected Output**: Both themes provide excellent readability and visual comfort
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR6: Scalability

#### TC70: System Performance with 500 Stocks (System Test)
**Test Case ID**: NR6-SYS-TC70
**Test Case Description**: Verify system handles large number of stocks without major degradation
**Test Case Procedure**:
1. Create script to generate 500 stocks with full price histories
2. Run script to populate database
3. Launch application and login as manager
4. Navigate to Stock Market page
5. Measure load time
6. Verify all stocks display correctly
7. Apply filters and measure response time
8. Select multiple stocks and run analysis
9. Verify analysis completes successfully
10. Monitor memory usage during operations
**Expected Output**: System handles 500 stocks with acceptable performance (load < 5 seconds)
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC71: Database Growth with 1000 Applications (System Test)
**Test Case ID**: NR6-SYS-TC71
**Test Case Description**: Verify database handles growth in applications and stocks
**Test Case Procedure**:
1. Create script to generate 1000 applications
2. Approve 500 of them (creates 500 stocks with 366 prices each = 183,000 price records)
3. Verify database file size is manageable (< 500MB)
4. Launch application
5. Login as manager (manager1/pass123)
6. Verify startup time is reasonable
7. Navigate to manager portal
8. Verify pending/approved/rejected lists load
9. Test database query performance with large dataset
**Expected Output**: System scales to 1000 applications and 500 stocks without redesign
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR7: Reliability - Deterministic Calculations

#### TC26: Return Calculation Consistency (Unit Test)
**Test Case ID**: NR7-TC26
**Test Case Description**: Verify return calculations are consistent and repeatable
**Test Case Procedure**:
1. Login as Stock Manager
2. Navigate to Stock Market page
3. Note the return percentages (24hr, 1M, 6M, 1Y) for a specific stock
4. Refresh the page
5. Verify the same stock shows identical return percentages
**Test Data**: Manager Username: manager1, Manager Password: pass123
**Expected Output**: Return percentages remain identical after page refresh
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC72: Return Calculation Repeatability (System Test)
**Test Case ID**: NR7-SYS-TC72
**Test Case Description**: Verify return calculations are deterministic and repeatable
**Test Case Procedure**:
1. Create stock with fixed price history
2. Login as manager
3. Select stock and run Time-framed Returns analysis
4. Record 1M, 6M, 1Y return values
5. Close and reopen analysis
6. Verify identical return values
7. Restart application
8. Run analysis again
9. Verify values still identical
10. Repeat 10 times
**Expected Output**: All calculations return exact same values every time
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC73: Sector Benchmarking Calculation Determinism (System Test)
**Test Case ID**: NR7-SYS-TC73
**Test Case Description**: Verify sector benchmarking calculations are repeatable
**Test Case Procedure**:
1. Login as manager (manager1/pass123)
2. Create 5 stocks in Technology sector with known returns
3. Navigate to StockMarketPage and select all 5 stocks
4. Run Sector Benchmarking analysis
5. Record sector average and individual stock differences
6. Run analysis again
7. Verify identical results
8. Add 6th stock to Technology sector
9. Run analysis
10. Verify sector average recalculated correctly
11. Remove 6th stock
12. Verify sector average returns to original value
**Expected Output**: Benchmarking calculations are deterministic and update correctly with data changes
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

#### TC74: Price History Generation Consistency (System Test)
**Test Case ID**: NR7-SYS-TC74
**Test Case Description**: Verify price history generation follows specified random walk model
**Test Case Procedure**:
1. Create application with shares=1,000,000 and valuation=500,000,000
2. Approve application (triggers price generation)
3. Verify initial price = valuation / shares = 500.00
4. Query all 366 price records
5. For each consecutive day pair, calculate daily change percentage
6. Verify all daily changes are within ±1.5% range
7. Verify no prices are negative or zero
8. Verify prices follow realistic random walk (no impossible jumps)
**Expected Output**: Generated prices follow random walk model with ±1.5% daily variance
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## CROSS-FUNCTIONAL SYSTEM TESTS

### TC75: Role-Based Access Control
**Test Case ID**: RBAC-SYS-TC75
**Test Case Description**: Verify company and manager users have appropriate access levels
**Test Case Procedure**:
1. Login as company user
2. Verify Stock Market page is read-only (no checkboxes, no delete button)
3. Verify Analysis menu is NOT available
4. Verify can only see own applications in My Applications
5. Logout and login as manager
6. Verify Stock Market page has full access (checkboxes, delete, analysis)
7. Verify can see all applications in Manager Portal
8. Verify can approve/reject applications
9. Attempt to directly access manager functions as company user (via URL manipulation if applicable)
**Expected Output**: Company users limited to read-only stock view and own applications, managers have full access
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### TC76: Data Persistence Across Sessions
**Test Case ID**: PERSIST-SYS-TC76
**Test Case Description**: Verify all data persists after application restart
**Test Case Procedure**:
1. Login as company and create application
2. Note application ID
3. Logout and login as manager
4. Approve application
5. Note created stock ticker
6. Close application completely
7. Relaunch application
8. Login as manager
9. Verify application still shows as approved
10. Navigate to Stock Market
11. Verify stock still exists with all data intact
12. Verify price history still available
**Expected Output**: All data persists correctly after application restart
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### TC77: Concurrent User Workflow (Sequential)
**Test Case ID**: CONCURRENT-SYS-TC77
**Test Case Description**: Verify two users can work with system sequentially without conflicts
**Test Case Procedure**:
1. User A (company) logs in and submits application
2. User A logs out
3. User B (manager) logs in
4. User B sees User A's application in pending list
5. User B approves application
6. User B logs out
7. User A logs in again
8. User A sees approved status
9. User A navigates to Stock Market
10. User A sees newly listed stock
**Expected Output**: Users can work sequentially without data corruption or conflicts
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### TC78: End-to-End Full System Workflow
**Test Case ID**: E2E-SYS-TC78
**Test Case Description**: Complete system test covering all major features
**Test Case Procedure**:
1. Register new company account
2. Login and submit 2 applications
3. Logout and login as manager
4. Approve 1st application, reject 2nd application
5. Verify stock created for approved application
6. Navigate to Stock Market
7. Verify new stock appears in listing
8. Create 2 more stocks directly (from other approved apps)
9. Apply sector filter to view subset of stocks
10. Select multiple stocks
11. Run all analysis reports: Time-framed Returns, Valuation Comparison, Sector Benchmarking, Consistency Score
12. Generate Market Report
13. Export all reports to TXT files
14. Delete one stock
15. Verify stock removed
16. Logout and login as company
17. Verify can see approved stock in Stock Market (read-only)
18. Verify can see rejection notes for rejected application
19. Switch between light and dark themes
20. Logout
**Expected Output**: All features work together cohesively in realistic usage scenario
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## NEGATIVE TESTING

### TC79: SQL Injection Prevention
**Test Case ID**: SEC-NEG-TC79
**Test Case Description**: Verify system is protected against SQL injection attacks
**Test Case Procedure**:
1. Attempt login with username: `admin' OR '1'='1`
2. Verify login fails (not vulnerable)
3. Create application with company name: `Test'; DROP TABLE stock; --`
4. Submit application
5. Verify application stored safely without executing SQL
6. Verify stock table still exists
7. Test other input fields with SQL injection patterns
**Expected Output**: System safely handles SQL injection attempts without execution
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### TC80: Invalid File Attachment Handling
**Test Case ID**: NEG-TC80
**Test Case Description**: Verify system handles invalid attachment files gracefully
**Test Case Procedure**:
1. Login as company
2. Create application
3. Attempt to attach non-existent file
4. Verify error message appears
5. Attempt to attach executable file (.exe) if validation exists
6. Attempt to attach extremely large file (>100MB)
7. Verify appropriate error messages or handling
**Expected Output**: System validates attachments and provides clear error messages
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### TC81: Boundary Testing - Maximum String Lengths
**Test Case ID**: NEG-TC81
**Test Case Description**: Verify system handles very long input strings
**Test Case Procedure**:
1. Login as company (company1/pass456)
2. Navigate to application form
3. Create application with 1000-character company name
4. Attempt to submit
5. Verify system handles appropriately (truncation or validation error)
6. Test with maximum username length (10 chars) and 11 chars during registration
7. Test password with 31 characters (max is 30) during registration
8. Verify appropriate validation messages
**Expected Output**: System enforces reasonable length limits with clear messages
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## TEST SUMMARY

**Total Test Cases**: 81

### Breakdown by Testing Type:
- **Unit Testing**: 26 test cases (TC1-TC26)
- **Integration Testing**: 15 test cases (TC27-TC41)
- **System Testing**: 37 test cases (TC42-TC78)
- **Negative Testing**: 3 test cases (TC79-TC81)

### Breakdown by Requirement:
- **FR1**: 3 test cases (TC1, TC27, TC42)
- **FR2**: 3 test cases (TC2, TC3, TC4)
- **FR3**: 3 test cases (TC5, TC28, TC43)
- **FR4**: 8 test cases (TC6-TC11, TC30, TC44, TC45)
- **FR5**: 8 test cases (TC12-TC16, TC29, TC46-TC48)
- **FR6**: 4 test cases (TC17, TC31, TC49, TC50)
- **FR7**: 7 test cases (TC18, TC32, TC33, TC51-TC54)
- **FR8-FR12**: 15 test cases (TC19-TC22, TC34-TC39, TC55-TC59)
- **NR1**: 3 test cases (TC40, TC60, TC61)
- **NR2**: 4 test cases (TC23-TC25, TC62)
- **NR3**: 3 test cases (TC41, TC63, TC64)
- **NR4**: 2 test cases (TC65, TC66)
- **NR5**: 3 test cases (TC67-TC69)
- **NR6**: 2 test cases (TC70, TC71)
- **NR7**: 4 test cases (TC26, TC72-TC74)
- **Cross-functional**: 4 test cases (TC75-TC78)
- **Negative Testing**: 3 test cases (TC79-TC81)

---

## TEST EXECUTION NOTES

### Prerequisites:
1. Python 3.x installed with tkinter support
2. SQLite3 available
3. Required Python packages: requests
4. Test data directory structure exists
5. Demo accounts available: manager1/pass123, company1/pass456

### Test Environment:
- Operating System: (To be specified)
- Python Version: (To be specified)
- Database: SQLite 3.x
- Screen Resolution: (For UI tests)

### Test Data:
- Create test companies with known registration numbers
- Prepare test documents for attachments
- Generate price histories with predictable patterns for calculation verification
- Use isolated test database to avoid production data contamination

### Execution Order:
1. Run Unit Tests first to verify individual components
2. Run Integration Tests to verify component interactions
3. Run System Tests for end-to-end workflows
4. Run Negative Tests to verify error handling

### Pass Criteria:
- All functional requirements (FR1-FR13) must have at least 80% test pass rate
- All non-functional requirements (NR1-NR7) must have 100% test pass rate
- No critical bugs (data loss, security vulnerabilities, system crashes)
- Performance requirements met (< 2 second load times)

---

## DEFECT TRACKING

When tests fail, record:
1. Test Case ID
2. Date and time of test
3. Tester name
4. Actual result observed
5. Steps to reproduce
6. Severity: Critical / High / Medium / Low
7. Screenshots or logs if applicable
8. Status: Open / In Progress / Fixed / Closed

---

*End of Test Plan*
