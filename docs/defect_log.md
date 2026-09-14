# TrackMate Defect Log

| ID     | Summary                                                                      | Severity / Priority | Status |
| ------ | ---------------------------------------------------------------------------- | ------------------- | ------ |
| BUG-01 | An accepted friendship could be deleted through the reject-request endpoint. | High / High         | Fixed  |
| BUG-02 | A completed or pending-review task accepted another proof submission.        | High / High         | Fixed  |
| BUG-03 | Deleting a goal left its locally stored proof images behind.                 | Medium / Medium     | Fixed  |
| BUG-04 | Task weight `0` showed required instead of the numeric range error.          | Low / Medium        | Fixed  |

## BUG-01 — Accepted friendship treated as rejectable request

- Preconditions: two users have an accepted friendship.
- Reproduction: the receiver posts to `/friends/reject/<friendship_id>`.
- Expected: only a `PENDING` request can be rejected; accepted friendship remains.
- Actual: the endpoint deleted the accepted friendship.
- Root cause: `reject_request` checked the receiver but not friendship status.
- Fix: return HTTP 400 unless status is `PENDING`.
- Regression: `test_accepted_friendship_cannot_be_rejected_as_pending`.

## BUG-02 — Proof submission after task review

- Preconditions: task proof has been approved or is pending review.
- Reproduction: owner submits another proof for the same task.
- Expected: task cannot accept a new proof outside `ACTIVE` state.
- Actual: submission could overwrite a completed task's state with `PENDING_REVIEW`.
- Root cause: submission checked only for a pending proof, not task state.
- Fix: allow submission only when `task.status == "ACTIVE"`.
- Regression: `test_completed_task_cannot_receive_another_proof` covers both pending-review and completed task states.

## BUG-03 — Orphaned local proof files

- Preconditions: a goal has a proof image in local storage.
- Reproduction: delete the goal.
- Expected: the related local file is removed with its database record.
- Actual: the database proof was deleted but the image file remained.
- Root cause: goal deletion removed ORM records only.
- Fix: remove the stored filename from `PROOF_UPLOAD_FOLDER` before deleting the proof record.
- Regression: `test_deleting_goal_removes_local_proof_file`.

## BUG-04 — Misleading zero-weight validation

- Preconditions: task creation form with weight `0`.
- Reproduction: submit weight `0`.
- Expected: range validation reports that weight must be 1–100.
- Actual: `DataRequired` treated numeric zero as absent and reported a required field.
- Root cause: `DataRequired` is unsuitable for a numeric zero boundary.
- Fix: use `InputRequired` before `NumberRange`.
- Regression: `test_task_weight_boundaries`.
