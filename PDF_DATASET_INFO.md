# Insurance Claim PDF Dataset

## 📄 Document Information

**File**: `data/insurance_claim_CLM2024001.pdf`

**Format**: PDF (15 pages)

**File Size**: 29 KB

**Claim ID**: CLM-2024-001

---

## 📋 Document Structure

The PDF contains a comprehensive insurance claim report structured across **15 pages** with the following sections:

### Page 1: Title and Overview
- Claim header information
- Policy details table
- Policyholder information

### Pages 2-3: Policy Information (Section 1)
- Coverage details
- **Deductible information** (Collision: $750, Comprehensive: $500)
- Insured vehicle details
- Agent of record

### Pages 3-5: Incident Timeline (Section 2)
- Incident overview (Jan 12, 2024, 7:42 AM)
- Chronological timeline from 7:38 AM - 10:30 AM
- Post-incident timeline (Jan 12 - Feb 28, 2024)
- Detailed minute-by-minute account
- **Timeline spans 47 days** from incident to near-closure

### Pages 6-7: Witness Statements (Section 3)
- Witness #1: Marcus Thompson (bus stop observer)
- Witness #2: Elena Rodriguez (stopped at intersection)
- **Witness #4: Patricia O'Brien (Registered Nurse)** - *Sparse data example*
  - Detailed observation about lighting conditions
  - Professional medical assessment
  - Unique detail about air freshener

### Page 7-8: Medical Documentation (Section 4)
- Emergency Department treatment summary
- Orthopedic follow-up
- Physical therapy course (8 sessions)
- All medical charges

### Pages 8-9: Vehicle Damage Assessment (Section 5)
- Initial damage inspection
- Supplemental damage discovered during tear-down
- **Final repair cost: $17,111.83**

### Page 9: Financial Summary (Section 6)
- **Total claim amount: $23,370.80**
- Breakdown of all costs
- Subrogation information
- Third-party liability (Nationwide Insurance)

### Page 10: Case Notes and Conclusion (Section 7)
- Claims adjuster assessment
- Professional evaluation
- File status and closure information

---

## 🎯 Key Data Points for Needle Queries

### Exact Amounts
- **Collision Deductible: $750** (Page 2)
- **Comprehensive Deductible: $500** (Page 2)
- **Initial Repair Estimate: $12,847.50** (Page 8)
- **Final Repair Cost: $17,111.83** (Page 9)
- **Total Claim Amount: $23,370.80** (Page 9)
- **Rental Cost: $1,402.47** (28 days @ $45/day)
- **Physical Therapy: $1,400.00** (8 sessions @ $175)

### Exact Dates and Times
- **Incident Date: January 12, 2024**
- **Incident Time: 7:42:15 AM** (precise to the second)
- **Claim Filed: January 15, 2024**
- **Repairs Started: January 29, 2024**
- **Repairs Completed: February 15, 2024**
- **Vehicle Returned: February 16, 2024**

### Exact Names
- **Policyholder: Sarah Mitchell**
- **At-Fault Driver: Robert Harrison**
- **Secondary Driver: Jennifer Park**
- **Claims Adjuster: Kevin Park**
- **ER Doctor: Dr. Amanda Foster, MD**
- **Orthopedist: Dr. Rachel Kim, MD**
- **Physical Therapist: Marcus Rodriguez, PT, DPT**
- **Witnesses: Marcus Thompson, Elena Rodriguez, David Chen, Patricia O'Brien**

### Sparse Data (Needle-in-Haystack)
- **Patricia O'Brien's lighting observation** (Page 7):
  - "Street lights were on normal cycle"
  - "Sunrise was at 6:58 AM"
  - "At 7:42 AM there was full daylight"
  - Detail about air freshener ("Pine Forest" scent masking vodka smell)

### Vehicle Details
- **Make/Model: 2021 Honda Accord EX**
- **VIN: 1HGCV1F39LA012345**
- **Mileage: 23,847 miles**
- **Color: Silver Metallic**

### Location
- **Intersection: Wilshire Blvd and Vermont Ave**
- **City: Los Angeles, CA 90005**
- **Repair Shop: Premier Auto Body, 5847 Santa Monica Blvd**
- **Hospital: Cedars-Sinai Medical Center**

---

## 📈 Timeline Queries Support

The document provides excellent support for timeline queries:

1. **Minute-by-minute incident timeline** (7:38 AM - 10:30 AM)
2. **Day-by-day post-incident timeline** (Jan 12 - Feb 28)
3. **Medical treatment timeline** (ED → Orthopedist → Physical Therapy)
4. **Repair timeline** (Assessment → Parts → Repairs → Completion)
5. **Legal timeline** (Arrest → Arraignment → Preliminary hearing)

---

## 🔍 Query Examples This PDF Supports

### Summary Queries
- "What is this insurance claim about?"
- "Summarize the timeline of events"
- "What happened during the accident?"

### Needle Queries
- "What was the exact collision deductible?" → **$750**
- "At what time did the accident occur?" → **7:42:15 AM**
- "Who was the claims adjuster?" → **Kevin Park**
- "What was the final repair cost?" → **$17,111.83**
- "How many physical therapy sessions?" → **8 sessions**

### Sparse Data Queries
- "What did Patricia O'Brien observe about lighting conditions?" → **Sunrise 6:58 AM, full daylight at 7:42 AM**
- "What unique detail did Patricia O'Brien notice?" → **Pine Forest air freshener masking vodka smell**

### Computation Queries (MCP)
- "How many days between incident and filing?" → **3 days** (Jan 12 → Jan 15)
- "How many days for repairs?" → **18 days** (Jan 29 → Feb 15)
- "What's the out-of-pocket after deductible?" → **$750**

### Hybrid Queries
- "Summarize medical treatment and provide exact number of PT sessions" → **Whiplash treated with 8 PT sessions over 4 weeks**
- "What happened and what was the total cost?" → **T-bone collision by DUI driver, total claim $23,370.80**

---

## 🛠️ Technical Details

### PDF Generation
- Generated using **reportlab** Python library
- Professional formatting with tables, headers, and structured sections
- Automatic page breaks for optimal readability
- Includes metadata for document type and claim information

### Text Extraction
- System uses **pypdf** library to extract text
- Page markers preserved during extraction
- Section headers maintained for parsing
- Supports both PDF and text formats seamlessly

### Document Processing
- PDF loaded by `InsuranceClaimLoader` class
- Automatic detection of PDF vs text files
- Sections parsed using regex patterns
- Metadata extracted for each section

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Total Pages** | 15 |
| **Total Words** | ~8,500 |
| **Total Sections** | 7 major sections |
| **Timeline Span** | 47 days |
| **Witness Statements** | 4 witnesses |
| **Medical Events** | 10+ documented |
| **Financial Transactions** | 8 major line items |
| **Named Individuals** | 15+ people |
| **Exact Dates** | 20+ specific dates |
| **Dollar Amounts** | 15+ precise amounts |

---

## ✅ Assignment Requirements Met

✅ **10+ pages**: PDF contains **15 pages**
✅ **Timeline-based**: Comprehensive 47-day timeline from incident to resolution
✅ **Sparse data**: Patricia O'Brien's lighting observation and air freshener detail
✅ **Multiple sections**: 7 major sections with subsections
✅ **Rich metadata**: Dates, amounts, names, locations, VINs, etc.
✅ **Professional format**: PDF format with proper structure and formatting

---

**The PDF document provides a complete, realistic insurance claim that supports all system capabilities including summary queries, needle queries, timeline reconstruction, and sparse data retrieval.**
