## 1. Test Information

- **Issue:** #21 – Measure and meet the availability target
- **Requirement:** NFR-03
- **Test Case:** TC-014
- **Environment:** Local development environment
- **Monitoring source:** Local Django API
- **Endpoint:** `/api/v1/complaints`
- **Monitoring interval:** Approximately 10 seconds
- **Number of checks:** 100
- **Measured observation span:** 992 seconds (based on CSV timestamps)

## 2. Test Results

| Metric | Result |
|---|---:|
| Total API checks | 100 |
| Successful checks | 100 |
| Failed checks | 0 |
| Sampled success rate | 100% |
| Required target | 99% |

## 3. Monitoring Method

The authenticated Complaints API endpoint was monitored from the local development environment using HTTP GET requests and JWT Bearer authentication. Access tokens were refreshed during the test to avoid authentication expiry affecting the results.

The CSV timestamps span approximately 992 seconds from the first recorded check to the last recorded check.

## 4. Conclusion and Limitations

All 100 sampled API checks returned successful responses during this local test.

The sampled success rate was 100%. This is preliminary local evidence only. It does not demonstrate sustained availability or establish that the production availability target of 99% has been met.

The observation period and monitoring method should be formally agreed with the project team before treating this as final NFR-03 acceptance evidence.
