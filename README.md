## Usage

This is a system designed to manage a library using django as back-end and telegram as frontend.

### Getting Started

First, create a database and run .sql scripts in the repository with the given order:
1. Tables.sql
2. Trigers.sql
3. Views.sql
4. Functions.sql
5. Procedures.sql
6. Logging Triggers.sql
7. Logging Views.sql

After that, Install the required packages:

```bash
pip install -r requirements
```

Change the BASE_URL value in data.py with your device IP

then open a terminal and run the back-end server:
```bash
python Backend/manage.py runserver 0.0.0.0:8000
```

Open another terminal and run the telegram script:
```bash
python Frontend/main.py
```

Now you can access the Robot via [t.me/LibrarianDB_bot](Librarian Bot)

For more help, send /help to the robot.