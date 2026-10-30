# Sprint 2 – Staff Usability Test Report

## 1. Test Information

- **Issue:** #22 – Validate staff usability without prior training
- **Requirement:** NFR-04
- **Test Case:** TC-015
- **Environment:** Local development environment
- **Test date:** 30 October 2026
- **Test type:** Preliminary self-usability walkthrough
- **Test role:** WARDEN

## 2. Test Objectives

Evaluate whether the Hostel Management System provides accessible workflows for hostel staff to manage complaints and visitor records.

## 3. Test Results

| No. | Task | Result |
|---|---|---|
| 1 | Log in using WARDEN account | Passed |
| 2 | Open and view complaints | Passed |
| 3 | Register a visitor arrival | Passed |
| 4 | Record visitor departure | Passed |
| 5 | Open leave requests page | Page loaded; no records available |
| 6 | View a student complaint | Passed |
| 7 | Change complaint status to IN_PROGRESS | Passed |
| 8 | Change complaint status to RESOLVED | Passed |

## 4. Observations

- The WARDEN dashboard loaded successfully.
- The complaints page displayed student complaints.
- Visitor registration successfully recorded visitor details.
- Visitor departure successfully changed the visitor status to CHECKED OUT.
- Complaint status transitions from OPEN to IN_PROGRESS and RESOLVED worked successfully.
- The leave requests page loaded but contained no records.

## 5. Limitations

- Testing was performed by one person using a local development environment.
- No independent hostel staff or simulated staff participants were involved.
- The formal participant-based usability acceptance target of at least 90% task completion has not been validated.
- No production usability conclusions can be drawn from this test.

## 6. Conclusion

The preliminary self-usability walkthrough successfully verified several important WARDEN workflows, including visitor management and complaint resolution.

However, formal staff usability validation remains pending. Additional participant testing is required before claiming that the NFR-04 acceptance criteria have been met.
