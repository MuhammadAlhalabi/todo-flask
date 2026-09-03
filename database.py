import sqlite3


def init_db():
  connection = sqlite3.connect("database.db")
  connection.execute("PRAGMA foreign_keys=ON")
  connection.execute("""
  CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
  )
  """)
  connection.execute("""
  CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0,1)),
  user_id INTEGER NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
  )
  """)
  connection.commit()
  connection.close()

def get_connection():
    connection=sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys=ON")
    return connection

def add_user(username, password):
    connection = get_connection()
    connection.execute(
        "INSERT INTO users (username,password) VALUES(?,?) ", (username, password)
    )
    connection.commit()
    connection.close()


def get_user(username):
    connection = get_connection()
    connection.row_factory = (
        sqlite3.Row
    )
    user = connection.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()
    connection.close()
    return user


def update_user(new_username, user_id):
    connection = get_connection()
    connection.execute(
        """
  UPDATE users
  SET username=?
  WHERE id=?
  """,
        (new_username, user_id),
    )
    connection.commit()
    connection.close()


def update_password_db(hashed_password, user_id):
    connection = get_connection()
    connection.execute(
        """
  UPDATE users 
  SET password=?
  WHERE id=?
  """,
        (hashed_password, user_id),
    )
    connection.commit()
    connection.close()


def delete_user_from_database(user_id):
    connection = get_connection()
    connection.execute(
        """
  DELETE FROM users 
  WHERE id=?
  """,
        (user_id,),
    )
    connection.commit()
    connection.close()


def add_task(title, user_id):
    connection = get_connection()
    connection.execute(
        "INSERT INTO tasks (title,user_id) VALUES(?,?)", (title, user_id)
    )
    connection.commit()
    connection.close()


def get_tasks(user_id, filter_task):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    if filter_task == "active":
        tasks = connection.execute(
            "SELECT * FROM tasks WHERE user_id=? AND completed = 0", (user_id,)
        ).fetchall()
    elif filter_task == "completed":
        tasks = connection.execute(
            "SELECT * FROM tasks WHERE user_id=? AND completed = 1", (user_id,)
        ).fetchall()
    else:
        tasks = connection.execute(
            "SELECT * FROM tasks WHERE user_id=?", (user_id,)
        ).fetchall()
    connection.close()
    return tasks


def get_task(task_id, user_id):
    connection = get_connection()
    task = connection.execute(
        """
  SELECT * FROM tasks 
  WHERE id=? AND user_id=?
  """,
        (task_id, user_id),
    ).fetchone()
    connection.close()
    return task


def update_task_status(task_id, completed, user_id):
    connection = get_connection()
    connection.execute(
        """
  UPDATE tasks 
  SET completed=?
  WHERE id=? AND user_id=?
  """,
        (completed, task_id, user_id),
    )
    connection.commit()
    connection.close()


def edit_task_from_db(title, task_id, user_id):
    connection = get_connection()
    connection.execute(
        """
  UPDATE tasks 
  SET title=?
  WHERE id =? AND user_id=?
""",
        (title, task_id, user_id),
    )
    connection.commit()
    connection.close()


def delete_task_from_db(task_id, user_id):
    connection = get_connection()
    connection.execute(
        """
    DELETE FROM tasks 
    WHERE id=? AND user_id=?
    """,
        (task_id, user_id),
    )
    connection.commit()
    connection.close()

def get_total_tasks(user_id):
    connection=get_connection()
    total_tasks=connection.execute("""
    SELECT COUNT(*) FROM tasks
    WHERE user_id=?
    """,(user_id,)).fetchone()[0]
    connection.close()
    return total_tasks


def get_completed_tasks_count(user_id):
    connection=get_connection()
    completed_tasks=connection.execute("""
    SELECT COUNT(*) FROM tasks
    WHERE user_id=?
    AND completed=1
    """,(user_id,)).fetchone()[0]
    connection.close()
    return completed_tasks


def get_uncompleted_tasks_count(user_id):
    connection=get_connection()
    uncompleted_tasks=connection.execute("""
    SELECT COUNT(*) FROM tasks
    WHERE user_id=?
    AND completed=0
    """,(user_id,)).fetchone()[0]
    connection.close()
    return uncompleted_tasks
