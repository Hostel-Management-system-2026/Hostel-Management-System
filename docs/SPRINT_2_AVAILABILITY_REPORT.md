# Sprint 2 – Availability Test Report

## 1. Test Information

- **Issue:** #21 – Measure and meet the availability target
- **Requirement:** NFR-03
- **Test Case:** TC-014
- **Environment:** Local development environment
- **Observation period:** 1,000 seconds (16 minutes, 40 seconds)
- **Monitoring interval:** 10 seconds

## 2. Test Results

| Metric | Result |
|---|---:|
| Total API checks | 100 |
| Successful checks | 100 |
| Failed checks | 0 |
| Measured availability | 100% |
| Required availability | 99% |
| Result | PASSED |

## 3. Calculation

Availability = (Successful checks / Total checks) × 100

Availability = (100 / 100) × 100 = **100%**

## 4. Authentication Handling

JWT authentication was used to access the Complaints API. Access tokens were refreshed during the test to prevent token expiry from being incorrectly counted as service downtime.

## 5. Evidence

Detailed check timestamps, response times, and outcomes are recorded in:

`backend/availability_results_corrected.csv`

## 6. Conclusion

The local API availability test achieved 100% successful responses across 100 checks, exceeding the 99% target during the measured observation period.

**Limitation:** This result represents a local development test only. It does not establish long-term or production availability.
