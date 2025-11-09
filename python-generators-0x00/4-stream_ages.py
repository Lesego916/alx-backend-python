#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row['age']

    cursor.close()
    connection.close()

def average_user_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += float(age)
        count += 1

    avg = total / count if count > 0 else 0
    print(f"Average age of users: {avg:.2f}")

if __name__ == "__main__":
    average_user_age()
