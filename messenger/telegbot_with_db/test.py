import sqlite3

try:
    conn = sqlite3.connect("accountant.db")
    cursor = conn.cursor()

    # Create user with user_id = 1000
    cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (1000,))

    # Reading all users
    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())

    # Apply changes
    conn.commit()


except sqlite3.Error as error:
    print("Error", error)

finally:
    if (conn):
        conn.close()
