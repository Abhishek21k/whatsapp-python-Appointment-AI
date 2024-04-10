import requests


def get_clinics(latitude, longitude, nearest):
    api_url = " http://localhost:3000/api/getClinics"
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "nearest": nearest
    }

    try:

        response = requests.post(api_url, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract clinic information from the response
            clinics = data.get("message", [])
            return clinics
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_Appointment(clinic_id):
    api_url = " http://localhost:3000/api/getAppointment"
    payload = {
        "clinicUserId": clinic_id
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def add_user_appointment(clinic, time, mobile, date):
    api_url = " http://localhost:3000/api/addAppointment"
    payload = {
        "clinic": clinic,
        "time": time,
        "mobile": mobile,
        "date": date
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "Failed to add appointment"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while adding the appointment"


def update_appointment(id, clinic, date, time):
    api_url = " http://localhost:3000/api/updateAppointment"
    payload = {
        "id": id,
        "clinic": clinic,
        "date": date,
        "time": time
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json().get("message", "Appointment updated successfully")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "Failed to update appointment"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while adding the appointment"


def get_user_appointments_fromServer(mobile):
    api_url = " http://localhost:3000/api/getUserAppointments"
    payload = {
        "mobile": mobile,
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "Failed to Get User appointments"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while Getting the appointments"


def addUser(mobile, name, address):
    api_url = f" http://localhost:3000/api/addUser"
    payload = {
        "mobile": mobile,
        "name": name,
        "address": address
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def getUser(mobile):
    api_url = f" http://localhost:3000/api/getUser"
    payload = {
        "mobile": mobile
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def updateUser(mobile, name, address):
    api_url = f" http://localhost:3000/api/updateUser"
    payload = {
        "mobile": mobile,
        "name": name,
        "address": address
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def get_conversation(mobile):
    api_url = f" http://localhost:3000/api/getConversation"
    payload = {
        "mobile": mobile
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            messages = response.json()["message"]
            return messages
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def add_conversation(mobile, user, bot):
    api_url = " http://localhost:3000/api/addConversation"
    payload = {
        "mobile": mobile,
        "user": user,
        "bot": bot
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()["message"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "Failed to send message"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while sending the message"


# if __name__ == "__main__":
#     clinics = get_clinics(0, 0)
#     print(clinics)
