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

- Clone the repository:
git clone https://github.com/tusharrbhardwaj/TrackMate.git

- Open the project directory:
cd TrackMate

- Create a virtual environment:
python -m venv .venv

- Activate the virtual environment.
Windows PowerShell: .venv\Scripts\Activate.ps1

- Install the required dependencies:
pip install -r requirements.txt

- Start the application:
python -m flask --app app.run run --debug

- Open the application in a browser:
http://127.0.0.1:5000/

=========================================================

Testing:
The project contains automated tests. To run them:
- python -m pytest

Coverage report:
- python -m pytest --cov=app --cov=trackmate_lib --cov-branch --cov-report=term-missing --cov-report=html

Static analysis:
- ruff check app trackmate_lib tests

Testing documentation and the defect log are in `docs/`.


TrackMate was developed as a university Software Design and Modelling project and provides the main functionality for goal management, task tracking, friend supervision, proof submission, and proof review.


