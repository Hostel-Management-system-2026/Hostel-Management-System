# Staff usability validation protocol

**Requirement:** NFR-04  
**Test case:** TC-015  
**Target:** At least 90% of assigned staff tasks completed successfully without prior technical training.

## Participants and scoring

- Recruit at least five hostel staff members who did not build or test the project. Include staff who use complaint, visitor, or leave workflows in their work.
- Give each participant the same eight tasks below, in order, without demonstrating the interface or explaining the navigation.
- Record one binary result per task. A task passes only when the participant completes the requested outcome without facilitator help. Record help requests, wrong turns, and time separately.
- With five participants, there are 40 task attempts. The acceptance threshold is at least 36 successful tasks: `successful tasks / attempted tasks × 100 >= 90%`.
- Use participant codes P01–P05. Do not record names, student information, or credentials in the results file.

## Task card

Prepare a Warden account and synthetic records before each session: one open complaint, visitor details for the participant to enter, one checked-in visitor, and two pending leave requests. Reset the records between participants. Do not pre-create the arrival the participant must record.

1. Sign in to the Warden workspace.
2. Open the complaints list and locate the supplied open complaint.
3. Change that complaint to **In Progress**.
4. Mark the same complaint **Resolved**.
5. Open visitor management and register the supplied visitor's arrival.
6. Find the supplied checked-in visitor and record the departure.
7. Open leave requests and approve the supplied pending request.
8. Reject the other supplied pending request.

If a workflow cannot be prepared or a task is not supported by the current application, mark it **Not testable**, explain why, and do not count it as a success. Keep the denominator and report the resulting limitation.

## Results sheet

| Participant | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | Successful / attempted | Help or observed issue |
|---|---|---|---|---|---|---|---|---|---:|---|
| P01 |  |  |  |  |  |  |  |  |  |  |
| P02 |  |  |  |  |  |  |  |  |  |  |
| P03 |  |  |  |  |  |  |  |  |  |  |
| P04 |  |  |  |  |  |  |  |  |  |  |
| P05 |  |  |  |  |  |  |  |  |  |  |

For each attempted task, mark `Pass`, `Fail`, or `Not testable`. Preserve the completed anonymized sheet and report the participant count, task count, completion percentage, and recurring issues. The protocol and workflow are **ready for testing**; TC-015 results remain pending until five independent staff complete the sessions.
