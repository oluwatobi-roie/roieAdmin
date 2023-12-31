import mysql.connector
from credentials import database_config



def assign_user_notification(new_user_id, notifications):
    # print (new_user_id)
    # print(f'First Notification ID: {notifications[0]}')
    # print(f'First Notification ID: {notifications[-1]}')

    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**database_config)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(buffered=True)

        query = 'UPDATE tc_user_notification SET userid = %s WHERE notificationid BETWEEN %s AND %s;'

        cursor.execute(query, (new_user_id, notifications[0], notifications[-1]))
        connection.commit()

        if cursor.rowcount > 0:
            print("All Notifications has been setup for User")
        else:
            print("No Notifications were updated")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and the connection in the 'finally' block to ensure they are always closed
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


def search_user(email):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**database_config)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(buffered=True)

        query = 'SELECT id, email FROM tc_users WHERE email = %s;'

        cursor.execute(query, (email,))
        connection.commit()

        if cursor.rowcount > 0:
            user_data = cursor.fetchone()  # Fetch the first row
            user_id = user_data[0]  # Get the id from the result
            return True, user_id
        else:
            print("No User found")
            return False, None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False, None

    finally:
        # Close the cursor and the connection in the 'finally' block to ensure they are always closed
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


def link_device_user(userid, deviceid):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**database_config)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(buffered=True)

        query = 'INSERT INTO tc_user_device (userid, deviceid) VALUES (%s, %s);'

        cursor.execute(query, (userid, deviceid))
        connection.commit()

        if cursor.rowcount > 0:
            print("user Successfully Linked")
            return True
        else:
            print("Something went Wrong")
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and the connection in the 'finally' block to ensure they are always closed
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")