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
- Supabase is used for the application's PostgreSQL database and proof file storage.
- Flask-Login manages authenticated user sessions.
- The application is divided into modules for authentication, goals, tasks, friends, profiles, and proof management.

=========================================================
Technologies Used:
- Python 3
- lask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Login
- Flask-WTF
- WTForms
- PostgreSQL
- Supabase
- Jinja2
- Bootstrap 5
- HTML
- CSS

=========================================================
Database:
The application uses a relational PostgreSQL database managed through Supabase.


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

- Create a .env file in the project root and add the required database and Supabase configuration:
DATABASE_URL=your_postgresql_connection_string
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key

- Start the application:
python run.py

- Open the application in a browser:
http://127.0.0.1:5000/

=========================================================
Testing:
The project contains automated tests. To run them:
- pytest


TrackMate was developed as a university Software Design and Modelling project and provides the main functionality for goal management, task tracking, friend supervision, proof submission, and proof review.


