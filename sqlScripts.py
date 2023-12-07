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

        # query = f'UPDATE tc_user_notification SET userid = {new_user_id} WHERE notificationid BETWEEN {notifications[0]} AND {notifications[-1]};'

        # cursor.execute(query)


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
