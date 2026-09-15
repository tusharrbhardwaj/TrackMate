TRACKMATE

TrackMate is a web-based goal and progress tracking application developed as a university Software Design and Modelling project.
It allows users to create goals, divide them into weighted tasks, track their progress, and work with friends who can supervise goals and review submitted proof.

=========================================================

Features:

- Authentication
- User registration and login
- Login using username or email
- Secure password hashing
- User session management
- Goal Management
- Friendship Management
- Create and delete personal goals
- Add descriptions and tasks to goals
- Assign percentage weights to tasks
- Track progress based on completed task weights
- Assign a friend as a goal supervisor
- Submit task completion proof
- Approve / Reject the proof
- User rating
- Expire overdue active tasks and decrease the owner's rating

=========================================================

Architecture:

- Flask web application architecture.
- Flask handles HTTP requests and application routing.
- Flask Blueprints separate the application into different functional areas.
- Jinja2 templates are used to generate the web pages.
- SQLAlchemy ORM is used to communicate with the database.
- SQLite stores application data locally in `instance/trackmate-local.db`.
- Proof images are stored locally in `app/static/uploads/proofs/`.
- `trackmate_lib` provides small framework-independent goal and task rules.
- Flask-Login manages authenticated user sessions.
- The application is divided into modules for authentication, goals, tasks, friends, profiles, and proof management.

=========================================================

Technologies Used:

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Login
- Flask-WTF
- WTForms
- SQLite
- Jinja2
- Bootstrap 5
- HTML
- CSS

=========================================================

Database:
The application uses a local SQLite relational database. This makes the project runnable and testable without Supabase credentials or an internet connection.

The main entities are:

- Users:
  Stores user accounts, authentication information, ratings, and other user-related data.

- Goals:
  Stores goals created by users and their assigned supervisors.

- Tasks:
  Stores tasks belonging to goals, including their title, description, deadline, weight, and status.

- Proofs:
  Stores proof submissions associated with tasks, including their status and submitted information.

- Friendships:
  Stores relationships and friend requests between users.

=========================================================

Installation Guide:

Requirements: Python 3.12 or newer and Git.

1. Clone and enter the project:

```powershell
git clone https://github.com/tusharrbhardwaj/TrackMate.git
====
cd TrackMate
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

For Git Bash, use:

```bash
source .venv/Scripts/activate
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Start the application:

```powershell
python -m flask --app app.run run --debug

- Open the application in a browser:
http://127.0.0.1:5000/
```

5. Open http://127.0.0.1:5000/ in a browser and register an account.

No `.env` file, Supabase account, remote database, or internet connection is required to run the application. On its first start, TrackMate creates:

- `instance/trackmate-local.db` for SQLite data;
- `app/static/uploads/proofs/` for uploaded proof images.

Both locations are ignored by Git, so each developer gets private local data.

=========================================================

Testing:
The project contains automated tests. To run them:

- python -m pytest

```powershell
python -m pytest
```

Coverage report:

```powershell
python -m pytest --cov=app --cov=trackmate_lib --cov-branch --cov-report=term-missing --cov-report=html
```

Static analysis:

```powershell
ruff check app trackmate_lib tests
```

Testing documentation and the defect log are in `docs/`.

TrackMate was developed as a university Software Design and Modelling project and provides the main functionality for goal management, task tracking, friend supervision, proof submission, and proof review.
