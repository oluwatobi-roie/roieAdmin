import secrets, string
# from flask import session
from datetime import datetime, timedelta, timezone

secret_key = secrets.token_hex(16)
myKey = '75392fe36ed27a058c950b427bb9a60e'
roie_endpoint = 'https://track.roie.com.ng/api/'



def userRestriction(id):
    adminuser = [1, 481, 856]
    premiumUser = [725]

    if id in adminuser:
        return("admin")
    elif id in premiumUser:
        return("premium")
    else:
        return ("unathorized")




def getOneYearDate():
    # Get the current date and time
    current_datetime = datetime.now(timezone.utc)

    # Add one year to the current date and time
    one_year_later = current_datetime + timedelta(days=365)

    # Convert to ISO 8601 format
    convert_one_year_to_iso = one_year_later.isoformat()

    return convert_one_year_to_iso


# Function to generate 
def randomPassword(length):
    # set a variable to include alphanumerc characters
    characters = string.ascii_letters + string.digits

    # use secrets to randomize selection of all the variable to a length as passed from the function.
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    print(password)
    
    return password



# define a notification wizard to set notification for certain clients.
def notification_wizard(type):
    # save basic notifications in an array
    basic_notification = ['ignitionOn', 'ignitionOff', 'geofenceEnter', 'geofenceExit']

    # check if passed variable is in an basic notification
    if type in basic_notification:
        data = {
            "always":'true',
            "type":type,
            "notificators":"traccar,firebase,web"
        }
        return data
    
    # if type is an alarm include formating for alarm
    else:
        data = {
            "attributes": {"alarms":"powerCut"},
            "always":'true',
            "type":"alarm",
            "notificators":"traccar,firebase,web,mail"
        }
        return  data

