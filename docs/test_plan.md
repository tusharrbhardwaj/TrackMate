# TrackMate Test Plan

## Scope and environment

Tests use Flask's test client, an isolated temporary SQLite database, and a temporary local proof-upload directory. They do not require Supabase credentials, a network connection, or a browser.

| ID    | Objective                                          | Technique                         | Level       | Expected result                                             |
| ----- | -------------------------------------------------- | --------------------------------- | ----------- | ----------------------------------------------------------- |
| TC-01 | Register with valid data                           | Equivalence partitioning          | Integration | User is persisted and registration succeeds.                |
| TC-02 | Reject invalid registration email                  | Equivalence partitioning          | Integration | Email validation error is shown.                            |
| TC-03 | Reject password confirmation mismatch              | Equivalence partitioning          | Integration | Confirmation validation error is shown.                     |
| TC-04 | Log in with valid credentials                      | Equivalence partitioning          | Integration | Authenticated session is created.                           |
| TC-05 | Reject unknown login identifier                    | Equivalence partitioning          | Integration | Generic invalid-credentials message is shown.               |
| TC-06 | Protect the home route                             | Access-control partitioning       | Integration | Anonymous user is redirected to login.                      |
| TC-07 | Create a valid goal for its owner                  | Equivalence partitioning          | Integration | Goal is stored with the current owner.                      |
| TC-08 | Reject an empty goal title                         | Equivalence partitioning          | Integration | Required-field validation is shown.                         |
| TC-09 | Deny another user access to a goal                 | Access-control partitioning       | Integration | Route returns 403.                                          |
| TC-10 | Create task weights 0, 1, 100 and 101              | Boundary value analysis           | Integration | Only 1 and 100 are accepted.                                |
| TC-11 | Allocate 99+1 and then add 1 more                  | Boundary value analysis           | Integration | 100 is accepted; 101 total is rejected.                     |
| TC-12 | Submit proof explanations of 99, 100 and 101 words | Boundary value analysis           | Integration | 99 is rejected; 100 and 101 are accepted.                   |
| TC-13 | Reject a GIF proof file                            | Equivalence partitioning          | Integration | File-extension validation is shown.                         |
| TC-14 | Reject a second proof during review                | State transition                  | Integration | Task remains unavailable for submission.                    |
| TC-15 | Send, accept and protect a friendship              | State transition                  | Integration | Accepted friendship cannot be rejected as pending.          |
| TC-16 | Approve a pending proof as supervisor              | Decision table / state transition | System      | Proof is approved, task completes, owner gains rating.      |
| TC-17 | Reject a pending proof as supervisor               | Decision table / state transition | Integration | Proof is rejected, task becomes active, owner loses rating. |
| TC-18 | Attempt approval as a non-supervisor               | Decision table                    | Integration | Route returns 403.                                          |
| TC-19 | Delete a goal with a local proof image             | Regression                        | Integration | Database records and local proof file are deleted.          |
| TC-20 | Test `trackmate_lib` access/allocation rules       | Unit testing                      | Unit        | Services raise or return the expected domain results.       |
