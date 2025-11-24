# MSEG Test Plan
## Manchester Stock Exchange System - Comprehensive Test Cases

---

## UNIT TESTING

### FR1: View Queue of Pending Applications

#### TC1: Retrieve All Pending Applications
**Test Case ID**: FR1-TC1
**Test Case Description**: Verify that the system retrieves all pending applications from database
**Test Case Procedure**:
1. Open Python interpreter and import db module
2. Create test applications with status='pending' using `application_insert()`
3. Call `applications_pending_all()`
4. Verify returned list contains only pending applications
**Expected Output**: Function returns list of tuples containing only applications with status='pending'
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR2: Approve Valid Application

#### TC2: Application Approval Status Update
**Test Case ID**: FR2-TC2
**Test Case Description**: Verify application status changes to 'approved' in database
**Test Case Procedure**:
1. Import db module
2. Insert test application with status='pending'
3. Call `application_set_approved(application_id)`
4. Query application table to verify status='approved'
**Expected Output**: Application status in database is updated to 'approved'
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC3: Stock Creation from Approved Application
**Test Case ID**: FR2-TC3
**Test Case Description**: Verify stock is created when application is approved
**Test Case Procedure**:
1. Import db module
2. Insert test application with valid data
3. Call `stock_create_from_application(app_id)`
4. Query stock table to verify new stock exists
5. Verify stock ticker matches application ticker
**Expected Output**: New stock record created with ticker, shares, and valuation from application
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC4: Stock Price History Generation
**Test Case ID**: FR2-TC4
**Test Case Description**: Verify 366 days of price history is generated for new stock
**Test Case Procedure**:
1. Import db module
2. Create stock using `stock_create_from_application()`
3. Call `stock_get_prices(stock_id)`
4. Count number of price records returned
5. Verify prices show realistic daily variation (±1.5%)
**Expected Output**: 366 price records created with random walk pricing model
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR3: Reject Application with Reasons

#### TC5: Application Rejection Status Update
**Test Case ID**: FR3-TC5
**Test Case Description**: Verify application status changes to 'rejected' with notes
**Test Case Procedure**:
1. Import db module
2. Insert test application with status='pending'
3. Call `application_set_rejected(app_id, "Test rejection reason")`
4. Query application to verify status='rejected' and internal_notes field contains reason
**Expected Output**: Application status='rejected' and internal_notes contains rejection reason
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR4: Integrity Check (Missing Fields, Duplicates, Unrealistic Valuations)

#### TC6: Ticker Format Validation
**Test Case ID**: FR4-TC6
**Test Case Description**: Verify ticker must be 3-4 capital letters only
**Test Case Procedure**:
1. Open ApplicationFormPage in test mode
2. Test invalid tickers: "AB" (too short), "ABCDE" (too long), "ab12" (lowercase/numbers)
3. Verify validation function rejects these inputs
4. Test valid ticker "MSFT"
**Expected Output**: Invalid tickers rejected, valid ticker accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC7: Duplicate Ticker Prevention
**Test Case ID**: FR4-TC7
**Test Case Description**: Verify system prevents duplicate ticker symbols
**Test Case Procedure**:
1. Import db module
2. Create stock with ticker "TEST"
3. Attempt to create application with same ticker "TEST"
4. Verify validation check in ApplicationFormPage.submit() detects duplicate (lines 472-476)
**Expected Output**: Error message "Ticker TEST is already in use" displayed
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC8: Valuation Lower Bound Check
**Test Case ID**: FR4-TC8
**Test Case Description**: Verify valuation must be at least 100 million
**Test Case Procedure**:
1. Open ApplicationFormPage
2. Enter valuation of 50,000,000 (50 million)
3. Attempt to submit application
4. Verify validation check at lines 501-504 in pages.py rejects submission
**Expected Output**: Error message "Total valuation must be at least 100 million"
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC9: Valuation Upper Bound Check
**Test Case ID**: FR4-TC9
**Test Case Description**: Verify valuation cannot exceed 500 billion
**Test Case Procedure**:
1. Open ApplicationFormPage
2. Enter valuation of 600,000,000,000 (600 billion)
3. Attempt to submit application
4. Verify validation check at lines 497-499 rejects submission
**Expected Output**: Error message "Total valuation must not exceed 500 billion"
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC10: Missing Required Fields
**Test Case ID**: FR4-TC10
**Test Case Description**: Verify all required fields must be filled
**Test Case Procedure**:
1. Open ApplicationFormPage
2. Leave one or more fields empty (e.g., company name)
3. Attempt to submit application
4. Verify validation check at lines 455-464 prevents submission
**Expected Output**: Error message "All fields must be filled" displayed
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC11: Attachment Requirement
**Test Case ID**: FR4-TC11
**Test Case Description**: Verify at least one attachment is required
**Test Case Procedure**:
1. Open ApplicationFormPage
2. Fill all fields but do not attach any documents
3. Attempt to submit application
4. Verify validation check at lines 507-509 prevents submission
**Expected Output**: Error message "At least one attachment is required" displayed
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR5: Regulatory Compliance Review

#### TC12: Company Incorporation Date Validation
**Test Case ID**: FR5-TC12
**Test Case Description**: Verify company must be incorporated for at least 3 years
**Test Case Procedure**:
1. Open InlineCompanySignup form
2. Enter incorporation date less than 3 years ago (e.g., 2023-01-01 if today is 2025-11-24)
3. Attempt to submit registration
4. Verify validation at lines 108-114 in pages.py rejects submission
**Expected Output**: Error message "Company must be incorporated at least 3 years ago"
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC13: Company Registration Number Uniqueness
**Test Case ID**: FR5-TC13
**Test Case Description**: Verify duplicate registration numbers are prevented
**Test Case Procedure**:
1. Import db module
2. Insert company with registration number "12345678"
3. Attempt to insert another company with same registration number
4. Verify UNIQUE constraint on company.registration_number prevents duplicate
**Expected Output**: Database error "UNIQUE constraint failed" raised
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC14: Companies House API Verification
**Test Case ID**: FR5-TC14
**Test Case Description**: Verify system checks company exists in Companies House registry
**Test Case Procedure**:
1. Import companies_house module
2. Call `verify_company_against_ch("InvalidCompanyName", "00000000")`
3. Verify function returns False for invalid company
4. Test with valid company (e.g., "TESCO", "00445790")
**Expected Output**: Invalid company returns False, valid company returns True
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC15: Incorporation Date Format Validation
**Test Case ID**: FR5-TC15
**Test Case Description**: Verify incorporation date must be in YYYY-MM-DD format
**Test Case Procedure**:
1. Open InlineCompanySignup
2. Enter invalid date formats: "01/01/2020", "2020-1-1", "20-01-2020"
3. Verify validation at line 91 in pages.py rejects these
4. Enter valid format "2020-01-01"
**Expected Output**: Invalid formats rejected with error "Date must be YYYY-MM-DD", valid format accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC16: Incorporation Date Range Validation
**Test Case ID**: FR5-TC16
**Test Case Description**: Verify incorporation date must be between 1850 and today
**Test Case Procedure**:
1. Open InlineCompanySignup
2. Test date "1800-01-01" (too old)
3. Test future date "2026-12-31"
4. Verify validation at lines 96-106 rejects both
**Expected Output**: Error message "Date must be between 1850 and today's date"
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR6: Edit Stock Details

#### TC17: Stock Update Function Exists
**Test Case ID**: FR6-TC17
**Test Case Description**: Verify stock update functionality (Note: May not be implemented)
**Test Case Procedure**:
1. Check db.py for stock update function
2. Check stock_market.py for edit UI
3. Document findings
**Expected Output**: Stock update function allows editing ticker, name, sector, shares, valuation
**Actual Result**: _(To be filled during testing - currently NOT implemented per code review)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR7: Remove Stock Listing

#### TC18: Stock Deletion Function
**Test Case ID**: FR7-TC18
**Test Case Description**: Verify stock can be deleted from database
**Test Case Procedure**:
1. Import db module
2. Create test stock with `stock_create_from_application()`
3. Call `stock_delete(stock_id)`
4. Query stock table to verify stock no longer exists
5. Verify CASCADE delete removed associated price history
**Expected Output**: Stock record deleted along with all price history records
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR8: View All Active Stock Listings

#### TC19: Retrieve All Stocks
**Test Case ID**: FR8-TC19
**Test Case Description**: Verify system retrieves all stocks with prices and sectors
**Test Case Procedure**:
1. Import db module
2. Create multiple test stocks in different sectors
3. Call `stocks_all()`
4. Verify returned list includes stock_id, ticker, current_price, and sector_name
**Expected Output**: List of all stocks with id, ticker, price, and sector information
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR9-FR13: Stock Analysis Functions

#### TC20: Time-framed Returns Calculation (1 Month)
**Test Case ID**: FR9-TC20
**Test Case Description**: Verify 1-month return calculation is accurate
**Test Case Procedure**:
1. Import db module
2. Create stock with known price history
3. Call `stock_calculate_return(stock_id, months=1)`
4. Manually calculate expected return: ((price_now - price_30days_ago) / price_30days_ago) * 100
5. Compare function output to manual calculation
**Expected Output**: Return percentage matches manual calculation within 0.01%
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC21: Time-framed Returns Calculation (6 Months)
**Test Case ID**: FR9-TC21
**Test Case Description**: Verify 6-month return calculation is accurate
**Test Case Procedure**:
1. Import db module
2. Create stock with known price history
3. Call `stock_calculate_return(stock_id, months=6)`
4. Manually calculate expected return: ((price_now - price_180days_ago) / price_180days_ago) * 100
5. Compare function output to manual calculation
**Expected Output**: Return percentage matches manual calculation within 0.01%
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC22: Time-framed Returns Calculation (1 Year)
**Test Case ID**: FR9-TC22
**Test Case Description**: Verify 1-year return calculation is accurate
**Test Case Procedure**:
1. Import db module
2. Create stock with known price history
3. Call `stock_calculate_return(stock_id, months=12)`
4. Manually calculate expected return: ((price_now - price_365days_ago) / price_365days_ago) * 100
5. Compare function output to manual calculation
**Expected Output**: Return percentage matches manual calculation within 0.01%
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC23: 24-Hour Change Calculation
**Test Case ID**: FR9-TC23
**Test Case Description**: Verify 24-hour price change calculation
**Test Case Procedure**:
1. Import db module
2. Create stock with known prices for today and yesterday
3. Call `stock_calculate_24hr_change(stock_id)`
4. Manually calculate: ((today_price - yesterday_price) / yesterday_price) * 100
5. Compare results
**Expected Output**: 24hr change percentage matches manual calculation
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR2: Data Integrity Validation

#### TC24: Positive Shares Validation
**Test Case ID**: NR2-TC24
**Test Case Description**: Verify shares outstanding must be positive
**Test Case Procedure**:
1. Import db module
2. Attempt to insert stock with shares_outstanding = 0 or negative value
3. Verify CHECK constraint prevents insertion
**Expected Output**: Database CHECK constraint error raised
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC25: Positive Valuation Validation
**Test Case ID**: NR2-TC25
**Test Case Description**: Verify total valuation must be positive
**Test Case Procedure**:
1. Import db module
2. Attempt to insert stock with total_valuation = 0 or negative value
3. Verify CHECK constraint prevents insertion
**Expected Output**: Database CHECK constraint error raised
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC26: Positive Price Validation
**Test Case ID**: NR2-TC26
**Test Case Description**: Verify stock prices must be positive
**Test Case Procedure**:
1. Import db module
2. Attempt to insert stock_price record with price <= 0
3. Verify CHECK constraint prevents insertion
**Expected Output**: Database CHECK constraint error raised
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR7: Reliability - Deterministic Calculations

#### TC27: Return Calculation Consistency
**Test Case ID**: NR7-TC27
**Test Case Description**: Verify return calculations are repeatable with same input
**Test Case Procedure**:
1. Import db module
2. Create stock with fixed price history
3. Call `stock_calculate_return(stock_id, months=6)` ten times
4. Verify all results are identical
**Expected Output**: All ten calculations return exact same percentage
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## INTEGRATION TESTING

### FR1-FR3: Application Workflow Integration

#### TC28: End-to-End Application Submission and Approval
**Test Case ID**: FR1-FR2-INT-TC28
**Test Case Description**: Verify complete workflow from submission to approval with database persistence
**Test Case Procedure**:
1. Login as company user
2. Navigate to ApplicationFormPage
3. Fill all application fields with valid data
4. Attach required documents
5. Submit application
6. Verify application appears in database with status='pending'
7. Login as manager user
8. Open ManagerPortalPage
9. Verify application appears in pending list
10. Select application and click "Approve"
11. Verify application status changes to 'approved' in database
12. Verify stock is created in stock table
**Expected Output**: Application successfully moves from pending to approved, stock created
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC29: End-to-End Application Submission and Rejection
**Test Case ID**: FR1-FR3-INT-TC29
**Test Case Description**: Verify complete workflow from submission to rejection with notes
**Test Case Procedure**:
1. Login as company user
2. Submit application with all required data
3. Verify application stored in database
4. Login as manager user
5. Open ManagerPortalPage and view application in pending list
6. Click "Reject" button
7. Enter rejection notes in text box
8. Save rejection
9. Verify application appears in rejected list
10. Verify internal_notes in database contains rejection reason
11. Login as company user
12. Verify application shows in "My Applications" with rejected status
**Expected Output**: Application successfully rejected with notes visible to both manager and company
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR4-FR5: Validation and Compliance Integration

#### TC30: Companies House Integration with Offline Fallback
**Test Case ID**: FR5-INT-TC30
**Test Case Description**: Verify system falls back to offline dataset when API unavailable
**Test Case Procedure**:
1. Disable network connection or remove API key
2. Open InlineCompanySignup form
3. Enter valid company name and number from offline dataset
4. Submit registration
5. Verify `verify_company_against_ch()` uses offline CSV/ZIP lookup
6. Verify registration succeeds with offline validation
**Expected Output**: System validates company using offline dataset when API fails
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC31: Attachment Storage and Retrieval
**Test Case ID**: FR4-INT-TC31
**Test Case Description**: Verify documents attached to applications are stored and retrievable
**Test Case Procedure**:
1. Login as company user
2. Create application and attach PDF file
3. Submit application
4. Verify file is copied to data/attachments/ directory
5. Verify attachment record created in database with correct file_path
6. Login as manager
7. View application details
8. Verify attachments are listed
9. Click "Open" button to view attachment
10. Verify file opens correctly
**Expected Output**: Attachments stored in filesystem, tracked in database, and openable from manager view
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR6-FR7: Stock CRUD Integration

#### TC32: Stock Deletion Cascade to Prices
**Test Case ID**: FR7-INT-TC32
**Test Case Description**: Verify deleting stock also removes all price history
**Test Case Procedure**:
1. Login as manager
2. Create stock from approved application (generates 366 price records)
3. Query stock_price table to confirm prices exist
4. Navigate to StockMarketPage
5. Select stock checkbox
6. Click "Delete Selected" button
7. Confirm deletion
8. Query stock table to verify stock removed
9. Query stock_price table to verify all associated prices removed via CASCADE
**Expected Output**: Stock and all 366 price records deleted from database
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR8: Stock Listing with Filtering

#### TC33: Sector Filter Application
**Test Case ID**: FR8-INT-TC33
**Test Case Description**: Verify sector filter correctly filters displayed stocks
**Test Case Procedure**:
1. Login as manager
2. Create stocks in multiple sectors (Technology, Healthcare, Finance)
3. Navigate to StockMarketPage
4. Verify all stocks displayed initially
5. Click "Filter by Sector" button
6. Select only "Technology" checkbox
7. Click "Apply Filter"
8. Verify only Technology sector stocks displayed in treeview
9. Click "Clear Filter"
10. Verify all stocks displayed again
**Expected Output**: Filter shows only selected sectors, clear filter shows all stocks
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC34: Multi-Sector Filter
**Test Case ID**: FR8-INT-TC34
**Test Case Description**: Verify multiple sectors can be selected simultaneously
**Test Case Procedure**:
1. Create stocks in Technology, Healthcare, Finance, Energy sectors
2. Open StockMarketPage
3. Click "Filter by Sector"
4. Select "Technology" and "Healthcare" checkboxes
5. Apply filter
6. Verify only Technology and Healthcare stocks displayed
7. Count stocks to ensure correct number shown
**Expected Output**: Only stocks from selected sectors (Technology and Healthcare) are visible
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR9: Multi-Stock Selection for Analysis

#### TC35: Select Multiple Stocks for Analysis
**Test Case ID**: FR9-INT-TC35
**Test Case Description**: Verify multiple stocks can be selected via checkboxes
**Test Case Procedure**:
1. Login as manager
2. Navigate to StockMarketPage
3. Click checkboxes for 3 different stocks
4. Verify stocks added to `self.selected_stocks` set
5. Click "Select All" button
6. Verify all stocks selected
7. Click "Deselect All" button
8. Verify all stocks deselected
**Expected Output**: Checkbox interface correctly tracks selected stocks
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR10-FR13: Analysis Report Generation

#### TC36: Time-framed Returns Report Generation
**Test Case ID**: FR10-INT-TC36
**Test Case Description**: Verify time-framed returns report displays correct data for selected stocks
**Test Case Procedure**:
1. Login as manager
2. Create 3 test stocks with known price histories
3. Select all 3 stocks via checkboxes
4. Click "Analysis" menu
5. Click "Time-framed Returns"
6. Verify report window opens
7. Verify report shows 1M, 6M, 1Y returns for all 3 stocks
8. Manually verify calculations are correct
9. Click "Save as TXT" button
10. Verify report exported to file
**Expected Output**: Report displays correct returns for all selected stocks, exportable to TXT
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC37: Valuation Comparison Report
**Test Case ID**: FR11-INT-TC37
**Test Case Description**: Verify valuation comparison shows current values and growth
**Test Case Procedure**:
1. Login as manager
2. Select multiple stocks
3. Click Analysis → Valuation Comparison
4. Verify report shows: ticker, current price, total valuation, shares, 1Y growth
5. Manually verify: total_valuation = current_price × shares_outstanding
6. Verify report is exportable
**Expected Output**: Report shows accurate valuation calculations and growth percentages
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC38: Sector Benchmarking Report
**Test Case ID**: FR12-INT-TC38
**Test Case Description**: Verify sector benchmarking compares stock to sector average
**Test Case Procedure**:
1. Create 5 stocks: 3 in Technology sector, 2 in Healthcare
2. Login as manager and navigate to StockMarketPage
3. Select all 5 stocks
4. Click Analysis → Sector Benchmarking
5. Verify report calculates average 1Y return for Technology sector
6. Verify report calculates average 1Y return for Healthcare sector
7. Verify each stock shows difference from its sector average
8. Manually verify calculations are correct
**Expected Output**: Each stock compared to its own sector average, differences shown
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC39: Performance Consistency Score Calculation
**Test Case ID**: FR13-INT-TC39
**Test Case Description**: Verify consistency score based on return variance
**Test Case Procedure**:
1. Create 2 test stocks:
   - Stock A: 1M=5%, 6M=5.5%, 1Y=6% (low variance)
   - Stock B: 1M=20%, 6M=-10%, 1Y=5% (high variance)
2. Select both stocks
3. Click Analysis → Performance Consistency
4. Verify Stock A has higher consistency score
5. Verify score calculation: 100 - variance
6. Manually calculate variance and verify
**Expected Output**: Low variance stock has score near 100, high variance stock has lower score
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC40: Market Report Generation (No Selection Required)
**Test Case ID**: FR13-INT-TC40
**Test Case Description**: Verify market report analyzes entire market regardless of selection
**Test Case Procedure**:
1. Create stocks across multiple sectors
2. Login as manager
3. Navigate to StockMarketPage (do NOT select any stocks)
4. Click Analysis → Generate Market Report
5. Verify report shows:
   - Total companies listed
   - Total market valuation (sum of all stocks)
   - Average valuation
   - Sector-wise distribution with percentages
6. Manually verify calculations
**Expected Output**: Report analyzes all stocks in database, not just selected ones
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR1: Privacy - Data Handling

#### TC41: Password Hashing on Storage
**Test Case ID**: NR1-INT-TC41
**Test Case Description**: Verify passwords are hashed before storage
**Test Case Procedure**:
1. Register new company user with password "TestPass123"
2. Open data/users.txt file
3. Verify password is NOT stored in plain text
4. Verify password is SHA256 hashed (64-character hex string)
5. Attempt login with "TestPass123"
6. Verify login succeeds (hash verification works)
**Expected Output**: Passwords stored as SHA256 hash, not plain text
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR3: Availability - Database Connection

#### TC42: Database Initialization on Startup
**Test Case ID**: NR3-INT-TC42
**Test Case Description**: Verify database and tables are created if missing
**Test Case Procedure**:
1. Delete data/mseg.db file if exists
2. Run main.py
3. Verify db.initialize_db() creates new database
4. Verify all tables created: sector, company, application, stock, stock_price, attachment
5. Verify 10 sectors are pre-populated
6. Verify foreign key enforcement is enabled
**Expected Output**: Database and all tables created automatically on first run
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## SYSTEM TESTING

### FR1-FR3: Complete Application Review Workflow

#### TC43: Company Submits Application - Manager Approves - Stock Appears
**Test Case ID**: FR1-FR2-SYS-TC43
**Test Case Description**: End-to-end system test of successful application flow
**Test Case Procedure**:
1. Launch MSEG application (python main.py)
2. Click "Sign Up" as company
3. Fill all registration fields with valid data:
   - Company Name: "Test Industries Ltd"
   - Registration Number: "12345678"
   - Username: "testco"
   - Password: "Pass1234"
   - Incorporation Date: "2020-01-01"
4. Submit registration
5. Login with new credentials
6. Navigate to "My Applications" page
7. Fill application form:
   - Ticker: "TEST"
   - Shares: 1000000
   - Valuation: 500000000
   - Sector: Technology
8. Attach at least one PDF document
9. Submit application
10. Verify success message appears
11. Logout
12. Login as manager (manager1/pass123)
13. Verify "Test Industries Ltd" application appears in Pending list
14. Click on application to view details
15. Verify all data is correct
16. Click "Approve" button
17. Verify application moves to Approved list
18. Navigate to Stock Market page
19. Verify "TEST" stock appears in listing with correct data
20. Verify 24hr, 1M, 6M, 1Y returns are displayed
21. Logout and login as testco
22. Navigate to Stock Market
23. Verify TEST stock is visible in read-only mode
**Expected Output**: Complete workflow from registration → application → approval → stock listing succeeds
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC44: Company Submits Application - Manager Rejects - No Stock Created
**Test Case ID**: FR1-FR3-SYS-TC44
**Test Case Description**: End-to-end system test of application rejection flow
**Test Case Procedure**:
1. Launch MSEG application
2. Login as existing company user
3. Submit new application with ticker "RJCT"
4. Logout and login as manager
5. Select application from Pending list
6. Click "Reject" button
7. Enter rejection reason: "Stage 2 - Regulatory Compliance Failed: Company does not meet activity duration requirement"
8. Click "Save Rejection"
9. Verify application moves to Rejected list
10. Navigate to Stock Market page
11. Verify "RJCT" stock does NOT appear in listing
12. Logout and login as company
13. Navigate to My Applications
14. Verify application shows rejected status
15. Select rejected application
16. Verify rejection notes are visible (if UI supports this)
**Expected Output**: Rejected application does not create stock, rejection notes recorded
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR4-FR5: Validation and Compliance System Tests

#### TC45: Duplicate Ticker Submission Blocked
**Test Case ID**: FR4-SYS-TC45
**Test Case Description**: Verify system prevents duplicate ticker at submission time
**Test Case Procedure**:
1. Login as manager and create stock with ticker "DUPL"
2. Logout and login as company
3. Navigate to application form
4. Fill form with ticker "DUPL"
5. Attempt to submit
6. Verify error message: "Ticker DUPL is already in use"
7. Verify application is NOT submitted
8. Change ticker to "UNIQ"
9. Submit successfully
**Expected Output**: Duplicate ticker rejected at form validation, unique ticker accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC46: Unrealistic Valuation Blocked
**Test Case ID**: FR4-SYS-TC46
**Test Case Description**: Verify valuations outside 100M-500B range are rejected
**Test Case Procedure**:
1. Login as company
2. Create application with valuation 50,000,000 (50M - too low)
3. Attempt to submit
4. Verify error: "Total valuation must be at least 100 million"
5. Change valuation to 600,000,000,000 (600B - too high)
6. Attempt to submit
7. Verify error: "Total valuation must not exceed 500 billion"
8. Change valuation to 250,000,000 (250M - valid)
9. Submit successfully
**Expected Output**: Out-of-range valuations rejected, valid valuation accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC47: Company Registration with Invalid Incorporation Date
**Test Case ID**: FR5-SYS-TC47
**Test Case Description**: Verify company registration validates incorporation date
**Test Case Procedure**:
1. Launch application
2. Click "Sign Up" as company
3. Fill all fields, set incorporation date to 2023-01-01 (less than 3 years ago)
4. Attempt to submit
5. Verify error: "Company must be incorporated at least 3 years ago"
6. Change date to 2020-01-01 (valid)
7. Submit successfully
8. Verify company account created
**Expected Output**: Recent incorporation date rejected, older date accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC48: Companies House Verification (Online API)
**Test Case ID**: FR5-SYS-TC48
**Test Case Description**: Verify online Companies House API verification works
**Test Case Procedure**:
1. Ensure API key is configured in data/ch_api_key.txt
2. Ensure internet connection available
3. Launch application and click "Sign Up"
4. Enter invalid company name "NonexistentCompanyXYZ123" and number "00000000"
5. Attempt to submit registration
6. Verify error: "Company not found in Companies House registry"
7. Enter valid company: "TESCO PLC" and "00445790"
8. Submit successfully
**Expected Output**: Invalid company rejected by API, valid company accepted
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC49: Companies House Verification (Offline Fallback)
**Test Case ID**: FR5-SYS-TC49
**Test Case Description**: Verify offline dataset validation when API unavailable
**Test Case Procedure**:
1. Remove API key file or disable internet
2. Ensure offline dataset exists in data/companies_house_offline/
3. Launch application and click "Sign Up"
4. Enter company name and number from offline dataset
5. Submit registration
6. Verify system uses offline validation (check console output)
7. Verify registration succeeds
**Expected Output**: System falls back to offline dataset when API unavailable
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR6-FR7: Stock Management System Tests

#### TC50: Delete Stock with Confirmation
**Test Case ID**: FR7-SYS-TC50
**Test Case Description**: Verify stock deletion requires confirmation and removes stock
**Test Case Procedure**:
1. Login as manager
2. Navigate to Stock Market page
3. Verify at least one stock exists
4. Select stock checkbox
5. Click "Delete Selected" button
6. Verify confirmation dialog appears asking to confirm deletion
7. Click "Cancel"
8. Verify stock is NOT deleted
9. Select stock again
10. Click "Delete Selected"
11. Click "Yes" to confirm
12. Verify success message appears
13. Verify stock no longer appears in listing
14. Refresh page
15. Verify stock still deleted (persistent)
**Expected Output**: Deletion requires confirmation, successfully removes stock from system
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC51: Delete Multiple Stocks Simultaneously
**Test Case ID**: FR7-SYS-TC51
**Test Case Description**: Verify multiple stocks can be deleted at once
**Test Case Procedure**:
1. Login as manager
2. Create 3 test stocks: "DEL1", "DEL2", "DEL3"
3. Navigate to Stock Market page
4. Select checkboxes for all 3 stocks
5. Click "Delete Selected"
6. Confirm deletion
7. Verify all 3 stocks removed from listing
8. Query database to verify all 3 deleted
**Expected Output**: All selected stocks deleted in single operation
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR8: Stock Listing and Filtering System Tests

#### TC52: Stock Listing Displays All Fields
**Test Case ID**: FR8-SYS-TC52
**Test Case Description**: Verify stock listing table shows all required information
**Test Case Procedure**:
1. Login as manager
2. Create stock with known values
3. Navigate to Stock Market page
4. Verify table columns: Ticker, Price, Sector, 24hr %, 1M %, 6M %, 1Y %
5. Verify all data displays correctly for created stock
6. Verify price formatted with 2 decimal places
7. Verify percentages show + or - signs
8. Verify color coding: green for positive returns, red for negative
**Expected Output**: Stock listing displays all fields with proper formatting and color coding
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC53: Filter by Single Sector
**Test Case ID**: FR8-SYS-TC53
**Test Case Description**: Verify sector filtering works correctly for single sector
**Test Case Procedure**:
1. Login as manager
2. Create stocks in multiple sectors: Technology (2), Healthcare (1), Finance (1)
3. Navigate to Stock Market page
4. Verify all 4 stocks displayed
5. Click "Filter by Sector" button
6. Select only "Healthcare" checkbox
7. Click "Apply Filter"
8. Verify only Healthcare stock displayed (1 stock)
9. Verify Technology and Finance stocks hidden
10. Click "Clear Filter"
11. Verify all 4 stocks displayed again
**Expected Output**: Filter correctly shows only Healthcare stocks, clear filter restores all
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC54: Filter by Multiple Sectors
**Test Case ID**: FR8-SYS-TC54
**Test Case Description**: Verify multiple sectors can be filtered simultaneously
**Test Case Procedure**:
1. Create stocks: Technology (2), Healthcare (2), Finance (1), Energy (1)
2. Navigate to Stock Market page
3. Click "Filter by Sector"
4. Select "Technology" and "Finance"
5. Apply filter
6. Verify 3 stocks displayed (2 Technology + 1 Finance)
7. Verify Healthcare and Energy stocks hidden
**Expected Output**: Multiple sector selection shows stocks from all selected sectors
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC55: Stock Listing as Company (Read-Only Mode)
**Test Case ID**: FR8-SYS-TC55
**Test Case Description**: Verify company users see stocks in read-only mode without CRUD buttons
**Test Case Procedure**:
1. Login as company user
2. Navigate to Stock Market page via header menu
3. Verify stock listing displays with all data
4. Verify NO checkboxes appear (read-only mode)
5. Verify NO "Delete Selected" button visible
6. Verify NO "Analysis" menu available
7. Verify Filter by Sector works
8. Attempt to select stock (should not be possible)
**Expected Output**: Company users can view stocks but cannot modify or analyze
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### FR9-FR13: Stock Analysis System Tests

#### TC56: Time-framed Returns Analysis for Multiple Stocks
**Test Case ID**: FR9-SYS-TC56
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

#### TC57: Valuation Comparison Analysis
**Test Case ID**: FR11-SYS-TC57
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

#### TC58: Sector Benchmarking with Mixed Sectors
**Test Case ID**: FR12-SYS-TC58
**Test Case Description**: Verify sector benchmarking with stocks from different sectors
**Test Case Procedure**:
1. Create stocks:
   - Tech A: 1Y return = 10%
   - Tech B: 1Y return = 20%
   - Healthcare A: 1Y return = 5%
   - Healthcare B: 1Y return = 15%
2. Login as manager
3. Select all 4 stocks
4. Click Analysis → Sector Benchmarking
5. Verify report calculates:
   - Technology average = 15% (average of 10% and 20%)
   - Healthcare average = 10% (average of 5% and 15%)
6. Verify each stock shows:
   - Tech A: -5% vs sector (10% - 15%)
   - Tech B: +5% vs sector (20% - 15%)
   - Healthcare A: -5% vs sector (5% - 10%)
   - Healthcare B: +5% vs sector (15% - 10%)
**Expected Output**: Each stock correctly compared to its own sector average
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC59: Performance Consistency Score Interpretation
**Test Case ID**: FR13-SYS-TC59
**Test Case Description**: Verify consistency score correctly identifies stable vs volatile stocks
**Test Case Procedure**:
1. Create 2 stocks:
   - Stable Stock: 1M=5%, 6M=5.2%, 1Y=5.5% (very consistent)
   - Volatile Stock: 1M=30%, 6M=-10%, 1Y=8% (inconsistent)
2. Select both stocks
3. Click Analysis → Performance Consistency
4. Verify Stable Stock has high consistency score (close to 100)
5. Verify Volatile Stock has lower consistency score
6. Verify score formula: 100 - variance
7. Manually calculate variance for both stocks and verify
**Expected Output**: Stable stock has significantly higher consistency score than volatile stock
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC60: Generate Market Report (All Stocks Analysis)
**Test Case ID**: FR13-SYS-TC60
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

### NR1: Privacy and Data Handling

#### TC61: Password Not Visible in UI
**Test Case ID**: NR1-SYS-TC61
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

#### TC62: No Sensitive Data in Error Messages
**Test Case ID**: NR1-SYS-TC62
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

### NR2: Data Integrity System Tests

#### TC63: Prevent Negative Stock Values Throughout System
**Test Case ID**: NR2-SYS-TC63
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

### NR3: Availability System Tests

#### TC64: Application Starts Without Errors
**Test Case ID**: NR3-SYS-TC64
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

#### TC65: Database Recovery After Corruption
**Test Case ID**: NR3-SYS-TC65
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

### NR4: Performance System Tests

#### TC66: Stock Listing Load Time
**Test Case ID**: NR4-SYS-TC66
**Test Case Description**: Verify stock listing loads within 2 seconds under normal load
**Test Case Procedure**:
1. Create 100 test stocks with full price history
2. Login as manager
3. Start timer
4. Navigate to Stock Market page
5. Stop timer when all stocks rendered in table
6. Verify load time < 2 seconds
7. Apply filter
8. Verify filter applies within 2 seconds
**Expected Output**: Stock listing with 100 stocks loads and renders within 2 seconds
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC67: Application Review Page Load Time
**Test Case ID**: NR4-SYS-TC67
**Test Case Description**: Verify application review screen loads within 2 seconds
**Test Case Procedure**:
1. Create 50 pending applications
2. Login as manager
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

### NR5: Usability System Tests

#### TC68: Clear Labels and Intuitive Navigation
**Test Case ID**: NR5-SYS-TC68
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

#### TC69: Consistent Filter Behavior Across System
**Test Case ID**: NR5-SYS-TC69
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

#### TC70: Theme Switching (Light/Dark Mode)
**Test Case ID**: NR5-SYS-TC70
**Test Case Description**: Verify theme toggle provides good visibility in both modes
**Test Case Procedure**:
1. Login to application (starts in light mode)
2. Verify all text is readable against light background
3. Click theme toggle button in header
4. Verify application switches to dark mode
5. Verify all text is readable against dark background
6. Verify colors provide good contrast
7. Navigate through different pages
8. Verify theme persists across page changes
9. Toggle back to light mode
10. Verify smooth transition
**Expected Output**: Both themes provide excellent readability and visual comfort
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR6: Scalability System Tests

#### TC71: System Performance with 500 Stocks
**Test Case ID**: NR6-SYS-TC71
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

#### TC72: Database Growth with 1000 Applications
**Test Case ID**: NR6-SYS-TC72
**Test Case Description**: Verify database handles growth in applications and stocks
**Test Case Procedure**:
1. Create script to generate 1000 applications
2. Approve 500 of them (creates 500 stocks with 366 prices each = 183,000 price records)
3. Verify database file size is manageable (< 500MB)
4. Launch application
5. Verify startup time is reasonable
6. Navigate to manager portal
7. Verify pending/approved/rejected lists load
8. Test database query performance with large dataset
**Expected Output**: System scales to 1000 applications and 500 stocks without redesign
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

### NR7: Reliability System Tests

#### TC73: Return Calculation Repeatability
**Test Case ID**: NR7-SYS-TC73
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

#### TC74: Sector Benchmarking Calculation Determinism
**Test Case ID**: NR7-SYS-TC74
**Test Case Description**: Verify sector benchmarking calculations are repeatable
**Test Case Procedure**:
1. Create 5 stocks in Technology sector with known returns
2. Run Sector Benchmarking analysis
3. Record sector average and individual stock differences
4. Run analysis again
5. Verify identical results
6. Add 6th stock to Technology sector
7. Run analysis
8. Verify sector average recalculated correctly
9. Remove 6th stock
10. Verify sector average returns to original value
**Expected Output**: Benchmarking calculations are deterministic and update correctly with data changes
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

#### TC75: Price History Generation Consistency
**Test Case ID**: NR7-SYS-TC75
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

### TC76: Role-Based Access Control
**Test Case ID**: RBAC-SYS-TC76
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

### TC77: Data Persistence Across Sessions
**Test Case ID**: PERSIST-SYS-TC77
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

### TC78: Concurrent User Workflow (Sequential)
**Test Case ID**: CONCURRENT-SYS-TC78
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

### TC79: End-to-End Full System Workflow
**Test Case ID**: E2E-SYS-TC79
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

### TC80: SQL Injection Prevention
**Test Case ID**: SEC-NEG-TC80
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

### TC81: Invalid File Attachment Handling
**Test Case ID**: NEG-TC81
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

### TC82: Boundary Testing - Maximum String Lengths
**Test Case ID**: NEG-TC82
**Test Case Description**: Verify system handles very long input strings
**Test Case Procedure**:
1. Create application with 1000-character company name
2. Attempt to submit
3. Verify system handles appropriately (truncation or validation error)
4. Test with maximum username length (10 chars) and 11 chars
5. Test password with 31 characters (max is 30)
6. Verify appropriate validation messages
**Expected Output**: System enforces reasonable length limits with clear messages
**Actual Result**: _(To be filled during testing)_
**Pass/Fail**: _(To be filled during testing)_

---

## TEST SUMMARY

**Total Test Cases**: 82

### Breakdown by Testing Type:
- **Unit Testing**: 27 test cases (TC1-TC27)
- **Integration Testing**: 15 test cases (TC28-TC42)
- **System Testing**: 38 test cases (TC43-TC80)
- **Negative Testing**: 3 test cases (TC81-TC83)

### Breakdown by Requirement:
- **FR1**: 1 test case
- **FR2**: 3 test cases
- **FR3**: 1 test case
- **FR4**: 6 test cases
- **FR5**: 5 test cases
- **FR6**: 1 test case
- **FR7**: 3 test cases
- **FR8**: 5 test cases
- **FR9-FR13**: 9 test cases
- **NR1**: 3 test cases
- **NR2**: 4 test cases
- **NR3**: 2 test cases
- **NR4**: 2 test cases
- **NR5**: 3 test cases
- **NR6**: 2 test cases
- **NR7**: 3 test cases
- **Cross-functional**: 4 test cases
- **Security**: 3 test cases

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
