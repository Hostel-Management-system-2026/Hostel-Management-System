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

## Follow-up observation — 10–11 November 2026 (complete by sample-count criterion)

A new authenticated observation ran against the local SQLite-backed Django development server, with JWT refresh every four minutes. The CSV reached the required 360 checks. Acceptance for TC-014 is based on the sampled success rate; elapsed time and gaps are retained below as context.

| Metric | Result |
|---|---:|
| Checks recorded | 360 |
| Successful / failed | 360 / 0 |
| Sampled success rate | 100% |
| Wall-clock span, first to last sample | 58,392.8 seconds |
| Sample gaps over 15 seconds | 2 (largest: 54,714.0 seconds) |
| Endpoint latency average / maximum | 19.558 / 264.221 ms |

Raw samples are in `../load_tests/evidence/2026-11-10/availability_1h.csv`; the summary is `../load_tests/evidence/2026-11-10/availability_1h.summary.json`. All 360 recorded checks succeeded, exceeding the 99% sampled target. **TC-014 is complete** by the sample-count and success-rate criterion. The timestamp gaps mean this result does not describe continuous uptime or establish a production SLA.
