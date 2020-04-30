import requests
import json


import config


api_url = 'http://127.0.0.1:8000/'


def signup_users():
    users = []

    for counter in range(config.NUMBER_OF_USERS):
        data = {
            'username': config.BASE_USERNAME_AND_PASSWORD + str(counter),
            'password': config.BASE_USERNAME_AND_PASSWORD + str(counter),
        }
        r = requests.post(api_url + 'api/users/', data=data)

        response = json.loads(r.text)
        if r.status_code == 201:  # created
            users.append(data)

        else:
            print("There was a problem during creating new users, try to change their username or Base username")
            print(response)

    return users


def login_users(users):
    tokens = []

    for user in users:
        r = requests.post(api_url + 'login/', user)

        response = json.loads(r.text)
        if r.status_code == 200:  # OK
            tokens.append(response['access'])

        else:
            print("There was a problem during login users")
            print(response)

    return tokens


if __name__ == "__main__":
    registered_users = signup_users()
    print(registered_users)

    access_tokens = login_users(registered_users)
    print(access_tokens)



