import requests
import lorem
import random

import config


def signup_users():
    users = []

    for counter in range(config.NUMBER_OF_USERS):
        data = {
            'username': config.BASE_USERNAME_AND_PASSWORD + str(counter),
            'password': config.BASE_USERNAME_AND_PASSWORD + str(counter),
        }
        r = requests.post(config.API_URL + 'api/users/', data=data)

        response = r.json()
        if r.status_code == 201:  # created
            users.append(data)

        else:
            print("There was a problem during creating new users, try to change their username or Base username")
            print(response)

    return users


def login_users(users):
    tokens = []

    for user in users:
        r = requests.post(config.API_URL + 'login/', data=user)

        response = r.json()
        if r.status_code == 200:  # OK
            tokens.append(response['access'])

        else:
            print("There was a problem during login users")
            print(response)

    return tokens


def create_post_activity(tokens):
    posts_id = []

    for token in tokens:
        headers = {
            'Authorization': 'Bearer ' + token,
        }

        posts_count = random.randint(0, config.MAX_POSTS_PER_USER)
        for i in range(posts_count):
            data = {
                'title': lorem.sentence(),
                'content': lorem.paragraph(),
            }
            r = requests.post(config.API_URL + 'api/posts/', headers=headers, data=data)

            response = r.json()
            if r.status_code == 201:  # created
                posts_id.append(response['id'])

            else:
                print("There was a problem during creating posts")
                print(response)

    return posts_id


def create_like_activity(tokens, posts_id):
    for token in tokens:
        headers = {
            'Authorization': 'Bearer ' + token,
        }

        likes_count = random.randint(0, config.MAX_LIKES_PER_USER)
        for i in range(likes_count):
            like_or_unlike = random.randint(0, 5)
            url = config.API_URL + 'api/posts/' + str(random.choice(posts_id)) + '/'

            if like_or_unlike < 3:
                r = requests.post(url + 'like/', headers=headers)

            else:
                r = requests.post(url + 'unlike/', headers=headers)

            # response = r.json()
            # print(response)


if __name__ == "__main__":
    registered_users = signup_users()
    print(registered_users)

    access_tokens = login_users(users=registered_users)
    print(access_tokens)

    created_posts_id = create_post_activity(tokens=access_tokens)
    print(created_posts_id)

    create_like_activity(tokens=access_tokens, posts_id=created_posts_id)



